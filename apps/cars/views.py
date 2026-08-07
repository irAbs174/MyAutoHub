import json
import time
from pathlib import Path

from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .forms import FUEL_ALIASES, SORT_ORDERING, CarCatalogFilterForm
from .models import Brand, Car

# #region agent log
_DEBUG_LOG = Path("/home/unique/Documents/projects/dev/MyAutoHub/.cursor/debug-f3274c.log")


def _agent_log(hypothesis_id, location, message, data, run_id="pre-fix"):
    payload = {
        "sessionId": "f3274c",
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    with _DEBUG_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


# #endregion


def list_cars(request):
    cars = (
        Car.objects.filter(is_published=True)
        .select_related("model__brand")
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
                | Q(trim__icontains=q)
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

    # #region agent log
    field_meta = []
    for name in ("q", "brand", "model", "fuel", "year_min", "year_max", "sort"):
        field = form[name]
        html = str(field)
        field_meta.append(
            {
                "name": name,
                "widget": field.field.widget.__class__.__name__,
                "has_class_attr": " class=" in html,
                "tag_select": html.lstrip().startswith("<select"),
                "tag_input": html.lstrip().startswith("<input"),
                "html_snip": html[:180],
            }
        )
    _agent_log(
        "B",
        "cars/views.py:list_cars",
        "filter_widget_html",
        {
            "bound": form.is_bound,
            "valid": form.is_bound and form.is_valid(),
            "fields": field_meta,
        },
    )
    _agent_log(
        "A",
        "cars/views.py:list_cars",
        "filter_panel_classes",
        {
            "panel_classes": "panel filter-panel cars-filter-panel",
            "uses_compact_overrides": True,
            "standard_filter_panel_padding": "1.1rem 1.25rem",
            "compact_padding": "0.65rem 0.85rem",
            "compact_removes_shadow": True,
            "compact_label_uppercase": True,
        },
    )
    # #endregion

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
        Car.objects.select_related("model__brand").prefetch_related("photos"),
        pk=pk,
        is_published=True,
    )
    return render(request, "cars/detail.html", {"car": car})
