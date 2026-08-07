from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.i18n_content import localized


class ListingStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    SOLD = "sold", "Sold"
    WITHDRAWN = "withdrawn", "Withdrawn"


class Currency(models.TextChoices):
    TOMAN = "تومان", _("Iran (تومان)")
    IRR = "IRR", _("Iran (IRR)")
    USD = "USD", _("United States (USD)")
    AED = "AED", _("United Arab Emirates (AED)")
    EUR = "EUR", _("Euro (EUR)")


class Listing(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
    )
    title_fa = models.CharField(
        max_length=160, blank=True, default="", verbose_name=_("Title (فارسی)")
    )
    title_en = models.CharField(
        max_length=160, blank=True, default="", verbose_name=_("Title (English)")
    )
    title_ar = models.CharField(
        max_length=160, blank=True, default="", verbose_name=_("Title (العربية)")
    )
    description_fa = models.TextField(
        blank=True, default="", verbose_name=_("Description (فارسی)")
    )
    description_en = models.TextField(
        blank=True, default="", verbose_name=_("Description (English)")
    )
    description_ar = models.TextField(
        blank=True, default="", verbose_name=_("Description (العربية)")
    )
    cover_image = models.ImageField(upload_to="marketplace/covers/", blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(
        max_length=8,
        choices=Currency.choices,
        default=Currency.TOMAN,
    )
    car_model = models.ForeignKey(
        "cars.CarModel",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="listings",
    )
    trim = models.CharField(max_length=80, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    mileage_km = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=80, blank=True)
    status = models.CharField(
        max_length=16,
        choices=ListingStatus.choices,
        default=ListingStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("marketplace:detail", kwargs={"pk": self.pk})

    @property
    def title(self):
        return localized(self, "title")

    @property
    def description(self):
        return localized(self, "description")

    @property
    def is_available(self):
        return self.status == ListingStatus.ACTIVE

    @property
    def brand_name(self):
        if self.car_model_id:
            return self.car_model.brand.name
        return ""

    @property
    def model_name(self):
        if self.car_model_id:
            return self.car_model.name
        return ""

    @property
    def car_identity(self):
        """Brand + model + optional trim for display."""
        if not self.car_model_id:
            return (self.trim or "").strip()
        parts = [str(self.car_model)]
        if self.trim:
            parts.append(self.trim)
        return " ".join(parts)

    @property
    def main_image(self):
        if self.cover_image:
            return self.cover_image
        photo = self.photos.order_by("sort_order", "id").first()
        return photo.image if photo else None


class ListingPhoto(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    image = models.ImageField(upload_to="marketplace/gallery/")
    caption = models.CharField(max_length=160, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"Photo {self.pk} for listing {self.listing_id}"


class ListingInquiry(models.Model):
    """Buyer interest message on another user's listing."""

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="inquiries",
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listing_inquiries",
    )
    message = models.TextField()
    contact_phone = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "listing inquiries"

    def __str__(self):
        return f"Inquiry on {self.listing_id} by {self.buyer_id}"
