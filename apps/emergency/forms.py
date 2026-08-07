from django import forms
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import SavedLocation

from .models import EmergencyRequest, EmergencyService, RequestStatus
from .services import is_emergency_operator, is_emergency_operator_admin


class SubmitNewEmergencyRequestForm(forms.ModelForm):
    LOCATION_MAP = "map"
    LOCATION_SAVED = "saved"

    location_mode = forms.ChoiceField(
        choices=(
            (LOCATION_MAP, _("Select on map")),
            (LOCATION_SAVED, _("Use a saved location")),
        ),
        initial=LOCATION_MAP,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = EmergencyRequest
        fields = ("service", "description", "saved_location", "latitude", "longitude")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "latitude": forms.NumberInput(attrs={"step": "0.000001"}),
            "longitude": forms.NumberInput(attrs={"step": "0.000001"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["service"].queryset = EmergencyService.objects.filter(is_active=True)
        self.fields["saved_location"].queryset = SavedLocation.objects.none()
        self.fields["saved_location"].required = False
        self.fields["latitude"].required = False
        self.fields["longitude"].required = False
        if user and user.is_authenticated:
            self.fields["saved_location"].queryset = user.saved_locations.all()

    def clean(self):
        cleaned = super().clean()
        mode = cleaned.get("location_mode")
        if mode == self.LOCATION_SAVED:
            if not cleaned.get("saved_location"):
                self.add_error("saved_location", _("Choose a saved location."))
            cleaned["latitude"] = None
            cleaned["longitude"] = None
        else:
            cleaned["saved_location"] = None
            if cleaned.get("latitude") is None or cleaned.get("longitude") is None:
                self.add_error(
                    "latitude",
                    _("Provide latitude and longitude from the map."),
                )
                self.add_error(
                    "longitude",
                    _("Provide latitude and longitude from the map."),
                )
        return cleaned


class VerifyEmergencyTransitionForm(forms.Form):
    to_status = forms.ChoiceField(choices=[])
    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=_("Optional note for the audit trail."),
    )

    def __init__(self, *args, user=None, emergency_request=None, **kwargs):
        self.user = user
        self.emergency_request = emergency_request
        super().__init__(*args, **kwargs)
        choices = []
        status = emergency_request.status if emergency_request else None
        if status == RequestStatus.WAIT_FOR_ACCEPT and is_emergency_operator(user):
            choices.append((RequestStatus.PROCESSING, _("Accept / start processing")))
        if status == RequestStatus.PROCESSING and is_emergency_operator_admin(user):
            choices.extend(
                [
                    (RequestStatus.FINISH_SUCCESS, _("Finish successfully")),
                    (RequestStatus.FINISH_FAILED, _("Finish as failed")),
                ]
            )
        if status in (RequestStatus.WAIT_FOR_ACCEPT, RequestStatus.PROCESSING):
            if emergency_request and (
                emergency_request.requester_id == getattr(user, "id", None)
                or is_emergency_operator(user)
            ):
                choices.append((RequestStatus.CANCELLED, _("Cancel request")))
        self.fields["to_status"].choices = choices
        if not choices:
            self.fields["to_status"].disabled = True


class EmergencyReviewForm(forms.Form):
    review_comment = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}),
        label=_("Public review"),
    )
    review_rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        required=False,
        label=_("Rating (1–5)"),
    )


class EmergencySearchForm(forms.Form):
    q = forms.CharField(required=False, label=_("Search"))
    service = forms.ModelChoiceField(
        required=False,
        queryset=EmergencyService.objects.filter(is_active=True),
        empty_label=_("All services"),
    )
