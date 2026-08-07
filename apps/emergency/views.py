from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from .forms import (
    EmergencyReviewForm,
    EmergencySearchForm,
    SubmitNewEmergencyRequestForm,
    VerifyEmergencyTransitionForm,
)
from .models import EmergencyRequest, RequestStatus
from .services import (
    add_public_review,
    buzz_request,
    create_emergency_request,
    is_emergency_operator,
    transition_request,
)


def _visible_queryset(user):
    qs = EmergencyRequest.objects.select_related(
        "service", "requester", "saved_location"
    ).annotate(buzz_count=Count("buzzes", filter=Q(buzzes__seen_by_operators=False)))
    if is_emergency_operator(user):
        return qs
    if user.is_authenticated:
        return qs.filter(requester=user)
    return qs.none()


def list_requests(request):
    form = EmergencySearchForm(request.GET or None)
    qs = _visible_queryset(request.user)
    if form.is_valid():
        q = form.cleaned_data.get("q")
        service = form.cleaned_data.get("service")
        if q:
            qs = qs.filter(
                Q(description__icontains=q)
                | Q(service__name__icontains=q)
                | Q(requester__username__icontains=q)
            )
        if service:
            qs = qs.filter(service=service)
    return render(
        request,
        "emergency/list.html",
        {
            "requests": qs,
            "form": form,
            "is_operator": is_emergency_operator(request.user),
        },
    )


@login_required
def submit_request(request):
    if request.method == "POST":
        form = SubmitNewEmergencyRequestForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                emergency = create_emergency_request(
                    requester=request.user,
                    service=form.cleaned_data["service"],
                    description=form.cleaned_data["description"],
                    saved_location=form.cleaned_data.get("saved_location"),
                    latitude=form.cleaned_data.get("latitude"),
                    longitude=form.cleaned_data.get("longitude"),
                )
            except ValidationError as exc:
                form.add_error(None, exc)
            else:
                messages.success(
                    request,
                    _(
                        "Emergency request submitted-waiting for an operator to accept."
                    ),
                )
                return redirect("emergency:detail", pk=emergency.pk)
    else:
        form = SubmitNewEmergencyRequestForm(user=request.user)
    return render(request, "emergency/submit.html", {"form": form})


@login_required
def detail(request, pk):
    emergency = get_object_or_404(
        _visible_queryset(request.user).prefetch_related("transitions", "buzzes"),
        pk=pk,
    )
    verify_form = VerifyEmergencyTransitionForm(
        user=request.user, emergency_request=emergency
    )
    review_form = EmergencyReviewForm()
    return render(
        request,
        "emergency/detail.html",
        {
            "emergency": emergency,
            "verify_form": verify_form,
            "review_form": review_form,
            "is_operator": is_emergency_operator(request.user),
            "latlng": emergency.resolve_coordinates(),
        },
    )


@login_required
def verify(request, pk):
    emergency = get_object_or_404(_visible_queryset(request.user), pk=pk)
    if request.method != "POST":
        return redirect("emergency:detail", pk=pk)
    form = VerifyEmergencyTransitionForm(
        request.POST, user=request.user, emergency_request=emergency
    )
    if form.is_valid():
        try:
            transition_request(
                emergency_request=emergency,
                actor=request.user,
                to_status=form.cleaned_data["to_status"],
                note=form.cleaned_data.get("note") or "",
            )
            messages.success(request, _("Request status updated."))
        except (ValidationError, PermissionDenied) as exc:
            messages.error(request, str(exc))
    else:
        messages.error(request, _("Could not update status."))
    return redirect("emergency:detail", pk=pk)


@login_required
def cancel(request, pk):
    emergency = get_object_or_404(_visible_queryset(request.user), pk=pk)
    if request.method == "POST":
        try:
            transition_request(
                emergency_request=emergency,
                actor=request.user,
                to_status=RequestStatus.CANCELLED,
                note=_("Cancelled via cancel action"),
            )
            messages.info(request, _("Request cancelled."))
        except (ValidationError, PermissionDenied) as exc:
            messages.error(request, str(exc))
    return redirect("emergency:detail", pk=pk)


@login_required
def buzz(request, pk):
    emergency = get_object_or_404(_visible_queryset(request.user), pk=pk)
    if request.method == "POST":
        try:
            buzz_request(emergency_request=emergency, user=request.user)
            messages.success(request, _("Buzz sent-operators will notice."))
        except (ValidationError, PermissionDenied) as exc:
            messages.error(request, str(exc))
    return redirect("emergency:detail", pk=pk)


@login_required
def review(request, pk):
    emergency = get_object_or_404(_visible_queryset(request.user), pk=pk)
    if request.method == "POST":
        form = EmergencyReviewForm(request.POST)
        if form.is_valid():
            try:
                add_public_review(
                    emergency_request=emergency,
                    user=request.user,
                    comment=form.cleaned_data["review_comment"],
                    rating=form.cleaned_data.get("review_rating"),
                )
                messages.success(request, _("Thanks for sharing your experience."))
            except (ValidationError, PermissionDenied) as exc:
                messages.error(request, str(exc))
        else:
            messages.error(request, _("Please check the review form."))
    return redirect("emergency:detail", pk=pk)
