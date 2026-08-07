from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import PriceReference, PriceReferencePhoto


class PriceReferencePhotoInline(admin.TabularInline):
    model = PriceReferencePhoto
    extra = 1


@admin.register(PriceReference)
class PriceReferenceAdmin(admin.ModelAdmin):
    list_display = ("title_fa", "title_en", "amount", "currency", "is_published", "updated_at")
    list_filter = ("currency", "is_published")
    search_fields = (
        "title_fa",
        "title_en",
        "title_ar",
        "category_fa",
        "category_en",
        "category_ar",
        "notes_fa",
        "notes_en",
        "notes_ar",
        "source_fa",
        "source_en",
        "source_ar",
    )
    inlines = [PriceReferencePhotoInline]
    fieldsets = (
        (
            _("فارسی"),
            {"fields": ("title_fa", "category_fa", "notes_fa", "source_fa")},
        ),
        (
            _("English"),
            {"fields": ("title_en", "category_en", "notes_en", "source_en")},
        ),
        (
            _("العربية"),
            {"fields": ("title_ar", "category_ar", "notes_ar", "source_ar")},
        ),
        (
            _("Pricing & media"),
            {"fields": ("amount", "currency", "cover_image", "is_published")},
        ),
    )
