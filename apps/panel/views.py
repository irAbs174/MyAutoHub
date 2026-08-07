from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from apps.cars.models import Brand, Car, CarModel, Dealer, OBDCode, RepairShop, Trim
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
    DealerForm,
    EmergencyServiceForm,
    OBDCodeForm,
    PanelContentSearchForm,
    PanelEmergencySearchForm,
    RepairShopForm,
    StoryForm,
    TrimForm,
    YoutubeVideoForm,
    build_car_related_forms,
    car_related_forms_valid,
    save_car_related,
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


def _car_form_context(form, spec_form, dims_form, formsets, editing, car=None):
    return {
        "form": form,
        "spec_form": spec_form,
        "dims_form": dims_form,
        "formsets": formsets,
        "formset": formsets["photos"],
        "editing": editing,
        "car": car,
        "panel_section": "cars",
    }


@staff_required
def car_list(request):
    form = PanelContentSearchForm(request.GET or None)
    qs = Car.objects.select_related("model__brand", "trim")
    if form.is_valid():
        q = form.cleaned_data.get("q")
        published = form.cleaned_data.get("published")
        if q:
            qs = qs.filter(
                Q(model__name__icontains=q)
                | Q(model__brand__name__icontains=q)
                | Q(trim__name__icontains=q)
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
        spec_form, dims_form, formsets = build_car_related_forms(
            request.POST, request.FILES
        )
        if form.is_valid() and car_related_forms_valid(spec_form, dims_form, formsets):
            car = form.save()
            save_car_related(car, spec_form, dims_form, formsets)
            messages.success(request, _("Car created."))
            return redirect("panel:car_list")
    else:
        form = CarForm()
        spec_form, dims_form, formsets = build_car_related_forms()
    return render(
        request,
        "panel/cars/form.html",
        _car_form_context(form, spec_form, dims_form, formsets, editing=False),
    )


@staff_required
def car_edit(request, pk):
    car = get_object_or_404(
        Car.objects.select_related("model__brand", "trim"), pk=pk
    )
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES, instance=car)
        spec_form, dims_form, formsets = build_car_related_forms(
            request.POST, request.FILES, instance=car
        )
        if form.is_valid() and car_related_forms_valid(spec_form, dims_form, formsets):
            form.save()
            save_car_related(car, spec_form, dims_form, formsets)
            messages.success(request, _("Car updated."))
            return redirect("panel:car_list")
    else:
        form = CarForm(instance=car)
        spec_form, dims_form, formsets = build_car_related_forms(instance=car)
    return render(
        request,
        "panel/cars/form.html",
        _car_form_context(
            form, spec_form, dims_form, formsets, editing=True, car=car
        ),
    )


@staff_required
def brand_list(request):
    brands = Brand.objects.annotate(model_count=Count("models")).prefetch_related(
        "models__trims"
    )
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
def trim_create(request):
    initial = {}
    model_id = request.GET.get("model")
    if model_id:
        initial["car_model"] = model_id
    if request.method == "POST":
        form = TrimForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Trim created."))
            return redirect("panel:brand_list")
    else:
        form = TrimForm(initial=initial)
    return render(
        request,
        "panel/cars/trim_form.html",
        {
            "form": form,
            "editing": False,
            "panel_section": "cars",
        },
    )


@staff_required
def trim_edit(request, pk):
    trim = get_object_or_404(Trim.objects.select_related("car_model__brand"), pk=pk)
    if request.method == "POST":
        form = TrimForm(request.POST, instance=trim)
        if form.is_valid():
            form.save()
            messages.success(request, _("Trim updated."))
            return redirect("panel:brand_list")
    else:
        form = TrimForm(instance=trim)
    return render(
        request,
        "panel/cars/trim_form.html",
        {
            "form": form,
            "editing": True,
            "trim": trim,
            "panel_section": "cars",
        },
    )


@staff_required
def obd_list(request):
    form = PanelContentSearchForm(request.GET or None)
    qs = OBDCode.objects.select_related("car_model__brand")
    model_id = request.GET.get("model")
    if model_id:
        qs = qs.filter(car_model_id=model_id)
    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            qs = qs.filter(
                Q(code__icontains=q)
                | Q(title__icontains=q)
                | Q(car_model__name__icontains=q)
            )
    return render(
        request,
        "panel/cars/obd_list.html",
        {
            "codes": qs,
            "form": form,
            "panel_section": "cars",
        },
    )


@staff_required
def obd_create(request):
    initial = {}
    model_id = request.GET.get("model")
    if model_id:
        initial["car_model"] = model_id
    if request.method == "POST":
        form = OBDCodeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("OBD code created."))
            return redirect("panel:obd_list")
    else:
        form = OBDCodeForm(initial=initial)
    return render(
        request,
        "panel/cars/obd_form.html",
        {
            "form": form,
            "editing": False,
            "panel_section": "cars",
        },
    )


@staff_required
def obd_edit(request, pk):
    code = get_object_or_404(OBDCode.objects.select_related("car_model"), pk=pk)
    if request.method == "POST":
        form = OBDCodeForm(request.POST, instance=code)
        if form.is_valid():
            form.save()
            messages.success(request, _("OBD code updated."))
            return redirect("panel:obd_list")
    else:
        form = OBDCodeForm(instance=code)
    return render(
        request,
        "panel/cars/obd_form.html",
        {
            "form": form,
            "editing": True,
            "code": code,
            "panel_section": "cars",
        },
    )


@staff_required
def dealer_list(request):
    form = PanelContentSearchForm(request.GET or None)
    qs = Dealer.objects.prefetch_related("brands")
    if form.is_valid():
        q = form.cleaned_data.get("q")
        published = form.cleaned_data.get("published")
        if q:
            qs = qs.filter(
                Q(name__icontains=q) | Q(city__icontains=q) | Q(phone__icontains=q)
            )
        qs = _apply_published_filter(qs, published)
    return render(
        request,
        "panel/cars/dealer_list.html",
        {
            "dealers": qs,
            "form": form,
            "panel_section": "dealers",
        },
    )


@staff_required
def dealer_create(request):
    if request.method == "POST":
        form = DealerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Dealer created."))
            return redirect("panel:dealer_list")
    else:
        form = DealerForm()
    return render(
        request,
        "panel/cars/dealer_form.html",
        {
            "form": form,
            "editing": False,
            "panel_section": "dealers",
        },
    )


@staff_required
def dealer_edit(request, pk):
    dealer = get_object_or_404(Dealer, pk=pk)
    if request.method == "POST":
        form = DealerForm(request.POST, instance=dealer)
        if form.is_valid():
            form.save()
            messages.success(request, _("Dealer updated."))
            return redirect("panel:dealer_list")
    else:
        form = DealerForm(instance=dealer)
    return render(
        request,
        "panel/cars/dealer_form.html",
        {
            "form": form,
            "editing": True,
            "dealer": dealer,
            "panel_section": "dealers",
        },
    )


@staff_required
def repair_shop_list(request):
    form = PanelContentSearchForm(request.GET or None)
    qs = RepairShop.objects.prefetch_related("brands")
    if form.is_valid():
        q = form.cleaned_data.get("q")
        published = form.cleaned_data.get("published")
        if q:
            qs = qs.filter(
                Q(name__icontains=q) | Q(city__icontains=q) | Q(phone__icontains=q)
            )
        qs = _apply_published_filter(qs, published)
    return render(
        request,
        "panel/cars/repair_shop_list.html",
        {
            "shops": qs,
            "form": form,
            "panel_section": "repair_shops",
        },
    )


@staff_required
def repair_shop_create(request):
    if request.method == "POST":
        form = RepairShopForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Repair shop created."))
            return redirect("panel:repair_shop_list")
    else:
        form = RepairShopForm()
    return render(
        request,
        "panel/cars/repair_shop_form.html",
        {
            "form": form,
            "editing": False,
            "panel_section": "repair_shops",
        },
    )


@staff_required
def repair_shop_edit(request, pk):
    shop = get_object_or_404(RepairShop, pk=pk)
    if request.method == "POST":
        form = RepairShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, _("Repair shop updated."))
            return redirect("panel:repair_shop_list")
    else:
        form = RepairShopForm(instance=shop)
    return render(
        request,
        "panel/cars/repair_shop_form.html",
        {
            "form": form,
            "editing": True,
            "shop": shop,
            "panel_section": "repair_shops",
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
