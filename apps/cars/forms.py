from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .models import Brand, CarModel, Category, Trim

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

TRANSMISSION_CHOICES = [
    ("", _("All transmissions")),
    ("automatic", _("Automatic")),
    ("manual", _("Manual")),
    ("cvt", _("CVT")),
]

TRANSMISSION_ALIASES = {
    "automatic": (
        "automatic",
        "auto",
        "at",
        "a/t",
        "tiptronic",
        "dsg",
        "dct",
        "dual clutch",
        "dual-clutch",
        "اتوماتیک",
        "اتومات",
    ),
    "manual": ("manual", "mt", "m/t", "stick", "دستی", "گیربکس دستی"),
    "cvt": ("cvt", "e-cvt", "ecvt"),
}

DRIVETRAIN_CHOICES = [
    ("", _("All drivetrains")),
    ("fwd", _("FWD")),
    ("rwd", _("RWD")),
    ("awd", _("AWD / 4WD")),
]

DRIVETRAIN_ALIASES = {
    "fwd": ("fwd", "front", "front-wheel", "2wd", "جلو"),
    "rwd": ("rwd", "rear", "rear-wheel", "عقب"),
    "awd": (
        "awd",
        "4wd",
        "4x4",
        "all-wheel",
        "all wheel",
        "xdrive",
        "quattro",
        "4matic",
        "چهار چرخ",
        "دو دیفرانسیل",
    ),
}

SEATS_CHOICES = [
    ("", _("Any seats")),
    ("2", _("2 seats")),
    ("4", _("4 seats")),
    ("5", _("5 seats")),
    ("7", _("7+ seats")),
]

# Market / origin country filter (Brand.country free text → aliases).
# Ordered by hub relevance: Iran first, then major active auto markets.
COUNTRY_FILTERS = (
    {
        "key": "iran",
        "label": _("Iran"),
        "flag": "🇮🇷",
        "aliases": ("iran", "ir", "irn", "ایران", "جمهوری اسلامی ایران"),
    },
    {
        "key": "japan",
        "label": _("Japan"),
        "flag": "🇯🇵",
        "aliases": ("japan", "jp", "jpn", "ژاپن", "日本"),
    },
    {
        "key": "germany",
        "label": _("Germany"),
        "flag": "🇩🇪",
        "aliases": ("germany", "de", "deu", "deutschland", "آلمان", "المانيا"),
    },
    {
        "key": "korea",
        "label": _("South Korea"),
        "flag": "🇰🇷",
        "aliases": (
            "south korea",
            "korea",
            "kr",
            "kor",
            "republic of korea",
            "کره",
            "کره جنوبی",
            "كوريا",
            "كوريا الجنوبية",
        ),
    },
    {
        "key": "usa",
        "label": _("USA"),
        "flag": "🇺🇸",
        "aliases": (
            "usa",
            "us",
            "u.s.",
            "u.s.a.",
            "united states",
            "united states of america",
            "america",
            "آمریکا",
            "ایالات متحده",
        ),
    },
    {
        "key": "france",
        "label": _("France"),
        "flag": "🇫🇷",
        "aliases": ("france", "fr", "fra", "فرانسه", "فرنسا"),
    },
    {
        "key": "italy",
        "label": _("Italy"),
        "flag": "🇮🇹",
        "aliases": ("italy", "it", "ita", "ایتالیا", "إيطاليا"),
    },
    {
        "key": "china",
        "label": _("China"),
        "flag": "🇨🇳",
        "aliases": ("china", "cn", "chn", "prc", "چین", "الصين"),
    },
    {
        "key": "uk",
        "label": _("United Kingdom"),
        "flag": "🇬🇧",
        "aliases": (
            "united kingdom",
            "uk",
            "gb",
            "gbr",
            "great britain",
            "england",
            "بریتانیا",
            "انگلستان",
            "المملكة المتحدة",
        ),
    },
)

COUNTRY_CHOICES = [("", _("All countries"))] + [
    (item["key"], item["label"]) for item in COUNTRY_FILTERS
]

COUNTRY_BY_KEY = {item["key"]: item for item in COUNTRY_FILTERS}


def brands_for_country(key: str):
    """Brand queryset limited to a country filter key (or all brands)."""
    brands = Brand.objects.all()
    meta = COUNTRY_BY_KEY.get(key or "")
    if not meta:
        return brands
    brand_q = Q()
    for alias in meta["aliases"]:
        brand_q |= Q(country__iexact=alias)
    brand_q |= Q(country__icontains=meta["aliases"][0])
    return brands.filter(brand_q)


def country_filter_q(key: str) -> Q | None:
    """Build a Car queryset filter for Brand.country."""
    meta = COUNTRY_BY_KEY.get(key or "")
    if not meta:
        return None
    q = Q()
    for alias in meta["aliases"]:
        q |= Q(model__brand__country__iexact=alias)
    q |= Q(model__brand__country__icontains=meta["aliases"][0])
    return q


def country_flag_for(value: str) -> str:
    """Return an emoji flag for a Brand.country value, or empty."""
    raw = (value or "").strip().lower()
    if not raw:
        return ""
    for item in COUNTRY_FILTERS:
        aliases = item["aliases"]
        if raw in aliases:
            return item["flag"]
        if any(len(a) > 2 and a in raw for a in aliases):
            return item["flag"]
    return ""


def alias_filter_q(field: str, key: str, aliases_map: dict) -> Q | None:
    aliases = aliases_map.get(key or "")
    if not aliases:
        return None
    q = Q()
    for alias in aliases:
        q |= Q(**{f"{field}__iexact": alias})
        if len(alias) > 2:
            q |= Q(**{f"{field}__icontains": alias})
    return q


SORT_CHOICES = [
    ("yearDesc", _("Newest first")),
    ("yearAsc", _("Oldest first")),
    ("powerDesc", _("Power (high → low)")),
    ("powerAsc", _("Power (low → high)")),
    ("nameAsc", _("Model A–Z")),
    ("brandAsc", _("Brand A–Z")),
]

SORT_ORDERING = {
    "yearDesc": ("-year", "model__brand__name", "model__name"),
    "yearAsc": ("year", "model__brand__name", "model__name"),
    "powerDesc": ("-horsepower", "-year", "model__brand__name"),
    "powerAsc": ("horsepower", "-year", "model__brand__name"),
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
    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        required=False,
        label=_("Country"),
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        empty_label=_("All brands"),
        label=_("Brand"),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label=_("All categories"),
        label=_("Category"),
    )
    model = forms.ModelChoiceField(
        queryset=CarModel.objects.none(),
        required=False,
        empty_label=_("All models"),
        label=_("Model"),
    )
    trim = forms.ModelChoiceField(
        queryset=Trim.objects.none(),
        required=False,
        empty_label=_("All trims"),
        label=_("Trim"),
    )
    manufacturer = forms.ChoiceField(
        choices=[("", _("All manufacturers"))],
        required=False,
        label=_("Manufacturer"),
    )
    fuel = forms.ChoiceField(
        choices=FUEL_CHOICES,
        required=False,
        label=_("Fuel"),
    )
    transmission = forms.ChoiceField(
        choices=TRANSMISSION_CHOICES,
        required=False,
        label=_("Transmission"),
    )
    drivetrain = forms.ChoiceField(
        choices=DRIVETRAIN_CHOICES,
        required=False,
        label=_("Drivetrain"),
    )
    seats = forms.ChoiceField(
        choices=SEATS_CHOICES,
        required=False,
        label=_("Seats"),
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
    hp_min = forms.IntegerField(
        required=False,
        label=_("HP from"),
        min_value=1,
        max_value=2000,
        widget=forms.NumberInput(
            attrs={
                "placeholder": _("Min"),
                "inputmode": "numeric",
                "aria-label": _("Horsepower from"),
            }
        ),
    )
    hp_max = forms.IntegerField(
        required=False,
        label=_("HP to"),
        min_value=1,
        max_value=2000,
        widget=forms.NumberInput(
            attrs={
                "placeholder": _("Max"),
                "inputmode": "numeric",
                "aria-label": _("Horsepower to"),
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
        model = None
        country_key = ""
        if self.is_bound:
            brand_raw = self.data.get("brand")
            if brand_raw and str(brand_raw).isdigit():
                brand = Brand.objects.filter(pk=int(brand_raw)).first()
            model_raw = self.data.get("model")
            if model_raw and str(model_raw).isdigit():
                model = CarModel.objects.filter(pk=int(model_raw)).first()
            country_key = (self.data.get("country") or "").strip()
        else:
            brand = self.initial.get("brand")
            if isinstance(brand, int):
                brand = Brand.objects.filter(pk=brand).first()
            model = self.initial.get("model")
            if isinstance(model, int):
                model = CarModel.objects.filter(pk=model).first()
            country_key = (self.initial.get("country") or "").strip()

        brands = brands_for_country(country_key)
        self.fields["brand"].queryset = brands

        manufacturers = (
            brands.exclude(manufacturer="")
            .order_by("manufacturer")
            .values_list("manufacturer", flat=True)
            .distinct()
        )
        self.fields["manufacturer"].choices = [("", _("All manufacturers"))] + [
            (name, name) for name in manufacturers
        ]

        if brand and brands.filter(pk=brand.pk).exists():
            models_qs = CarModel.objects.filter(brand=brand).select_related("brand")
        elif country_key in COUNTRY_BY_KEY:
            models_qs = CarModel.objects.filter(brand__in=brands).select_related("brand")
        else:
            models_qs = CarModel.objects.select_related("brand").all()
        self.fields["model"].queryset = models_qs

        trims = Trim.objects.select_related("car_model__brand")
        if model and models_qs.filter(pk=model.pk).exists():
            trims = trims.filter(car_model=model)
        elif brand and brands.filter(pk=brand.pk).exists():
            trims = trims.filter(car_model__brand=brand)
        elif country_key in COUNTRY_BY_KEY:
            trims = trims.filter(car_model__brand__in=brands)
        self.fields["trim"].queryset = trims.order_by(
            "car_model__brand__name", "car_model__name", "name"
        )
