from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from apps.cars.models import (
    BatterySpec,
    BrakeSpec,
    Brand,
    CabinSpec,
    Car,
    CarModel,
    CarPhoto,
    CarPrice,
    Category,
    CommonFailure,
    Dealer,
    Dimensions,
    Feature,
    FluidSpec,
    MaintenanceItem,
    MarketInfo,
    MultimediaSpec,
    OBDCode,
    Part,
    RepairShop,
    ServiceScheduleItem,
    SuspensionSpec,
    TechnicalSpec,
    TireSpec,
    Trim,
    WheelSpec,
)
from apps.panel.car_field_labels import (
    BATTERY_LABELS,
    BRAKE_LABELS,
    CABIN_LABELS,
    CAR_LABELS,
    DIMENSIONS_LABELS,
    FAILURE_LABELS,
    FEATURE_LABELS,
    FLUID_LABELS,
    MAINTENANCE_LABELS,
    MARKET_LABELS,
    MULTIMEDIA_LABELS,
    PART_LABELS,
    PHOTO_LABELS,
    PRICE_LABELS,
    SERVICE_LABELS,
    SUSPENSION_LABELS,
    TECHNICAL_SPEC_LABELS,
    TIRE_LABELS,
    WHEEL_LABELS,
    apply_field_labels,
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
        fields = (
            "brand",
            "name",
            "name_fa",
            "name_en",
            "name_ar",
            "official_name",
            "model_code",
            "chassis_code",
            "generation",
            "body_style",
            "introduced_year",
            "iran_entry_year",
            "production_start_year",
            "production_end_year",
            "categories",
        )
        widgets = {
            "categories": forms.CheckboxSelectMultiple,
        }


class TrimForm(forms.ModelForm):
    class Meta:
        model = Trim
        fields = ("car_model", "name")


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("slug", "name", "name_fa", "name_en", "name_ar", "sort_order")


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
            "name_fa",
            "name_en",
            "name_ar",
            "official_name_fa",
            "official_name_en",
            "official_name_ar",
            "description_fa",
            "description_en",
            "description_ar",
            "model_code",
            "chassis_code",
            "generation",
            "facelift",
            "body_style",
            "manufacturer",
            "importer",
            "assembler",
            "country_of_origin",
            "country_of_assembly",
            "introduced_year",
            "iran_entry_year",
            "production_start_year",
            "production_end_year",
            "market_status",
            "doors",
            "categories",
            "cover_image",
            "is_published",
        )
        widgets = {
            "description_fa": forms.Textarea(attrs={"rows": 4}),
            "description_en": forms.Textarea(attrs={"rows": 4}),
            "description_ar": forms.Textarea(attrs={"rows": 4}),
            "categories": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, CAR_LABELS)
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, TECHNICAL_SPEC_LABELS)


class DimensionsForm(forms.ModelForm):
    class Meta:
        model = Dimensions
        exclude = ("car",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, DIMENSIONS_LABELS)


class SuspensionSpecForm(forms.ModelForm):
    class Meta:
        model = SuspensionSpec
        exclude = ("car",)
        widgets = {"notes": forms.Textarea(attrs={"rows": 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, SUSPENSION_LABELS)


class BrakeSpecForm(forms.ModelForm):
    class Meta:
        model = BrakeSpec
        exclude = ("car",)
        widgets = {"notes": forms.Textarea(attrs={"rows": 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, BRAKE_LABELS)


class WheelSpecForm(forms.ModelForm):
    class Meta:
        model = WheelSpec
        exclude = ("car",)
        widgets = {"notes": forms.Textarea(attrs={"rows": 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, WHEEL_LABELS)


class CabinSpecForm(forms.ModelForm):
    class Meta:
        model = CabinSpec
        exclude = ("car",)
        widgets = {"notes": forms.Textarea(attrs={"rows": 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, CABIN_LABELS)


class MultimediaSpecForm(forms.ModelForm):
    class Meta:
        model = MultimediaSpec
        exclude = ("car",)
        widgets = {"notes": forms.Textarea(attrs={"rows": 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, MULTIMEDIA_LABELS)


class MarketInfoForm(forms.ModelForm):
    class Meta:
        model = MarketInfo
        exclude = ("car",)
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 2}),
            "recorded_at": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, MARKET_LABELS)
        # Entire OneToOne block is optional on the car form.
        for field in self.fields.values():
            field.required = False


class CarPhotoForm(forms.ModelForm):
    class Meta:
        model = CarPhoto
        fields = ("image", "caption", "sort_order")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, PHOTO_LABELS)


class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ("category", "key", "name", "value", "availability")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, FEATURE_LABELS)


class MaintenanceItemForm(forms.ModelForm):
    class Meta:
        model = MaintenanceItem
        fields = (
            "title",
            "interval_km",
            "interval_months",
            "description",
            "estimated_cost",
        )
        widgets = {"description": forms.Textarea(attrs={"rows": 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, MAINTENANCE_LABELS)


class FluidSpecForm(forms.ModelForm):
    class Meta:
        model = FluidSpec
        fields = (
            "fluid_type",
            "specification",
            "grade",
            "capacity",
            "interval_km",
            "interval_months",
            "estimated_cost",
            "notes",
        )
        widgets = {"notes": forms.Textarea(attrs={"rows": 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, FLUID_LABELS)


class TireSpecForm(forms.ModelForm):
    class Meta:
        model = TireSpec
        fields = (
            "position",
            "size",
            "pressure_psi",
            "load_index",
            "speed_rating",
            "rim_size",
            "rim_material",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, TIRE_LABELS)


class BatterySpecForm(forms.ModelForm):
    class Meta:
        model = BatterySpec
        fields = ("group_size", "voltage", "cca", "chemistry", "notes")
        widgets = {"notes": forms.Textarea(attrs={"rows": 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, BATTERY_LABELS)


class ServiceScheduleItemForm(forms.ModelForm):
    class Meta:
        model = ServiceScheduleItem
        fields = ("mileage_km", "months", "tasks", "sort_order")
        widgets = {"tasks": forms.Textarea(attrs={"rows": 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, SERVICE_LABELS)


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = (
            "name",
            "oem_number",
            "category",
            "is_consumable",
            "interval_km",
            "interval_months",
            "estimated_cost",
            "notes",
        )
        widgets = {"notes": forms.Textarea(attrs={"rows": 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, PART_LABELS)


class CommonFailureForm(forms.ModelForm):
    class Meta:
        model = CommonFailure
        fields = (
            "area",
            "title",
            "severity",
            "likelihood",
            "repair_cost_min",
            "repair_cost_max",
            "currency",
            "symptoms",
            "notes",
        )
        widgets = {
            "symptoms": forms.Textarea(attrs={"rows": 2}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, FAILURE_LABELS)


class CarPriceForm(forms.ModelForm):
    class Meta:
        model = CarPrice
        fields = (
            "label",
            "amount",
            "currency",
            "source",
            "year_for_price",
            "mileage_km",
            "notes",
            "recorded_at",
        )
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 2}),
            "recorded_at": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_field_labels(self, PRICE_LABELS)


RELATED_FORM_CLASSES = {
    "spec": (TechnicalSpecForm, TechnicalSpec, "technical_spec"),
    "dims": (DimensionsForm, Dimensions, "dimensions"),
    "suspension": (SuspensionSpecForm, SuspensionSpec, "suspension"),
    "brakes": (BrakeSpecForm, BrakeSpec, "brakes"),
    "wheels": (WheelSpecForm, WheelSpec, "wheels"),
    "cabin": (CabinSpecForm, CabinSpec, "cabin"),
    "multimedia": (MultimediaSpecForm, MultimediaSpec, "multimedia"),
    "market": (MarketInfoForm, MarketInfo, "market_info"),
}


CarPhotoFormSet = inlineformset_factory(
    Car,
    CarPhoto,
    form=CarPhotoForm,
    extra=1,
    can_delete=True,
)

FeatureFormSet = inlineformset_factory(
    Car,
    Feature,
    form=FeatureForm,
    extra=1,
    can_delete=True,
)

MaintenanceItemFormSet = inlineformset_factory(
    Car,
    MaintenanceItem,
    form=MaintenanceItemForm,
    extra=1,
    can_delete=True,
)

FluidSpecFormSet = inlineformset_factory(
    Car,
    FluidSpec,
    form=FluidSpecForm,
    extra=1,
    can_delete=True,
)

TireSpecFormSet = inlineformset_factory(
    Car,
    TireSpec,
    form=TireSpecForm,
    extra=1,
    can_delete=True,
)

BatterySpecFormSet = inlineformset_factory(
    Car,
    BatterySpec,
    form=BatterySpecForm,
    extra=1,
    can_delete=True,
)

ServiceScheduleFormSet = inlineformset_factory(
    Car,
    ServiceScheduleItem,
    form=ServiceScheduleItemForm,
    extra=1,
    can_delete=True,
)

PartFormSet = inlineformset_factory(
    Car,
    Part,
    form=PartForm,
    extra=1,
    can_delete=True,
)

CommonFailureFormSet = inlineformset_factory(
    Car,
    CommonFailure,
    form=CommonFailureForm,
    extra=1,
    can_delete=True,
)

CarPriceFormSet = inlineformset_factory(
    Car,
    CarPrice,
    form=CarPriceForm,
    extra=1,
    can_delete=True,
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
    "failures": CommonFailureFormSet,
    "prices": CarPriceFormSet,
}


def _form_has_values(form):
    if not form.is_valid():
        return False
    blank = form._meta.model()
    for name, value in form.cleaned_data.items():
        if name in ("car", "id"):
            continue
        if value in (None, ""):
            continue
        default = getattr(blank, name, None)
        if value != default:
            return True
    return False


def build_car_related_forms(data=None, files=None, instance=None):
    """Return (related_forms_dict, formsets_dict) for a Car create/edit view."""
    car = instance if instance is not None else Car()
    related = {}
    for prefix, (form_cls, model_cls, _rel) in RELATED_FORM_CLASSES.items():
        obj = None
        if instance is not None and instance.pk:
            obj = model_cls.objects.filter(car=instance).first()
        if data is not None:
            related[prefix] = form_cls(data, instance=obj, prefix=prefix)
        else:
            related[prefix] = form_cls(instance=obj, prefix=prefix)

    if data is not None:
        formsets = {
            key: factory(data, files, instance=car, prefix=key)
            for key, factory in FORMSET_FACTORIES.items()
        }
    else:
        formsets = {
            key: factory(instance=car, prefix=key)
            for key, factory in FORMSET_FACTORIES.items()
        }
    return related, formsets


def car_related_forms_valid(related_forms, formsets):
    ok = all(f.is_valid() for f in related_forms.values())
    for fs in formsets.values():
        ok = fs.is_valid() and ok
    return ok


def save_car_related(car, related_forms, formsets):
    for form in related_forms.values():
        if _form_has_values(form) or (form.instance and form.instance.pk):
            obj = form.save(commit=False)
            obj.car = car
            obj.save()

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

