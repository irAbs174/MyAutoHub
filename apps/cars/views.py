from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .forms import FUEL_ALIASES, SORT_ORDERING, CarCatalogFilterForm
from .models import Brand, Car, Dealer, RepairShop


def list_cars(request):
    cars = (
        Car.objects.filter(is_published=True)
        .select_related("model__brand", "trim")
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

    if form.is_bound and form.is_valid():
        data = form.cleaned_data
        q = (data.get("q") or "").strip()
        brand = data.get("brand")
        model = data.get("model")
        fuel = data.get("fuel") or ""
        year_min = data.get("year_min")
        year_max = data.get("year_max")
        sort_key = data.get("sort") or "yearDesc"

        if q:
            cars = cars.filter(
                Q(model__name__icontains=q)
                | Q(trim__name__icontains=q)
                | Q(model__brand__name__icontains=q)
                | Q(fuel_type__icontains=q)
            )
            filters_active = True

        if brand:
            cars = cars.filter(model__brand=brand)
            filters_active = True

        if model and (not brand or model.brand_id == brand.id):
            cars = cars.filter(model=model)
            filters_active = True

        if fuel in FUEL_ALIASES:
            fuel_q = Q()
            for alias in FUEL_ALIASES[fuel]:
                fuel_q |= Q(fuel_type__iexact=alias)
            cars = cars.filter(fuel_q)
            filters_active = True

        if year_min is not None:
            cars = cars.filter(year__gte=year_min)
            filters_active = True

        if year_max is not None:
            cars = cars.filter(year__lte=year_max)
            filters_active = True
    elif brand_raw:
        if brand_raw.isdigit():
            cars = cars.filter(model__brand_id=int(brand_raw))
        else:
            cars = cars.filter(model__brand__name__iexact=brand_raw)
        filters_active = True

    cars = cars.order_by(*SORT_ORDERING.get(sort_key, SORT_ORDERING["yearDesc"]))

    return render(
        request,
        "cars/list.html",
        {
            "cars": cars,
            "form": form,
            "filters_active": filters_active,
            "result_count": cars.count(),
        },
    )


def detail(request, pk):
    car = get_object_or_404(
        Car.objects.select_related(
            "model__brand",
            "trim",
            "technical_spec",
            "dimensions",
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
    return render(
        request,
        "cars/detail.html",
        {
            "car": car,
            "dealers": dealers,
            "repair_shops": repair_shops,
        },
    )
