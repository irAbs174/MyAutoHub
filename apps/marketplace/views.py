from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from apps.cars.models import Brand, CarModel

from .models import Currency, Listing, ListingInquiry, ListingPhoto, ListingStatus


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def clean(self, data, initial=None):
        single_clean = super().clean
        if not data and not self.required:
            return []
        if not isinstance(data, (list, tuple)):
            data = [data] if data else []
        cleaned = []
        errors = []
        for item in data:
            try:
                value = single_clean(item, initial)
            except forms.ValidationError as exc:
                errors.extend(exc.error_list)
            else:
                if value:
                    cleaned.append(value)
        if errors:
            raise forms.ValidationError(errors)
        return cleaned


class ListingForm(forms.ModelForm):
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        empty_label=_("Select brand"),
    )
    photos = MultipleFileField(
        required=False,
        widget=MultipleImageInput(attrs={"accept": "image/*", "multiple": True}),
    )

    class Meta:
        model = Listing
        fields = (
            "title_fa",
            "title_en",
            "title_ar",
            "description_fa",
            "description_en",
            "description_ar",
            "car_model",
            "trim",
            "price",
            "currency",
            "year",
            "mileage_km",
            "city",
        )
        widgets = {
            "title_fa": forms.TextInput(attrs={"autocomplete": "off"}),
            "title_en": forms.TextInput(attrs={"autocomplete": "off"}),
            "title_ar": forms.TextInput(attrs={"autocomplete": "off"}),
            "description_fa": forms.Textarea(attrs={"rows": 4}),
            "description_en": forms.Textarea(attrs={"rows": 4}),
            "description_ar": forms.Textarea(attrs={"rows": 4}),
            "trim": forms.TextInput(attrs={"autocomplete": "off"}),
            "price": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
            "currency": forms.Select(),
            "year": forms.NumberInput(attrs={"min": "1950", "max": "2100"}),
            "mileage_km": forms.NumberInput(attrs={"min": "0"}),
            "city": forms.TextInput(attrs={"autocomplete": "address-level2"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = {
            "title_fa": _("Title (فارسی)"),
            "title_en": _("Title (English)"),
            "title_ar": _("Title (العربية)"),
            "description_fa": _("Description (فارسی)"),
            "description_en": _("Description (English)"),
            "description_ar": _("Description (العربية)"),
            "brand": _("Brand"),
            "car_model": _("Model"),
            "trim": _("Trim"),
            "photos": _("Photos"),
            "price": _("Price"),
            "currency": _("Currency"),
            "year": _("Year"),
            "mileage_km": _("Mileage (km)"),
            "city": _("City"),
        }
        helps = {
            "title_fa": _("A short headline buyers will see first."),
            "title_en": _("A short headline buyers will see first."),
            "title_ar": _("A short headline buyers will see first."),
            "description_fa": _("Be honest and specific-it builds trust."),
            "description_en": _("Be honest and specific-it builds trust."),
            "description_ar": _("Be honest and specific-it builds trust."),
            "brand": _("Choose the car brand from the catalog (optional)."),
            "car_model": _("Choose the model for the selected brand (optional)."),
            "trim": _("Trim or variant, e.g. SE, Limited (optional)."),
            "photos": _(
                "Optional, but listings with photos sell faster. You can select multiple."
            ),
            "price": _("Ask a fair market price."),
            "currency": _("Prices are shown in the currency you select."),
            "year": _("Model year (optional)."),
            "mileage_km": _("Odometer reading in kilometres (optional)."),
            "city": _("Where the car is located (optional)."),
        }
        placeholders = {
            "title_fa": _("e.g. 2018 Toyota Corolla"),
            "title_en": _("e.g. 2018 Toyota Corolla"),
            "title_ar": _("e.g. 2018 Toyota Corolla"),
            "description_fa": _("Condition, extras, reason for selling…"),
            "description_en": _("Condition, extras, reason for selling…"),
            "description_ar": _("Condition, extras, reason for selling…"),
            "trim": _("e.g. SE"),
            "city": _("e.g. Tehran"),
        }
        for name, label in labels.items():
            if name in self.fields:
                self.fields[name].label = label
                self.fields[name].help_text = helps.get(name, "")
        for name, placeholder in placeholders.items():
            if name in self.fields:
                self.fields[name].widget.attrs["placeholder"] = placeholder
        for name in (
            "title_fa",
            "title_en",
            "title_ar",
            "description_fa",
            "description_en",
            "description_ar",
        ):
            self.fields[name].required = False
        self.fields["currency"].choices = Currency.choices
        if not self.is_bound and not self.initial.get("currency") and not (
            self.instance and self.instance.pk
        ):
            self.initial["currency"] = Currency.TOMAN
        # Keep legacy stored values editable even if not in the current list.
        current = self.initial.get("currency") or getattr(self.instance, "currency", None)
        if current and current not in dict(Currency.choices):
            self.fields["currency"].choices = [
                (current, current),
                *Currency.choices,
            ]
        self.fields["year"].required = False
        self.fields["mileage_km"].required = False
        self.fields["city"].required = False
        self.fields["trim"].required = False
        self.fields["photos"].required = False
        self.fields["car_model"].required = False
        self.fields["car_model"].empty_label = _("Select model")
        self.fields["car_model"].queryset = CarModel.objects.select_related("brand").all()

        brand_id = None
        if self.data.get("brand"):
            brand_id = self.data.get("brand")
        elif self.initial.get("brand"):
            brand = self.initial.get("brand")
            brand_id = getattr(brand, "pk", brand)
        elif self.instance and self.instance.pk and self.instance.car_model_id:
            brand_id = self.instance.car_model.brand_id
            if "brand" not in self.initial:
                self.initial["brand"] = self.instance.car_model.brand

        if brand_id:
            self.fields["car_model"].queryset = CarModel.objects.filter(
                brand_id=brand_id
            ).select_related("brand")
        elif not self.is_bound:
            if not (self.instance and self.instance.car_model_id):
                self.fields["car_model"].queryset = CarModel.objects.none()

    def clean(self):
        cleaned = super().clean()
        langs = ("fa", "en", "ar")
        has_complete = False
        for code in langs:
            title = (cleaned.get(f"title_{code}") or "").strip()
            description = (cleaned.get(f"description_{code}") or "").strip()
            if title and description:
                has_complete = True
                break
        if not has_complete:
            raise forms.ValidationError(
                _(
                    "Add a title and description in at least one language "
                    "(فارسی, English, or العربية)."
                )
            )
        brand = cleaned.get("brand")
        car_model = cleaned.get("car_model")
        if car_model and brand and car_model.brand_id != brand.pk:
            self.add_error(
                "car_model",
                _("Selected model does not belong to the chosen brand."),
            )
        return cleaned

    def clean_photos(self):
        images = self.cleaned_data.get("photos") or []
        for uploaded in images:
            content_type = getattr(uploaded, "content_type", "") or ""
            if content_type and not content_type.startswith("image/"):
                raise forms.ValidationError(_("Please upload image files only."))
        return images


class ListingEditForm(ListingForm):
    class Meta(ListingForm.Meta):
        fields = ListingForm.Meta.fields + ("status",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].label = _("Status")
        self.fields["status"].help_text = _("Active listings appear in the marketplace.")


def _brands_models_payload():
    payload = {}
    for model in CarModel.objects.select_related("brand").order_by("name"):
        key = str(model.brand_id)
        payload.setdefault(key, []).append({"id": model.pk, "name": model.name})
    return payload


def _listing_form_context(form, *, editing=False, listing=None):
    return {
        "form": form,
        "editing": editing,
        "listing": listing,
        "brands_models": _brands_models_payload(),
    }


def _save_listing_photos(listing, uploaded_files):
    if not uploaded_files:
        return
    start = listing.photos.count()
    first_photo = None
    for index, image in enumerate(uploaded_files):
        photo = ListingPhoto.objects.create(
            listing=listing,
            image=image,
            sort_order=start + index,
        )
        if first_photo is None:
            first_photo = photo
    if not listing.cover_image and first_photo and first_photo.image:
        listing.cover_image = first_photo.image.name
        listing.save(update_fields=["cover_image", "updated_at"])


class InquiryForm(forms.ModelForm):
    class Meta:
        model = ListingInquiry
        fields = ("message", "contact_phone")
        widgets = {
            "message": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["message"].label = _("Your message to the seller")
        self.fields["contact_phone"].label = _("Phone (optional)")
        self.fields["contact_phone"].required = False


def list_listings(request):
    items = (
        Listing.objects.filter(status=ListingStatus.ACTIVE)
        .select_related("seller", "car_model__brand")
        .prefetch_related("photos")
        .annotate(inquiry_count=Count("inquiries"))
    )
    return render(
        request,
        "marketplace/list.html",
        {
            "items": items,
            "buy_count": items.count(),
        },
    )


@login_required
def my_listings(request):
    items = (
        Listing.objects.filter(seller=request.user)
        .select_related("car_model__brand")
        .prefetch_related("photos")
        .annotate(
            inquiry_count=Count("inquiries"),
            unread_count=Count("inquiries", filter=Q(inquiries__is_read=False)),
        )
        .order_by("-created_at")
    )
    return render(request, "marketplace/mine.html", {"items": items})


def detail(request, pk):
    item = get_object_or_404(
        Listing.objects.select_related("seller", "car_model__brand").prefetch_related(
            "photos"
        ),
        pk=pk,
    )
    is_owner = request.user.is_authenticated and item.seller_id == request.user.id
    inquiry_form = None
    inquiries = []

    if is_owner:
        inquiries = item.inquiries.select_related("buyer").all()
        if inquiries.filter(is_read=False).exists():
            inquiries.filter(is_read=False).update(is_read=True)
    elif item.is_available:
        inquiry_form = InquiryForm()

    return render(
        request,
        "marketplace/detail.html",
        {
            "item": item,
            "is_owner": is_owner,
            "inquiry_form": inquiry_form,
            "inquiries": inquiries,
        },
    )


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.status = ListingStatus.ACTIVE
            listing.save()
            _save_listing_photos(listing, form.cleaned_data.get("photos") or [])
            messages.success(
                request,
                _("Your car is listed. Buyers can message you from the listing."),
            )
            return redirect("marketplace:detail", pk=listing.pk)
    else:
        form = ListingForm(initial={"currency": Currency.TOMAN})
    return render(
        request,
        "marketplace/create.html",
        _listing_form_context(form, editing=False),
    )


@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(
        Listing.objects.select_related("car_model__brand").prefetch_related("photos"),
        pk=pk,
        seller=request.user,
    )
    if request.method == "POST":
        form = ListingEditForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            remove_ids = request.POST.getlist("remove_photos")
            if remove_ids:
                listing.photos.filter(pk__in=remove_ids).delete()
            _save_listing_photos(listing, form.cleaned_data.get("photos") or [])
            messages.success(request, _("Listing updated."))
            return redirect("marketplace:detail", pk=listing.pk)
    else:
        form = ListingEditForm(instance=listing)
    return render(
        request,
        "marketplace/create.html",
        _listing_form_context(form, editing=True, listing=listing),
    )


@login_required
@require_POST
def mark_sold(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    listing.status = ListingStatus.SOLD
    listing.save(update_fields=["status", "updated_at"])
    messages.success(request, _("Marked as sold. It no longer appears for buyers."))
    return redirect("marketplace:detail", pk=listing.pk)


@login_required
@require_POST
def withdraw_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    listing.status = ListingStatus.WITHDRAWN
    listing.save(update_fields=["status", "updated_at"])
    messages.success(request, _("Listing withdrawn."))
    return redirect("marketplace:mine")


@login_required
@require_POST
def inquire(request, pk):
    listing = get_object_or_404(
        Listing.objects.select_related("seller", "car_model__brand"),
        pk=pk,
        status=ListingStatus.ACTIVE,
    )
    if listing.seller_id == request.user.id:
        messages.error(request, _("You cannot inquire on your own listing."))
        return redirect("marketplace:detail", pk=pk)

    form = InquiryForm(request.POST)
    if form.is_valid():
        inquiry = form.save(commit=False)
        inquiry.listing = listing
        inquiry.buyer = request.user
        inquiry.save()
        messages.success(
            request,
            _("Message sent to %(seller)s. They will see it on this listing.")
            % {"seller": listing.seller.get_username()},
        )
        return redirect("marketplace:detail", pk=pk)

    return render(
        request,
        "marketplace/detail.html",
        {
            "item": listing,
            "is_owner": False,
            "inquiry_form": form,
            "inquiries": [],
        },
    )
