from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Brand, CarModel

FUEL_CHOICES = [
    ("", _("All fuels")),
    ("petrol", _("Petrol")),
    ("hybrid", _("Hybrid")),
    ("diesel", _("Diesel")),
    ("electric", _("Electric")),
]

# Maps filter keys to stored fuel_type values (seed / panel free text).
FUEL_ALIASES = {
    "petrol": ("petrol", "gasoline", "gas"),
    "hybrid": ("hybrid",),
    "diesel": ("diesel",),
    "electric": ("electric", "ev"),
}

SORT_CHOICES = [
    ("yearDesc", _("Newest first")),
    ("yearAsc", _("Oldest first")),
    ("powerDesc", _("Power (high → low)")),
    ("nameAsc", _("Model A–Z")),
    ("brandAsc", _("Brand A–Z")),
]

SORT_ORDERING = {
    "yearDesc": ("-year", "model__brand__name", "model__name"),
    "yearAsc": ("year", "model__brand__name", "model__name"),
    "powerDesc": ("-horsepower", "-year", "model__brand__name"),
    "nameAsc": ("model__name", "model__brand__name", "-year"),
    "brandAsc": ("model__brand__name", "model__name", "-year"),
}


class CarCatalogFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label=_("Search"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Brand, model, trim…"), "autocomplete": "off"}
        ),
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        empty_label=_("All brands"),
        label=_("Brand"),
    )
    model = forms.ModelChoiceField(
        queryset=CarModel.objects.none(),
        required=False,
        empty_label=_("All models"),
        label=_("Model"),
    )
    fuel = forms.ChoiceField(
        choices=FUEL_CHOICES,
        required=False,
        label=_("Fuel"),
    )
    year_min = forms.IntegerField(
        required=False,
        label=_("Year from"),
        min_value=1950,
        max_value=2100,
        widget=forms.NumberInput(
            attrs={
                "placeholder": _("From"),
                "inputmode": "numeric",
                "aria-label": _("Year from"),
            }
        ),
    )
    year_max = forms.IntegerField(
        required=False,
        label=_("Year to"),
        min_value=1950,
        max_value=2100,
        widget=forms.NumberInput(
            attrs={
                "placeholder": _("To"),
                "inputmode": "numeric",
                "aria-label": _("Year to"),
            }
        ),
    )
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial="yearDesc",
        label=_("Sort by"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        brand = None
        if self.is_bound:
            brand_raw = self.data.get("brand")
            if brand_raw and str(brand_raw).isdigit():
                brand = Brand.objects.filter(pk=int(brand_raw)).first()
        else:
            brand = self.initial.get("brand")
            if isinstance(brand, int):
                brand = Brand.objects.filter(pk=brand).first()

        if brand:
            self.fields["model"].queryset = CarModel.objects.filter(brand=brand).select_related(
                "brand"
            )
        else:
            self.fields["model"].queryset = CarModel.objects.select_related("brand").all()
