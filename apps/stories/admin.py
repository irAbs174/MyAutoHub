from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Story


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("title_fa", "title_en", "author", "is_published", "published_at")
    list_filter = ("is_published",)
    search_fields = (
        "title_fa",
        "title_en",
        "title_ar",
        "excerpt_fa",
        "excerpt_en",
        "excerpt_ar",
        "body_fa",
        "body_en",
        "body_ar",
    )
    prepopulated_fields = {"slug": ("title_en",)}
    fieldsets = (
        (
            _("فارسی"),
            {"fields": ("title_fa", "excerpt_fa", "body_fa")},
        ),
        (
            _("English"),
            {"fields": ("title_en", "excerpt_en", "body_en")},
        ),
        (
            _("العربية"),
            {"fields": ("title_ar", "excerpt_ar", "body_ar")},
        ),
        (
            _("Publishing"),
            {"fields": ("slug", "cover_image", "author", "is_published", "published_at")},
        ),
    )
