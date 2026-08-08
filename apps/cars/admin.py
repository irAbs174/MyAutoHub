from django.contrib import admin

from .models import (
    BatterySpec,
    BrakeSpec,
    Brand,
    CabinSpec,
    Car,
    CarModel,
    CarPhoto,
    CarPrice,
    Category,
    CommonFailure,
    Dealer,
    Dimensions,
    Feature,
    FluidSpec,
    MaintenanceItem,
    MarketInfo,
    MultimediaSpec,
    OBDCode,
    Part,
    RepairShop,
    ServiceScheduleItem,
    SuspensionSpec,
    TechnicalSpec,
    TireSpec,
    Trim,
    WheelSpec,
)


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 0
    fields = (
        "name",
        "name_fa",
        "name_en",
        "generation",
        "body_style",
        "model_code",
    )


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


class CommonFailureInline(admin.TabularInline):
    model = CommonFailure
    extra = 0


class TechnicalSpecInline(admin.StackedInline):
    model = TechnicalSpec
    extra = 0
    max_num = 1


class DimensionsInline(admin.StackedInline):
    model = Dimensions
    extra = 0
    max_num = 1


class SuspensionSpecInline(admin.StackedInline):
    model = SuspensionSpec
    extra = 0
    max_num = 1


class BrakeSpecInline(admin.StackedInline):
    model = BrakeSpec
    extra = 0
    max_num = 1


class WheelSpecInline(admin.StackedInline):
    model = WheelSpec
    extra = 0
    max_num = 1


class CabinSpecInline(admin.StackedInline):
    model = CabinSpec
    extra = 0
    max_num = 1


class MultimediaSpecInline(admin.StackedInline):
    model = MultimediaSpec
    extra = 0
    max_num = 1


class MarketInfoInline(admin.StackedInline):
    model = MarketInfo
    extra = 0
    max_num = 1


class OBDCodeInline(admin.TabularInline):
    model = OBDCode
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "name_fa", "name_en", "name_ar", "slug", "sort_order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "name_fa", "name_en", "name_ar", "slug")


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "manufacturer", "country")
    search_fields = ("name", "manufacturer", "country")
    inlines = [CarModelInline]


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "generation", "body_style", "model_code")
    list_filter = ("brand", "body_style")
    search_fields = (
        "name",
        "name_fa",
        "name_en",
        "name_ar",
        "brand__name",
        "model_code",
    )
    filter_horizontal = ("categories",)
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
    list_display = (
        "model",
        "year",
        "trim",
        "market_status",
        "horsepower",
        "is_published",
    )
    list_filter = ("is_published", "year", "market_status", "body_style", "model__brand")
    search_fields = (
        "model__name",
        "model__brand__name",
        "trim__name",
        "name_fa",
        "name_en",
        "name_ar",
        "importer",
    )
    autocomplete_fields = ("model", "trim")
    filter_horizontal = ("categories",)
    inlines = [
        TechnicalSpecInline,
        DimensionsInline,
        SuspensionSpecInline,
        BrakeSpecInline,
        WheelSpecInline,
        CabinSpecInline,
        MultimediaSpecInline,
        MarketInfoInline,
        CarPhotoInline,
        FeatureInline,
        MaintenanceItemInline,
        FluidSpecInline,
        TireSpecInline,
        BatterySpecInline,
        ServiceScheduleItemInline,
        PartInline,
        CommonFailureInline,
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
