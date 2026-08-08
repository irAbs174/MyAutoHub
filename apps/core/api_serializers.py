from rest_framework import serializers

from apps.cars.models import (
    BatterySpec,
    BrakeSpec,
    Brand,
    CabinSpec,
    Car,
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
    WheelSpec,
)
from apps.core.i18n_content import localized
from apps.emergency.models import EmergencyService
from apps.marketplace.models import Listing
from apps.pricing.models import PriceReference
from apps.stories.models import Story
from apps.youtube.models import YoutubeVideo


def absolute_media_url(request, file_field):
    if not file_field:
        return None
    url = file_field.url
    if request is None:
        return url
    return request.build_absolute_uri(url)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name", "country", "manufacturer")


class CategorySerializer(serializers.ModelSerializer):
    name_localized = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "slug", "name", "name_fa", "name_en", "name_ar", "name_localized")

    def get_name_localized(self, obj):
        return localized(obj, "name") or obj.name


class PublicCarSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="model.brand.name", read_only=True)
    brand_id = serializers.IntegerField(source="model.brand_id", read_only=True)
    model_name = serializers.CharField(source="model.name", read_only=True)
    trim = serializers.SerializerMethodField()
    trim_name = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)
    market_status_display = serializers.CharField(
        source="get_market_status_display", read_only=True
    )
    body_style_display = serializers.CharField(
        source="get_body_style_display", read_only=True
    )
    description = serializers.SerializerMethodField()
    official_name = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = (
            "id",
            "brand",
            "brand_id",
            "model_name",
            "year",
            "trim",
            "trim_name",
            "horsepower",
            "fuel_type",
            "description",
            "description_fa",
            "description_en",
            "description_ar",
            "cover_image",
            "official_name",
            "official_name_fa",
            "official_name_en",
            "official_name_ar",
            "name_fa",
            "name_en",
            "name_ar",
            "display_name",
            "model_code",
            "chassis_code",
            "generation",
            "facelift",
            "body_style",
            "body_style_display",
            "manufacturer",
            "importer",
            "assembler",
            "country_of_origin",
            "country_of_assembly",
            "introduced_year",
            "iran_entry_year",
            "production_start_year",
            "production_end_year",
            "market_status",
            "market_status_display",
            "doors",
            "categories",
        )

    def get_trim(self, obj):
        return obj.trim.name if obj.trim_id else ""

    def get_trim_name(self, obj):
        return self.get_trim(obj)

    def get_cover_image(self, obj):
        request = self.context.get("request")
        image = obj.main_image
        return absolute_media_url(request, image)

    def get_description(self, obj):
        return localized(obj, "description")

    def get_official_name(self, obj):
        return localized(obj, "official_name")

    def get_display_name(self, obj):
        return obj.display_name


class TechnicalSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSpec
        exclude = ("id", "car")


class DimensionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimensions
        exclude = ("id", "car")


class FeatureSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(
        source="get_category_display", read_only=True
    )
    availability_display = serializers.CharField(
        source="get_availability_display", read_only=True
    )

    class Meta:
        model = Feature
        fields = (
            "id",
            "category",
            "category_display",
            "key",
            "name",
            "value",
            "availability",
            "availability_display",
        )


class MaintenanceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceItem
        fields = (
            "id",
            "title",
            "interval_km",
            "interval_months",
            "description",
            "estimated_cost",
        )


class FluidSpecSerializer(serializers.ModelSerializer):
    fluid_type_display = serializers.CharField(
        source="get_fluid_type_display", read_only=True
    )

    class Meta:
        model = FluidSpec
        fields = (
            "id",
            "fluid_type",
            "fluid_type_display",
            "specification",
            "grade",
            "capacity",
            "interval_km",
            "interval_months",
            "estimated_cost",
            "notes",
        )


class TireSpecSerializer(serializers.ModelSerializer):
    position_display = serializers.CharField(
        source="get_position_display", read_only=True
    )

    class Meta:
        model = TireSpec
        fields = (
            "id",
            "position",
            "position_display",
            "size",
            "pressure_psi",
            "load_index",
            "speed_rating",
            "rim_size",
            "rim_material",
        )


class BatterySpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatterySpec
        fields = ("id", "group_size", "voltage", "cca", "chemistry", "notes")


class ServiceScheduleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceScheduleItem
        fields = ("id", "mileage_km", "months", "tasks", "sort_order")


class OBDCodeSerializer(serializers.ModelSerializer):
    severity_display = serializers.CharField(
        source="get_severity_display", read_only=True
    )

    class Meta:
        model = OBDCode
        fields = (
            "id",
            "code",
            "title",
            "description",
            "severity",
            "severity_display",
        )


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = (
            "id",
            "name",
            "oem_number",
            "category",
            "is_consumable",
            "interval_km",
            "interval_months",
            "estimated_cost",
            "notes",
        )


class CommonFailureSerializer(serializers.ModelSerializer):
    area_display = serializers.CharField(source="get_area_display", read_only=True)
    severity_display = serializers.CharField(
        source="get_severity_display", read_only=True
    )
    likelihood_display = serializers.CharField(
        source="get_likelihood_display", read_only=True
    )

    class Meta:
        model = CommonFailure
        fields = (
            "id",
            "area",
            "area_display",
            "title",
            "severity",
            "severity_display",
            "likelihood",
            "likelihood_display",
            "repair_cost_min",
            "repair_cost_max",
            "currency",
            "symptoms",
            "notes",
        )


class MarketInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketInfo
        exclude = ("id", "car")


class SuspensionSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuspensionSpec
        exclude = ("id", "car")


class BrakeSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrakeSpec
        exclude = ("id", "car")


class WheelSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = WheelSpec
        exclude = ("id", "car")


class CabinSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = CabinSpec
        exclude = ("id", "car")


class MultimediaSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultimediaSpec
        exclude = ("id", "car")


class CarPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPrice
        fields = (
            "id",
            "label",
            "amount",
            "currency",
            "source",
            "notes",
            "recorded_at",
            "year_for_price",
            "mileage_km",
        )


class CarPhotoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = CarPhoto
        fields = ("id", "image", "caption", "sort_order")

    def get_image(self, obj):
        return absolute_media_url(self.context.get("request"), obj.image)


class DealerSerializer(serializers.ModelSerializer):
    brand_ids = serializers.PrimaryKeyRelatedField(
        source="brands", many=True, read_only=True
    )
    brand_names = serializers.SlugRelatedField(
        source="brands", many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Dealer
        fields = (
            "id",
            "name",
            "city",
            "address",
            "phone",
            "website",
            "brand_ids",
            "brand_names",
            "is_published",
        )


class RepairShopSerializer(serializers.ModelSerializer):
    brand_ids = serializers.PrimaryKeyRelatedField(
        source="brands", many=True, read_only=True
    )
    brand_names = serializers.SlugRelatedField(
        source="brands", many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = RepairShop
        fields = (
            "id",
            "name",
            "city",
            "address",
            "phone",
            "website",
            "brand_ids",
            "brand_names",
            "is_published",
        )


class PublicCarDetailSerializer(PublicCarSerializer):
    technical_spec = TechnicalSpecSerializer(read_only=True)
    dimensions = DimensionsSerializer(read_only=True)
    suspension = SuspensionSpecSerializer(read_only=True)
    brakes = BrakeSpecSerializer(read_only=True)
    wheels = WheelSpecSerializer(read_only=True)
    cabin = CabinSpecSerializer(read_only=True)
    multimedia = MultimediaSpecSerializer(read_only=True)
    market_info = MarketInfoSerializer(read_only=True)
    features = FeatureSerializer(many=True, read_only=True)
    maintenance = MaintenanceItemSerializer(
        source="maintenance_items", many=True, read_only=True
    )
    fluids = FluidSpecSerializer(many=True, read_only=True)
    tires = TireSpecSerializer(many=True, read_only=True)
    batteries = BatterySpecSerializer(many=True, read_only=True)
    service_schedule = ServiceScheduleItemSerializer(many=True, read_only=True)
    obd_codes = OBDCodeSerializer(
        source="model.obd_codes", many=True, read_only=True
    )
    parts = PartSerializer(many=True, read_only=True)
    common_failures = CommonFailureSerializer(many=True, read_only=True)
    prices = CarPriceSerializer(many=True, read_only=True)
    images = CarPhotoSerializer(source="photos", many=True, read_only=True)
    dealers = serializers.SerializerMethodField()
    repair_shops = serializers.SerializerMethodField()

    class Meta(PublicCarSerializer.Meta):
        fields = PublicCarSerializer.Meta.fields + (
            "technical_spec",
            "dimensions",
            "suspension",
            "brakes",
            "wheels",
            "cabin",
            "multimedia",
            "market_info",
            "features",
            "maintenance",
            "fluids",
            "tires",
            "batteries",
            "service_schedule",
            "obd_codes",
            "parts",
            "common_failures",
            "prices",
            "images",
            "dealers",
            "repair_shops",
        )

    def get_dealers(self, obj):
        qs = Dealer.objects.filter(
            is_published=True, brands=obj.model.brand
        ).distinct()
        return DealerSerializer(qs, many=True, context=self.context).data

    def get_repair_shops(self, obj):
        qs = RepairShop.objects.filter(
            is_published=True, brands=obj.model.brand
        ).distinct()
        return RepairShopSerializer(qs, many=True, context=self.context).data


class PublicYoutubeVideoSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = YoutubeVideo
        fields = (
            "id",
            "title",
            "youtube_id",
            "description",
            "cover_image",
            "thumbnail_url",
            "published_at",
            "embed_url",
        )

    def get_cover_image(self, obj):
        request = self.context.get("request")
        return absolute_media_url(request, obj.cover_image)

    def get_thumbnail_url(self, obj):
        if obj.cover_image:
            return self.get_cover_image(obj)
        return obj.thumbnail_url


class PublicPriceReferenceSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = PriceReference
        fields = (
            "id",
            "title",
            "title_fa",
            "title_en",
            "title_ar",
            "category",
            "category_fa",
            "category_en",
            "category_ar",
            "amount",
            "currency",
            "notes",
            "notes_fa",
            "notes_en",
            "notes_ar",
            "source",
            "source_fa",
            "source_en",
            "source_ar",
            "cover_image",
            "images",
            "updated_at",
        )

    def get_title(self, obj):
        return localized(obj, "title")

    def get_category(self, obj):
        return localized(obj, "category")

    def get_notes(self, obj):
        return localized(obj, "notes")

    def get_source(self, obj):
        return localized(obj, "source")

    def get_cover_image(self, obj):
        request = self.context.get("request")
        return absolute_media_url(request, obj.main_image)

    def get_images(self, obj):
        request = self.context.get("request")
        return [
            absolute_media_url(request, photo.image)
            for photo in obj.photos.all()
            if photo.image
        ]


class PublicListingSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    seller_username = serializers.CharField(source="seller.username", read_only=True)
    brand = serializers.CharField(
        source="car_model.brand.name", read_only=True, allow_null=True
    )
    brand_id = serializers.IntegerField(
        source="car_model.brand_id", read_only=True, allow_null=True
    )
    model_name = serializers.CharField(
        source="car_model.name", read_only=True, allow_null=True
    )
    car_model_id = serializers.IntegerField(read_only=True, allow_null=True)

    class Meta:
        model = Listing
        fields = (
            "id",
            "title",
            "title_fa",
            "title_en",
            "title_ar",
            "description",
            "description_fa",
            "description_en",
            "description_ar",
            "cover_image",
            "images",
            "price",
            "currency",
            "brand",
            "brand_id",
            "model_name",
            "car_model_id",
            "trim",
            "year",
            "mileage_km",
            "city",
            "status",
            "seller_username",
            "created_at",
        )

    def get_title(self, obj):
        return localized(obj, "title")

    def get_description(self, obj):
        return localized(obj, "description")

    def get_cover_image(self, obj):
        request = self.context.get("request")
        return absolute_media_url(request, obj.main_image)

    def get_images(self, obj):
        request = self.context.get("request")
        return [
            absolute_media_url(request, photo.image)
            for photo in obj.photos.all()
            if photo.image
        ]


class PublicEmergencyServiceSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    coverage_notes = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = EmergencyService
        fields = (
            "id",
            "name",
            "name_fa",
            "name_en",
            "name_ar",
            "description",
            "description_fa",
            "description_en",
            "description_ar",
            "coverage_notes",
            "coverage_notes_fa",
            "coverage_notes_en",
            "coverage_notes_ar",
            "cover_image",
            "is_active",
        )

    def get_name(self, obj):
        return localized(obj, "name")

    def get_description(self, obj):
        return localized(obj, "description")

    def get_coverage_notes(self, obj):
        return localized(obj, "coverage_notes")

    def get_cover_image(self, obj):
        request = self.context.get("request")
        return absolute_media_url(request, obj.cover_image)


class PublicStorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = (
            "id",
            "title",
            "title_fa",
            "title_en",
            "title_ar",
            "slug",
            "excerpt",
            "excerpt_fa",
            "excerpt_en",
            "excerpt_ar",
            "cover_image",
            "author_name",
            "published_at",
        )

    def get_title(self, obj):
        return localized(obj, "title")

    def get_excerpt(self, obj):
        return localized(obj, "excerpt")

    def get_cover_image(self, obj):
        request = self.context.get("request")
        return absolute_media_url(request, obj.cover_image)

    def get_author_name(self, obj):
        if obj.author_id and obj.author:
            return obj.author.get_username()
        return None
