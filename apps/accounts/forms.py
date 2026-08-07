from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import SavedLocation

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autocomplete": "username"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"})
    )


class SavedLocationForm(forms.ModelForm):
    class Meta:
        model = SavedLocation
        fields = ("label", "address", "latitude", "longitude", "is_default")
        widgets = {
            # Coordinates come from the map pin only (profile UI).
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
        }
