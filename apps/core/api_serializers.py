from rest_framework import serializers

from apps.cars.models import Brand, Car
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
        fields = ("id", "name", "country")


class PublicCarSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="model.brand.name", read_only=True)
    brand_id = serializers.IntegerField(source="model.brand_id", read_only=True)
    model_name = serializers.CharField(source="model.name", read_only=True)
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = (
            "id",
            "brand",
            "brand_id",
            "model_name",
            "year",
            "trim",
            "horsepower",
            "fuel_type",
            "description",
            "cover_image",
        )

    def get_cover_image(self, obj):
        request = self.context.get("request")
        image = obj.main_image
        return absolute_media_url(request, image)


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
