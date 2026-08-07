from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView

from .forms import LoginForm, RegisterForm, SavedLocationForm
from .models import SavedLocation


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, _("Welcome to MyAutoHub."))
        return response

    def get_success_url(self):
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        if next_url and next_url.startswith("/"):
            return next_url
        return super().get_success_url()


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("core:home")


@login_required
def profile(request):
    locations = request.user.saved_locations.all()
    if request.method == "POST":
        form = SavedLocationForm(request.POST)
        if form.is_valid():
            loc = form.save(commit=False)
            loc.user = request.user
            if loc.is_default:
                request.user.saved_locations.update(is_default=False)
            loc.save()
            messages.success(request, _("Location saved."))
            return redirect("accounts:profile")
    else:
        form = SavedLocationForm()
    return render(
        request,
        "accounts/profile.html",
        {"locations": locations, "form": form},
    )


@login_required
def delete_location(request, pk):
    loc = get_object_or_404(SavedLocation, pk=pk, user=request.user)
    if request.method == "POST":
        loc.delete()
        messages.info(request, _("Location removed."))
    return redirect("accounts:profile")
