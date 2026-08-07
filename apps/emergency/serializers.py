from rest_framework import serializers
from django.utils.translation import gettext as _

from apps.accounts.models import SavedLocation
from apps.core.i18n_content import localized

from .models import EmergencyBuzz, EmergencyRequest, EmergencyService, EmergencyTransition


class EmergencyServiceSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    coverage_notes = serializers.SerializerMethodField()

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
            "is_active",
        )

    def get_name(self, obj):
        return localized(obj, "name")

    def get_description(self, obj):
        return localized(obj, "description")

    def get_coverage_notes(self, obj):
        return localized(obj, "coverage_notes")


class EmergencyTransitionSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor.username", read_only=True)

    class Meta:
        model = EmergencyTransition
        fields = (
            "id",
            "from_status",
            "to_status",
            "actor",
            "actor_username",
            "note",
            "created_at",
        )


class EmergencyBuzzSerializer(serializers.ModelSerializer):
    from_username = serializers.CharField(source="from_user.username", read_only=True)

    class Meta:
        model = EmergencyBuzz
        fields = ("id", "from_user", "from_username", "seen_by_operators", "created_at")


class EmergencyRequestSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.name", read_only=True)
    requester_username = serializers.CharField(source="requester.username", read_only=True)
    unread_buzz_count = serializers.SerializerMethodField()
    transitions = EmergencyTransitionSerializer(many=True, read_only=True)

    class Meta:
        model = EmergencyRequest
        fields = (
            "id",
            "requester",
            "requester_username",
            "service",
            "service_name",
            "status",
            "saved_location",
            "latitude",
            "longitude",
            "description",
            "review_comment",
            "review_rating",
            "reviewed_at",
            "unread_buzz_count",
            "transitions",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "requester",
            "status",
            "review_comment",
            "review_rating",
            "reviewed_at",
            "created_at",
            "updated_at",
        )

    def get_unread_buzz_count(self, obj):
        return obj.get_unread_buzz_count()


class SubmitEmergencySerializer(serializers.Serializer):
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=EmergencyService.objects.filter(is_active=True),
        source="service",
    )
    description = serializers.CharField()
    saved_location_id = serializers.PrimaryKeyRelatedField(
        queryset=SavedLocation.objects.all(),
        source="saved_location",
        required=False,
        allow_null=True,
    )
    latitude = serializers.DecimalField(
        max_digits=9, decimal_places=6, required=False, allow_null=True
    )
    longitude = serializers.DecimalField(
        max_digits=9, decimal_places=6, required=False, allow_null=True
    )

    def validate(self, attrs):
        saved = attrs.get("saved_location")
        lat = attrs.get("latitude")
        lng = attrs.get("longitude")
        request = self.context["request"]
        if saved and saved.user_id != request.user.id:
            raise serializers.ValidationError(
                {"saved_location_id": _("That location does not belong to you.")}
            )
        if not saved and (lat is None or lng is None):
            raise serializers.ValidationError(
                _("Provide saved_location_id or latitude and longitude.")
            )
        return attrs


class VerifyEmergencySerializer(serializers.Serializer):
    to_status = serializers.CharField()
    note = serializers.CharField(required=False, allow_blank=True, default="")


class ReviewSerializer(serializers.Serializer):
    review_comment = serializers.CharField()
    review_rating = serializers.IntegerField(required=False, min_value=1, max_value=5)
