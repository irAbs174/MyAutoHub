from django.contrib import admin

from .models import SavedLocation


@admin.register(SavedLocation)
class SavedLocationAdmin(admin.ModelAdmin):
    list_display = ("label", "user", "latitude", "longitude", "is_default", "created_at")
    list_filter = ("is_default",)
    search_fields = ("label", "address", "user__username")
