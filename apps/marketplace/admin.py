from django.contrib import admin

from .models import Listing, ListingInquiry, ListingPhoto


class ListingPhotoInline(admin.TabularInline):
    model = ListingPhoto
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "seller",
        "car_model",
        "trim",
        "price",
        "currency",
        "status",
        "created_at",
    )
    list_filter = ("status", "currency", "car_model__brand")
    search_fields = (
        "title_fa",
        "title_en",
        "title_ar",
        "description_fa",
        "description_en",
        "description_ar",
        "seller__username",
        "city",
        "trim",
        "car_model__name",
        "car_model__brand__name",
    )
    autocomplete_fields = ("car_model",)
    inlines = [ListingPhotoInline]


@admin.register(ListingInquiry)
class ListingInquiryAdmin(admin.ModelAdmin):
    list_display = ("listing", "buyer", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = (
        "message",
        "buyer__username",
        "listing__title_en",
        "listing__title_fa",
        "contact_phone",
    )
