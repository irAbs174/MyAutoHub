from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from apps.cars.models import Brand, Car, CarModel
from apps.emergency.forms import VerifyEmergencyTransitionForm
from apps.emergency.models import EmergencyRequest, EmergencyService, RequestStatus
from apps.emergency.services import (
    is_emergency_operator,
    is_emergency_operator_admin,
    transition_request,
)
from apps.stories.models import Story
from apps.youtube.models import YoutubeVideo

from .decorators import staff_required
from .forms import (
    BrandForm,
    CarForm,
    CarModelForm,
    CarPhotoFormSet,
    EmergencyServiceForm,
    PanelContentSearchForm,
    PanelEmergencySearchForm,
    StoryForm,
    YoutubeVideoForm,
)


def _request_queryset():
    return EmergencyRequest.objects.select_related(
        "service", "requester", "saved_location"
    ).annotate(
        unread_buzz_count=Count(
            "buzzes", filter=Q(buzzes__seen_by_operators=False)
        )
    )


def _apply_published_filter(qs, published):
    if published == "1":
        return qs.filter(is_published=True)
    if published == "0":
        return qs.filter(is_published=False)
    return qs


@staff_required
def overview(request):
    qs = EmergencyRequest.objects.all()
    waiting = qs.filter(status=RequestStatus.WAIT_FOR_ACCEPT).count()
    processing = qs.filter(status=RequestStatus.PROCESSING).count()
    unread_buzzes = (
        EmergencyRequest.objects.filter(buzzes__seen_by_operators=False)
        .distinct()
        .count()
    )
    active_services = EmergencyService.objects.filter(is_active=True).count()
    published_cars = Car.objects.filter(is_published=True).count()
    published_videos = YoutubeVideo.objects.filter(is_published=True).count()
    published_stories = Story.objects.filter(is_published=True).count()
    recent = _request_queryset()[:8]
    return render(
        request,
        "panel/overview.html",
        {
            "stats": {
                "waiting": waiting,
                "processing": processing,
                "unread_buzzes": unread_buzzes,
                "active_services": active_services,
                "published_cars": published_cars,
                "published_videos": published_videos,
                "published_stories": published_stories,
            },
            "recent_requests": recent,
            "panel_section": "overview",
        },
    )


@staff_required
def emergency_request_list(request):
    form = PanelEmergencySearchForm(request.GET or None)
    qs = _request_queryset()
    if form.is_valid():
        q = form.cleaned_data.get("q")
        status = form.cleaned_data.get("status")
        service = form.cleaned_data.get("service")
        if q:
            qs = qs.filter(
                Q(description__icontains=q)
                | Q(service__name__icontains=q)
                | Q(requester__username__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        if service:
            qs = qs.filter(service=service)
    return render(
        request,
        "panel/emergency/request_list.html",
        {
            "requests": qs,
            "form": form,
            "panel_section": "emergency",
        },
    )


@staff_required
def emergency_request_detail(request, pk):
    emergency = get_object_or_404(
        _request_queryset().prefetch_related("transitions", "buzzes"),
        pk=pk,
    )
    verify_form = VerifyEmergencyTransitionForm(
        user=request.user, emergency_request=emergency
    )
    return render(
        request,
        "panel/emergency/request_detail.html",
        {
            "emergency": emergency,
            "verify_form": verify_form,
            "latlng": emergency.resolve_coordinates(),
            "is_operator": is_emergency_operator(request.user),
            "is_operator_admin": is_emergency_operator_admin(request.user),
            "panel_section": "emergency",
        },
    )


@staff_required
def emergency_request_verify(request, pk):
    emergency = get_object_or_404(EmergencyRequest, pk=pk)
    if request.method != "POST":
        return redirect("panel:emergency_request_detail", pk=pk)
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
    return redirect("panel:emergency_request_detail", pk=pk)


@staff_required
def emergency_service_list(request):
    services = EmergencyService.objects.annotate(request_count=Count("requests"))
    return render(
        request,
        "panel/emergency/service_list.html",
        {
            "services": services,
            "panel_section": "services",
        },
    )


@staff_required
def emergency_service_create(request):
    if request.method == "POST":
        form = EmergencyServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Service created."))
            return redirect("panel:emergency_service_list")
    else:
        form = EmergencyServiceForm()
    return render(
        request,
        "panel/emergency/service_form.html",
        {
            "form": form,
            "editing": False,
            "panel_section": "services",
        },
    )


@staff_required
def emergency_service_edit(request, pk):
    service = get_object_or_404(EmergencyService, pk=pk)
    if request.method == "POST":
        form = EmergencyServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, _("Service updated."))
            return redirect("panel:emergency_service_list")
    else:
        form = EmergencyServiceForm(instance=service)
    return render(
        request,
        "panel/emergency/service_form.html",
        {
            "form": form,
            "editing": True,
            "service": service,
            "panel_section": "services",
        },
    )


@staff_required
def car_list(request):
    form = PanelContentSearchForm(request.GET or None)
    qs = Car.objects.select_related("model__brand")
    if form.is_valid():
        q = form.cleaned_data.get("q")
        published = form.cleaned_data.get("published")
        if q:
            qs = qs.filter(
                Q(model__name__icontains=q)
                | Q(model__brand__name__icontains=q)
                | Q(trim__icontains=q)
                | Q(description__icontains=q)
            )
        qs = _apply_published_filter(qs, published)
    return render(
        request,
        "panel/cars/list.html",
        {
            "cars": qs,
            "form": form,
            "panel_section": "cars",
        },
    )


@staff_required
def car_create(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            formset = CarPhotoFormSet(request.POST, request.FILES, instance=car)
            if formset.is_valid():
                car.save()
                formset.save()
                messages.success(request, _("Car created."))
                return redirect("panel:car_list")
        else:
            formset = CarPhotoFormSet(request.POST, request.FILES)
    else:
        form = CarForm()
        formset = CarPhotoFormSet()
    return render(
        request,
        "panel/cars/form.html",
        {
            "form": form,
            "formset": formset,
            "editing": False,
            "panel_section": "cars",
        },
    )


@staff_required
def car_edit(request, pk):
    car = get_object_or_404(Car.objects.select_related("model__brand"), pk=pk)
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES, instance=car)
        formset = CarPhotoFormSet(request.POST, request.FILES, instance=car)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, _("Car updated."))
            return redirect("panel:car_list")
    else:
        form = CarForm(instance=car)
        formset = CarPhotoFormSet(instance=car)
    return render(
        request,
        "panel/cars/form.html",
        {
            "form": form,
            "formset": formset,
            "editing": True,
            "car": car,
            "panel_section": "cars",
        },
    )


@staff_required
def brand_list(request):
    brands = Brand.objects.annotate(model_count=Count("models"))
    return render(
        request,
        "panel/cars/brand_list.html",
        {
            "brands": brands,
            "panel_section": "cars",
        },
    )


@staff_required
def brand_create(request):
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Brand created."))
            return redirect("panel:brand_list")
    else:
        form = BrandForm()
    return render(
        request,
        "panel/cars/brand_form.html",
        {
            "form": form,
            "editing": False,
            "panel_section": "cars",
        },
    )


@staff_required
def brand_edit(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == "POST":
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, _("Brand updated."))
            return redirect("panel:brand_list")
    else:
        form = BrandForm(instance=brand)
    return render(
        request,
        "panel/cars/brand_form.html",
        {
            "form": form,
            "editing": True,
            "brand": brand,
            "panel_section": "cars",
        },
    )


@staff_required
def car_model_create(request):
    initial = {}
    brand_id = request.GET.get("brand")
    if brand_id:
        initial["brand"] = brand_id
    if request.method == "POST":
        form = CarModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Car model created."))
            return redirect("panel:brand_list")
    else:
        form = CarModelForm(initial=initial)
    return render(
        request,
        "panel/cars/model_form.html",
        {
            "form": form,
            "editing": False,
            "panel_section": "cars",
        },
    )


@staff_required
def car_model_edit(request, pk):
    car_model = get_object_or_404(CarModel.objects.select_related("brand"), pk=pk)
    if request.method == "POST":
        form = CarModelForm(request.POST, instance=car_model)
        if form.is_valid():
            form.save()
            messages.success(request, _("Car model updated."))
            return redirect("panel:brand_list")
    else:
        form = CarModelForm(instance=car_model)
    return render(
        request,
        "panel/cars/model_form.html",
        {
            "form": form,
            "editing": True,
            "car_model": car_model,
            "panel_section": "cars",
        },
    )


@staff_required
def youtube_list(request):
    form = PanelContentSearchForm(request.GET or None)
    qs = YoutubeVideo.objects.all()
    if form.is_valid():
        q = form.cleaned_data.get("q")
        published = form.cleaned_data.get("published")
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(youtube_id__icontains=q)
                | Q(description__icontains=q)
            )
        qs = _apply_published_filter(qs, published)
    return render(
        request,
        "panel/youtube/list.html",
        {
            "videos": qs,
            "form": form,
            "panel_section": "youtube",
        },
    )


@staff_required
def youtube_create(request):
    if request.method == "POST":
        form = YoutubeVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Video created."))
            return redirect("panel:youtube_list")
    else:
        form = YoutubeVideoForm()
    return render(
        request,
        "panel/youtube/form.html",
        {
            "form": form,
            "editing": False,
            "panel_section": "youtube",
        },
    )


@staff_required
def youtube_edit(request, pk):
    video = get_object_or_404(YoutubeVideo, pk=pk)
    if request.method == "POST":
        form = YoutubeVideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, _("Video updated."))
            return redirect("panel:youtube_list")
    else:
        form = YoutubeVideoForm(instance=video)
    return render(
        request,
        "panel/youtube/form.html",
        {
            "form": form,
            "editing": True,
            "video": video,
            "panel_section": "youtube",
        },
    )


@staff_required
def story_list(request):
    form = PanelContentSearchForm(request.GET or None)
    qs = Story.objects.select_related("author")
    if form.is_valid():
        q = form.cleaned_data.get("q")
        published = form.cleaned_data.get("published")
        if q:
            qs = qs.filter(
                Q(title_fa__icontains=q)
                | Q(title_en__icontains=q)
                | Q(title_ar__icontains=q)
                | Q(slug__icontains=q)
                | Q(excerpt_fa__icontains=q)
                | Q(excerpt_en__icontains=q)
                | Q(excerpt_ar__icontains=q)
            )
        qs = _apply_published_filter(qs, published)
    return render(
        request,
        "panel/stories/list.html",
        {
            "stories": qs,
            "form": form,
            "panel_section": "stories",
        },
    )


@staff_required
def story_create(request):
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            if not story.author_id:
                story.author = request.user
            story.save()
            messages.success(request, _("Story created."))
            return redirect("panel:story_list")
    else:
        form = StoryForm(initial={"author": request.user})
    return render(
        request,
        "panel/stories/form.html",
        {
            "form": form,
            "editing": False,
            "panel_section": "stories",
        },
    )


@staff_required
def story_edit(request, pk):
    story = get_object_or_404(Story.objects.select_related("author"), pk=pk)
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES, instance=story)
        if form.is_valid():
            form.save()
            messages.success(request, _("Story updated."))
            return redirect("panel:story_list")
    else:
        form = StoryForm(instance=story)
    return render(
        request,
        "panel/stories/form.html",
        {
            "form": form,
            "editing": True,
            "story": story,
            "panel_section": "stories",
        },
    )
