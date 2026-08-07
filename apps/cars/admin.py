from django.contrib import admin

from .models import Brand, Car, CarModel, CarPhoto


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 0


class CarPhotoInline(admin.TabularInline):
    model = CarPhoto
    extra = 1


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name",)
    inlines = [CarModelInline]


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "brand")
    list_filter = ("brand",)
    search_fields = ("name", "brand__name")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("model", "year", "trim", "horsepower", "is_published")
    list_filter = ("is_published", "year", "model__brand")
    search_fields = ("model__name", "model__brand__name", "trim")
    inlines = [CarPhotoInline]
