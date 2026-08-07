from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.i18n_content import localized


class PriceReference(models.Model):
    title_fa = models.CharField(max_length=160, verbose_name=_("Title (فارسی)"))
    title_en = models.CharField(max_length=160, verbose_name=_("Title (English)"))
    title_ar = models.CharField(max_length=160, verbose_name=_("Title (العربية)"))
    category_fa = models.CharField(
        max_length=80, blank=True, verbose_name=_("Category (فارسی)")
    )
    category_en = models.CharField(
        max_length=80, blank=True, verbose_name=_("Category (English)")
    )
    category_ar = models.CharField(
        max_length=80, blank=True, verbose_name=_("Category (العربية)")
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default="تومان")
    notes_fa = models.TextField(blank=True, verbose_name=_("Notes (فارسی)"))
    notes_en = models.TextField(blank=True, verbose_name=_("Notes (English)"))
    notes_ar = models.TextField(blank=True, verbose_name=_("Notes (العربية)"))
    source_fa = models.CharField(
        max_length=160, blank=True, verbose_name=_("Source (فارسی)")
    )
    source_en = models.CharField(
        max_length=160, blank=True, verbose_name=_("Source (English)")
    )
    source_ar = models.CharField(
        max_length=160, blank=True, verbose_name=_("Source (العربية)")
    )
    cover_image = models.ImageField(upload_to="pricing/covers/", blank=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category_fa", "title_fa"]

    def __str__(self):
        return f"{self.title} ({self.amount} {self.currency})"

    def get_absolute_url(self):
        return reverse("pricing:detail", kwargs={"pk": self.pk})

    @property
    def title(self):
        return localized(self, "title")

    @property
    def category(self):
        return localized(self, "category")

    @property
    def notes(self):
        return localized(self, "notes")

    @property
    def source(self):
        return localized(self, "source")

    @property
    def main_image(self):
        if self.cover_image:
            return self.cover_image
        photo = self.photos.order_by("sort_order", "id").first()
        return photo.image if photo else None


class PriceReferencePhoto(models.Model):
    price_reference = models.ForeignKey(
        PriceReference,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    image = models.ImageField(upload_to="pricing/gallery/")
    caption = models.CharField(max_length=160, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"Photo {self.pk} for price {self.price_reference_id}"
