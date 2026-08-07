from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from apps.cars.models import (
    BatterySpec,
    Brand,
    Car,
    CarModel,
    CarPhoto,
    CarPrice,
    Dealer,
    Dimensions,
    Feature,
    FluidSpec,
    MaintenanceItem,
    OBDCode,
    Part,
    RepairShop,
    ServiceScheduleItem,
    TechnicalSpec,
    TireSpec,
    Trim,
)
from apps.emergency.models import EmergencyService, RequestStatus
from apps.marketplace.models import Listing, ListingStatus
from apps.pricing.models import PriceReference
from apps.stories.models import Story
from apps.youtube.models import YoutubeVideo

PUBLISHED_CHOICES = [
    ("", _("All")),
    ("1", _("Published")),
    ("0", _("Draft")),
]


class PanelEmergencySearchForm(forms.Form):
    q = forms.CharField(required=False, label=_("Search"))
    status = forms.ChoiceField(
        required=False,
        label=_("Status"),
        choices=[("", _("All statuses"))] + list(RequestStatus.choices),
    )
    service = forms.ModelChoiceField(
        required=False,
        queryset=EmergencyService.objects.all(),
        empty_label=_("All services"),
        label=_("Service"),
    )


class EmergencyServiceForm(forms.ModelForm):
    class Meta:
        model = EmergencyService
        fields = (
            "name_fa",
            "name_en",
            "name_ar",
            "description_fa",
            "description_en",
            "description_ar",
            "coverage_notes_fa",
            "coverage_notes_en",
            "coverage_notes_ar",
            "cover_image",
            "is_active",
        )
        widgets = {
            "description_fa": forms.Textarea(attrs={"rows": 3}),
            "description_en": forms.Textarea(attrs={"rows": 3}),
            "description_ar": forms.Textarea(attrs={"rows": 3}),
            "coverage_notes_fa": forms.Textarea(attrs={"rows": 3}),
            "coverage_notes_en": forms.Textarea(attrs={"rows": 3}),
            "coverage_notes_ar": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in (
            "name_fa",
            "name_en",
            "name_ar",
            "description_fa",
            "description_en",
            "description_ar",
            "coverage_notes_fa",
            "coverage_notes_en",
            "coverage_notes_ar",
        ):
            self.fields[name].required = True


class PanelContentSearchForm(forms.Form):
    q = forms.CharField(required=False, label=_("Search"))
    published = forms.ChoiceField(
        required=False,
        label=_("Published"),
        choices=PUBLISHED_CHOICES,
    )


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ("name", "manufacturer", "country")


class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = ("brand", "name")


class TrimForm(forms.ModelForm):
    class Meta:
        model = Trim
        fields = ("car_model", "name")


class OBDCodeForm(forms.ModelForm):
    class Meta:
        model = OBDCode
        fields = ("car_model", "code", "title", "description", "severity")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class DealerForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = (
            "name",
            "city",
            "address",
            "phone",
            "website",
            "brands",
            "is_published",
        )
        widgets = {
            "address": forms.Textarea(attrs={"rows": 2}),
            "brands": forms.CheckboxSelectMultiple,
        }


class RepairShopForm(forms.ModelForm):
    class Meta:
        model = RepairShop
        fields = (
            "name",
            "city",
            "address",
            "phone",
            "website",
            "brands",
            "is_published",
        )
        widgets = {
            "address": forms.Textarea(attrs={"rows": 2}),
            "brands": forms.CheckboxSelectMultiple,
        }


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = (
            "model",
            "year",
            "trim",
            "horsepower",
            "fuel_type",
            "description",
            "cover_image",
            "is_published",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["trim"].queryset = Trim.objects.select_related(
            "car_model__brand"
        ).order_by("car_model__brand__name", "car_model__name", "name")
        model = None
        if self.data.get("model"):
            try:
                model = CarModel.objects.get(pk=self.data.get("model"))
            except (CarModel.DoesNotExist, ValueError, TypeError):
                model = None
        elif self.instance and self.instance.pk and self.instance.model_id:
            model = self.instance.model
        if model is not None:
            self.fields["trim"].queryset = Trim.objects.filter(car_model=model)

    def clean(self):
        cleaned = super().clean()
        model = cleaned.get("model")
        trim = cleaned.get("trim")
        if model and trim and trim.car_model_id != model.id:
            self.add_error("trim", _("Trim must belong to the selected model."))
        return cleaned


class TechnicalSpecForm(forms.ModelForm):
    class Meta:
        model = TechnicalSpec
        exclude = ("car",)
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 2}),
        }


class DimensionsForm(forms.ModelForm):
    class Meta:
        model = Dimensions
        exclude = ("car",)


CarPhotoFormSet = inlineformset_factory(
    Car,
    CarPhoto,
    fields=("image", "caption", "sort_order"),
    extra=1,
    can_delete=True,
)

FeatureFormSet = inlineformset_factory(
    Car,
    Feature,
    fields=("category", "name", "value"),
    extra=0,
    can_delete=True,
)

MaintenanceItemFormSet = inlineformset_factory(
    Car,
    MaintenanceItem,
    fields=(
        "title",
        "interval_km",
        "interval_months",
        "description",
        "estimated_cost",
    ),
    extra=0,
    can_delete=True,
    widgets={"description": forms.Textarea(attrs={"rows": 2})},
)

FluidSpecFormSet = inlineformset_factory(
    Car,
    FluidSpec,
    fields=("fluid_type", "specification", "capacity", "notes"),
    extra=0,
    can_delete=True,
    widgets={"notes": forms.Textarea(attrs={"rows": 2})},
)

TireSpecFormSet = inlineformset_factory(
    Car,
    TireSpec,
    fields=("position", "size", "pressure_psi", "load_index", "speed_rating"),
    extra=0,
    can_delete=True,
)

BatterySpecFormSet = inlineformset_factory(
    Car,
    BatterySpec,
    fields=("group_size", "voltage", "cca", "chemistry", "notes"),
    extra=0,
    can_delete=True,
    widgets={"notes": forms.Textarea(attrs={"rows": 2})},
)

ServiceScheduleFormSet = inlineformset_factory(
    Car,
    ServiceScheduleItem,
    fields=("mileage_km", "months", "tasks", "sort_order"),
    extra=0,
    can_delete=True,
    widgets={"tasks": forms.Textarea(attrs={"rows": 2})},
)

PartFormSet = inlineformset_factory(
    Car,
    Part,
    fields=("name", "oem_number", "category", "notes"),
    extra=0,
    can_delete=True,
    widgets={"notes": forms.Textarea(attrs={"rows": 2})},
)

CarPriceFormSet = inlineformset_factory(
    Car,
    CarPrice,
    fields=("label", "amount", "currency", "source", "notes", "recorded_at"),
    extra=0,
    can_delete=True,
    widgets={
        "notes": forms.Textarea(attrs={"rows": 2}),
        "recorded_at": forms.DateInput(attrs={"type": "date"}),
    },
)


FORMSET_FACTORIES = {
    "photos": CarPhotoFormSet,
    "features": FeatureFormSet,
    "maintenance": MaintenanceItemFormSet,
    "fluids": FluidSpecFormSet,
    "tires": TireSpecFormSet,
    "batteries": BatterySpecFormSet,
    "service": ServiceScheduleFormSet,
    "parts": PartFormSet,
    "prices": CarPriceFormSet,
}


def _form_has_values(form):
    if not form.is_valid():
        return False
    for name, value in form.cleaned_data.items():
        if name == "car":
            continue
        if value not in (None, "", []):
            return True
    return False


def build_car_related_forms(data=None, files=None, instance=None):
    """Return (spec_form, dims_form, formsets_dict) for a Car create/edit view."""
    car = instance if instance is not None else Car()
    spec_instance = None
    dims_instance = None
    if instance is not None and instance.pk:
        spec_instance = TechnicalSpec.objects.filter(car=instance).first()
        dims_instance = Dimensions.objects.filter(car=instance).first()

    if data is not None:
        spec_form = TechnicalSpecForm(data, instance=spec_instance, prefix="spec")
        dims_form = DimensionsForm(data, instance=dims_instance, prefix="dims")
        formsets = {
            key: factory(data, files, instance=car, prefix=key)
            for key, factory in FORMSET_FACTORIES.items()
        }
    else:
        spec_form = TechnicalSpecForm(instance=spec_instance, prefix="spec")
        dims_form = DimensionsForm(instance=dims_instance, prefix="dims")
        formsets = {
            key: factory(instance=car, prefix=key)
            for key, factory in FORMSET_FACTORIES.items()
        }
    return spec_form, dims_form, formsets


def car_related_forms_valid(spec_form, dims_form, formsets):
    ok = spec_form.is_valid() and dims_form.is_valid()
    for fs in formsets.values():
        ok = fs.is_valid() and ok
    return ok


def save_car_related(car, spec_form, dims_form, formsets):
    if _form_has_values(spec_form) or (
        spec_form.instance and spec_form.instance.pk
    ):
        spec = spec_form.save(commit=False)
        spec.car = car
        spec.save()

    if _form_has_values(dims_form) or (
        dims_form.instance and dims_form.instance.pk
    ):
        dims = dims_form.save(commit=False)
        dims.car = car
        dims.save()

    for fs in formsets.values():
        fs.instance = car
        fs.save()


class YoutubeVideoForm(forms.ModelForm):
    class Meta:
        model = YoutubeVideo
        fields = (
            "title",
            "youtube_id",
            "description",
            "cover_image",
            "published_at",
            "is_published",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "published_at": forms.DateInput(attrs={"type": "date"}),
        }


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = (
            "title_fa",
            "title_en",
            "title_ar",
            "excerpt_fa",
            "excerpt_en",
            "excerpt_ar",
            "body_fa",
            "body_en",
            "body_ar",
            "slug",
            "cover_image",
            "author",
            "is_published",
            "published_at",
        )
        widgets = {
            "excerpt_fa": forms.TextInput(),
            "excerpt_en": forms.TextInput(),
            "excerpt_ar": forms.TextInput(),
            "body_fa": forms.Textarea(attrs={"rows": 8}),
            "body_en": forms.Textarea(attrs={"rows": 8}),
            "body_ar": forms.Textarea(attrs={"rows": 8}),
            "published_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in (
            "title_fa",
            "title_en",
            "title_ar",
            "body_fa",
            "body_en",
            "body_ar",
        ):
            self.fields[name].required = True
        self.fields["author"].required = False
        self.fields["slug"].required = False


STATUS_CHOICES = [("", _("All statuses"))] + list(ListingStatus.choices)


class PanelListingSearchForm(forms.Form):
    q = forms.CharField(required=False, label=_("Search"))
    status = forms.ChoiceField(
        required=False,
        label=_("Status"),
        choices=STATUS_CHOICES,
    )


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = (
            "seller",
            "title_fa",
            "title_en",
            "title_ar",
            "description_fa",
            "description_en",
            "description_ar",
            "cover_image",
            "price",
            "currency",
            "car_model",
            "trim",
            "year",
            "mileage_km",
            "city",
            "status",
        )
        widgets = {
            "description_fa": forms.Textarea(attrs={"rows": 4}),
            "description_en": forms.Textarea(attrs={"rows": 4}),
            "description_ar": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["car_model"].queryset = CarModel.objects.select_related(
            "brand"
        ).order_by("brand__name", "name")
        self.fields["seller"].required = True


class PriceReferenceForm(forms.ModelForm):
    class Meta:
        model = PriceReference
        fields = (
            "title_fa",
            "title_en",
            "title_ar",
            "category_fa",
            "category_en",
            "category_ar",
            "amount",
            "currency",
            "notes_fa",
            "notes_en",
            "notes_ar",
            "source_fa",
            "source_en",
            "source_ar",
            "cover_image",
            "is_published",
        )
        widgets = {
            "notes_fa": forms.Textarea(attrs={"rows": 3}),
            "notes_en": forms.Textarea(attrs={"rows": 3}),
            "notes_ar": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("title_fa", "title_en", "title_ar"):
            self.fields[name].required = True

