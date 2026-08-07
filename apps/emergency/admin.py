from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import EmergencyBuzz, EmergencyRequest, EmergencyService, EmergencyTransition


class TransitionInline(admin.TabularInline):
    model = EmergencyTransition
    extra = 0
    readonly_fields = ("from_status", "to_status", "actor", "note", "created_at")
    can_delete = False


class BuzzInline(admin.TabularInline):
    model = EmergencyBuzz
    extra = 0
    readonly_fields = ("from_user", "seen_by_operators", "created_at")
    can_delete = False


@admin.register(EmergencyService)
class EmergencyServiceAdmin(admin.ModelAdmin):
    list_display = ("name_fa", "name_en", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = (
        "name_fa",
        "name_en",
        "name_ar",
        "description_fa",
        "description_en",
        "description_ar",
    )
    fieldsets = (
        (
            _("فارسی"),
            {"fields": ("name_fa", "description_fa", "coverage_notes_fa")},
        ),
        (
            _("English"),
            {"fields": ("name_en", "description_en", "coverage_notes_en")},
        ),
        (
            _("العربية"),
            {"fields": ("name_ar", "description_ar", "coverage_notes_ar")},
        ),
        (_("Status & media"), {"fields": ("cover_image", "is_active")}),
    )


@admin.register(EmergencyRequest)
class EmergencyRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "service",
        "requester",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "service")
    search_fields = (
        "description",
        "requester__username",
        "service__name_fa",
        "service__name_en",
        "service__name_ar",
    )
    inlines = [TransitionInline, BuzzInline]
    readonly_fields = ("created_at", "updated_at", "reviewed_at")


@admin.register(EmergencyTransition)
class EmergencyTransitionAdmin(admin.ModelAdmin):
    list_display = ("request", "from_status", "to_status", "actor", "created_at")
    list_filter = ("to_status", "from_status")


@admin.register(EmergencyBuzz)
class EmergencyBuzzAdmin(admin.ModelAdmin):
    list_display = ("request", "from_user", "seen_by_operators", "created_at")
    list_filter = ("seen_by_operators",)
