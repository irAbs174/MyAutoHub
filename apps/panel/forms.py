from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from apps.cars.models import Brand, Car, CarModel, CarPhoto
from apps.emergency.models import EmergencyService, RequestStatus
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
        fields = ("name", "country")


class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = ("brand", "name")


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


CarPhotoFormSet = inlineformset_factory(
    Car,
    CarPhoto,
    fields=("image", "caption", "sort_order"),
    extra=1,
    can_delete=True,
)


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
