from django.contrib import admin

from .models import (
    BatterySpec,
    Brand,
    Car,
    CarModel,
    CarPhoto,
    CarPrice,
    Dealer,
    Dimensions,
    Feature,
    FluidSpec,
    MaintenanceItem,
    OBDCode,
    Part,
    RepairShop,
    ServiceScheduleItem,
    TechnicalSpec,
    TireSpec,
    Trim,
)


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 0


class TrimInline(admin.TabularInline):
    model = Trim
    extra = 0


class CarPhotoInline(admin.TabularInline):
    model = CarPhoto
    extra = 1


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 0


class MaintenanceItemInline(admin.TabularInline):
    model = MaintenanceItem
    extra = 0


class FluidSpecInline(admin.TabularInline):
    model = FluidSpec
    extra = 0


class TireSpecInline(admin.TabularInline):
    model = TireSpec
    extra = 0


class BatterySpecInline(admin.TabularInline):
    model = BatterySpec
    extra = 0


class ServiceScheduleItemInline(admin.TabularInline):
    model = ServiceScheduleItem
    extra = 0


class PartInline(admin.TabularInline):
    model = Part
    extra = 0


class CarPriceInline(admin.TabularInline):
    model = CarPrice
    extra = 0


class TechnicalSpecInline(admin.StackedInline):
    model = TechnicalSpec
    extra = 0
    max_num = 1


class DimensionsInline(admin.StackedInline):
    model = Dimensions
    extra = 0
    max_num = 1


class OBDCodeInline(admin.TabularInline):
    model = OBDCode
    extra = 0


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
    inlines = [TrimInline, OBDCodeInline]


@admin.register(Trim)
class TrimAdmin(admin.ModelAdmin):
    list_display = ("name", "car_model", "brand_name")
    list_filter = ("car_model__brand", "car_model")
    search_fields = ("name", "car_model__name", "car_model__brand__name")

    @admin.display(description="Brand", ordering="car_model__brand__name")
    def brand_name(self, obj):
        return obj.car_model.brand.name


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("model", "year", "trim", "horsepower", "is_published")
    list_filter = ("is_published", "year", "model__brand")
    search_fields = ("model__name", "model__brand__name", "trim__name")
    autocomplete_fields = ("model", "trim")
    inlines = [
        TechnicalSpecInline,
        DimensionsInline,
        CarPhotoInline,
        FeatureInline,
        MaintenanceItemInline,
        FluidSpecInline,
        TireSpecInline,
        BatterySpecInline,
        ServiceScheduleItemInline,
        PartInline,
        CarPriceInline,
    ]


@admin.register(OBDCode)
class OBDCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "car_model", "severity")
    list_filter = ("severity", "car_model__brand")
    search_fields = ("code", "title", "car_model__name")


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "phone", "is_published")
    list_filter = ("is_published", "brands")
    search_fields = ("name", "city", "phone")
    filter_horizontal = ("brands",)


@admin.register(RepairShop)
class RepairShopAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "phone", "is_published")
    list_filter = ("is_published", "brands")
    search_fields = ("name", "city", "phone")
    filter_horizontal = ("brands",)
