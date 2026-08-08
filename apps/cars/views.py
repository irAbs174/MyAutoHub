from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from .forms import (
    COUNTRY_FILTERS,
    DRIVETRAIN_ALIASES,
    FUEL_ALIASES,
    SORT_ORDERING,
    TRANSMISSION_ALIASES,
    CarCatalogFilterForm,
    alias_filter_q,
    country_filter_q,
    country_flag_for,
)
from .models import Brand, Car, CarModel, Category, Dealer, RepairShop


def list_cars(request):
    cars = (
        Car.objects.filter(is_published=True)
        .select_related("model__brand", "trim", "technical_spec", "dimensions")
        .prefetch_related("photos")
    )

    get_data = request.GET.copy()
    # Legacy bookmarks: ?brand=Toyota → resolve to brand pk for the form.
    brand_raw = (get_data.get("brand") or "").strip()
    if brand_raw and not brand_raw.isdigit():
        legacy = Brand.objects.filter(name__iexact=brand_raw).first()
        if legacy:
            get_data["brand"] = str(legacy.pk)

    if request.GET:
        form = CarCatalogFilterForm(get_data)
    else:
        form = CarCatalogFilterForm(initial={"sort": "yearDesc"})

    filters_active = False
    sort_key = "yearDesc"
    selected_country = ""

    if form.is_bound and form.is_valid():
        data = form.cleaned_data
        q = (data.get("q") or "").strip()
        brand = data.get("brand")
        category = data.get("category")
        model = data.get("model")
        trim = data.get("trim")
        manufacturer = (data.get("manufacturer") or "").strip()
        fuel = data.get("fuel") or ""
        transmission = data.get("transmission") or ""
        drivetrain = data.get("drivetrain") or ""
        seats = data.get("seats") or ""
        year_min = data.get("year_min")
        year_max = data.get("year_max")
        hp_min = data.get("hp_min")
        hp_max = data.get("hp_max")
        sort_key = data.get("sort") or "yearDesc"
        selected_country = data.get("country") or ""

        country_q = country_filter_q(selected_country)
        if country_q is not None:
            cars = cars.filter(country_q)
            filters_active = True

        if q:
            cars = cars.filter(
                Q(model__name__icontains=q)
                | Q(trim__name__icontains=q)
                | Q(model__brand__name__icontains=q)
                | Q(fuel_type__icontains=q)
                | Q(model__brand__country__icontains=q)
                | Q(model__brand__manufacturer__icontains=q)
                | Q(technical_spec__transmission__icontains=q)
                | Q(technical_spec__drivetrain__icontains=q)
            )
            filters_active = True

        if brand:
            cars = cars.filter(model__brand=brand)
            filters_active = True

        if category:
            cars = cars.filter(categories=category).distinct()
            filters_active = True

        if model and (not brand or model.brand_id == brand.id):
            cars = cars.filter(model=model)
            filters_active = True

        if trim and (not model or trim.car_model_id == model.id):
            cars = cars.filter(trim=trim)
            filters_active = True

        if manufacturer:
            cars = cars.filter(model__brand__manufacturer=manufacturer)
            filters_active = True

        if fuel in FUEL_ALIASES:
            fuel_q = Q()
            for alias in FUEL_ALIASES[fuel]:
                fuel_q |= Q(fuel_type__iexact=alias)
            cars = cars.filter(fuel_q)
            filters_active = True

        transmission_q = alias_filter_q(
            "technical_spec__transmission", transmission, TRANSMISSION_ALIASES
        )
        if transmission_q is not None:
            cars = cars.filter(transmission_q)
            filters_active = True

        drivetrain_q = alias_filter_q(
            "technical_spec__drivetrain", drivetrain, DRIVETRAIN_ALIASES
        )
        if drivetrain_q is not None:
            cars = cars.filter(drivetrain_q)
            filters_active = True

        if seats == "7":
            cars = cars.filter(dimensions__seats__gte=7)
            filters_active = True
        elif seats.isdigit():
            cars = cars.filter(dimensions__seats=int(seats))
            filters_active = True

        if year_min is not None:
            cars = cars.filter(year__gte=year_min)
            filters_active = True

        if year_max is not None:
            cars = cars.filter(year__lte=year_max)
            filters_active = True

        if hp_min is not None:
            cars = cars.filter(horsepower__gte=hp_min)
            filters_active = True

        if hp_max is not None:
            cars = cars.filter(horsepower__lte=hp_max)
            filters_active = True
    elif brand_raw:
        if brand_raw.isdigit():
            cars = cars.filter(model__brand_id=int(brand_raw))
        else:
            cars = cars.filter(model__brand__name__iexact=brand_raw)
        filters_active = True

    cars = cars.order_by(*SORT_ORDERING.get(sort_key, SORT_ORDERING["yearDesc"]))

    # Attach display flags for cards (avoid template logic).
    car_list = list(cars)
    for car in car_list:
        car.country_flag = country_flag_for(car.model.brand.country)

    return render(
        request,
        "cars/list.html",
        {
            "cars": car_list,
            "form": form,
            "filters_active": filters_active,
            "result_count": len(car_list),
            "country_filters": COUNTRY_FILTERS,
            "selected_country": selected_country
            or (form["country"].value() if form.is_bound else ""),
        },
    )


def brand_list(request):
    brands = Brand.objects.annotate(
        model_count=Count("models", distinct=True),
        car_count=Count(
            "models__cars",
            filter=Q(models__cars__is_published=True),
            distinct=True,
        ),
    ).order_by("name")
    brand_list_items = list(brands)
    for brand in brand_list_items:
        brand.country_flag = country_flag_for(brand.country)

    # Group by country filter order (Iran first), then unknown.
    country_order = {item["key"]: i for i, item in enumerate(COUNTRY_FILTERS)}
    groups: dict[str, dict] = {}
    for brand in brand_list_items:
        flag = brand.country_flag
        key = next(
            (item["key"] for item in COUNTRY_FILTERS if item["flag"] == flag),
            "other",
        )
        if key not in groups:
            meta = next((item for item in COUNTRY_FILTERS if item["key"] == key), None)
            groups[key] = {
                "key": key,
                "label": meta["label"] if meta else brand.country or "",
                "flag": flag,
                "brands": [],
                "sort": country_order.get(key, 999),
            }
        groups[key]["brands"].append(brand)

    brand_groups = sorted(groups.values(), key=lambda g: (g["sort"], str(g["label"])))

    return render(
        request,
        "cars/brands.html",
        {
            "brands": brand_list_items,
            "brand_groups": brand_groups,
            "brand_count": len(brand_list_items),
        },
    )


def brand_detail(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    models = (
        CarModel.objects.filter(brand=brand)
        .annotate(
            car_count=Count("cars", filter=Q(cars__is_published=True), distinct=True)
        )
        .prefetch_related("trims")
        .order_by("name")
    )
    cars = (
        Car.objects.filter(is_published=True, model__brand=brand)
        .select_related("model", "trim")
        .prefetch_related("photos")
        .order_by("-year", "model__name")[:24]
    )
    return render(
        request,
        "cars/brand_detail.html",
        {
            "brand": brand,
            "country_flag": country_flag_for(brand.country),
            "models": models,
            "cars": cars,
        },
    )


def category_list(request):
    categories = Category.objects.annotate(
        model_count=Count("car_models", distinct=True),
        car_count=Count(
            "cars",
            filter=Q(cars__is_published=True),
            distinct=True,
        ),
    ).order_by("sort_order", "name")
    category_list_items = list(categories)
    return render(
        request,
        "cars/categories.html",
        {
            "categories": category_list_items,
            "category_count": len(category_list_items),
        },
    )


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    models = (
        CarModel.objects.filter(categories=category)
        .select_related("brand")
        .annotate(
            car_count=Count("cars", filter=Q(cars__is_published=True), distinct=True)
        )
        .prefetch_related("trims")
        .order_by("brand__name", "name")
    )
    cars = (
        Car.objects.filter(is_published=True, categories=category)
        .select_related("model__brand", "trim")
        .prefetch_related("photos")
        .order_by("-year", "model__brand__name", "model__name")[:24]
    )
    return render(
        request,
        "cars/category_detail.html",
        {
            "category": category,
            "models": models,
            "cars": cars,
        },
    )


def _car_gallery_images(car):
    """Cover first, then gallery photos (deduped by storage name)."""
    items = []
    seen = set()
    if car.cover_image:
        items.append({"url": car.cover_image.url, "caption": ""})
        seen.add(car.cover_image.name)
    for photo in car.photos.all():
        name = getattr(photo.image, "name", "") or ""
        if name and name in seen:
            continue
        if name:
            seen.add(name)
        items.append(
            {
                "url": photo.image.url,
                "caption": photo.caption or "",
            }
        )
    return items


def detail(request, pk):
    car = get_object_or_404(
        Car.objects.select_related(
            "model__brand",
            "trim",
            "technical_spec",
            "dimensions",
            "suspension",
            "brakes",
            "wheels",
            "cabin",
            "multimedia",
            "market_info",
        ).prefetch_related(
            "photos",
            "features",
            "maintenance_items",
            "fluids",
            "tires",
            "batteries",
            "service_schedule",
            "parts",
            "prices",
            "common_failures",
            "categories",
            "model__obd_codes",
        ),
        pk=pk,
        is_published=True,
    )
    brand = car.model.brand
    dealers = Dealer.objects.filter(
        is_published=True, brands=brand
    ).distinct()
    repair_shops = RepairShop.objects.filter(
        is_published=True, brands=brand
    ).distinct()
    gallery_images = _car_gallery_images(car)
    gallery_preview_limit = 5
    return render(
        request,
        "cars/detail.html",
        {
            "car": car,
            "dealers": dealers,
            "repair_shops": repair_shops,
            "gallery_images": gallery_images,
            "gallery_preview": gallery_images[:gallery_preview_limit],
            "gallery_preview_limit": gallery_preview_limit,
            "gallery_extra_count": max(
                0, len(gallery_images) - gallery_preview_limit
            ),
        },
    )


def places_index(request):
    dealers = Dealer.objects.filter(is_published=True).prefetch_related("brands")
    shops = RepairShop.objects.filter(is_published=True).prefetch_related("brands")
    return render(
        request,
        "places/index.html",
        {
            "dealers": dealers,
            "repair_shops": shops,
        },
    )


def dealer_detail(request, pk):
    dealer = get_object_or_404(
        Dealer.objects.prefetch_related("brands"),
        pk=pk,
        is_published=True,
    )
    return render(request, "places/dealer_detail.html", {"dealer": dealer})


def repair_shop_detail(request, pk):
    shop = get_object_or_404(
        RepairShop.objects.prefetch_related("brands"),
        pk=pk,
        is_published=True,
    )
    return render(request, "places/repair_shop_detail.html", {"shop": shop})
