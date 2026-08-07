from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import SavedLocation
from apps.core.i18n_content import localized


class RequestStatus(models.TextChoices):
    WAIT_FOR_ACCEPT = "wait_for_accept", _("Waiting for accept")
    PROCESSING = "processing_request", _("Processing")
    FINISH_SUCCESS = "finish_success", _("Finished successfully")
    FINISH_FAILED = "finish_failed", _("Finished failed")
    CANCELLED = "cancelled", _("Cancelled")


TERMINAL_STATUSES = {
    RequestStatus.FINISH_SUCCESS,
    RequestStatus.FINISH_FAILED,
    RequestStatus.CANCELLED,
}

FINISHED_FOR_REVIEW = {
    RequestStatus.FINISH_SUCCESS,
    RequestStatus.FINISH_FAILED,
}


class EmergencyService(models.Model):
    name_fa = models.CharField(max_length=120, verbose_name=_("Name (فارسی)"))
    name_en = models.CharField(max_length=120, verbose_name=_("Name (English)"))
    name_ar = models.CharField(max_length=120, verbose_name=_("Name (العربية)"))
    description_fa = models.TextField(blank=True, verbose_name=_("Description (فارسی)"))
    description_en = models.TextField(blank=True, verbose_name=_("Description (English)"))
    description_ar = models.TextField(blank=True, verbose_name=_("Description (العربية)"))
    coverage_notes_fa = models.TextField(
        blank=True, verbose_name=_("Coverage notes (فارسی)")
    )
    coverage_notes_en = models.TextField(
        blank=True, verbose_name=_("Coverage notes (English)")
    )
    coverage_notes_ar = models.TextField(
        blank=True, verbose_name=_("Coverage notes (العربية)")
    )
    cover_image = models.ImageField(upload_to="emergency/covers/", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name_fa"]

    def __str__(self):
        return self.name

    @property
    def name(self):
        return localized(self, "name")

    @property
    def description(self):
        return localized(self, "description")

    @property
    def coverage_notes(self):
        return localized(self, "coverage_notes")


class EmergencyRequest(models.Model):
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="emergency_requests",
    )
    service = models.ForeignKey(
        EmergencyService,
        on_delete=models.PROTECT,
        related_name="requests",
    )
    status = models.CharField(
        max_length=32,
        choices=RequestStatus.choices,
        default=RequestStatus.WAIT_FOR_ACCEPT,
        db_index=True,
    )
    saved_location = models.ForeignKey(
        SavedLocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="emergency_requests",
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    description = models.TextField()
    review_comment = models.TextField(blank=True)
    review_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} {self.service} ({self.status})"

    def clean(self):
        has_saved = self.saved_location_id is not None
        has_coords = self.latitude is not None and self.longitude is not None
        if not has_saved and not has_coords:
            raise ValidationError(
                _("Select a saved location or provide map coordinates.")
            )
        if self.review_rating is not None and not (1 <= self.review_rating <= 5):
            raise ValidationError({"review_rating": _("Rating must be between 1 and 5.")})

    def resolve_coordinates(self):
        if self.saved_location_id:
            return self.saved_location.latitude, self.saved_location.longitude
        return self.latitude, self.longitude

    def get_unread_buzz_count(self):
        # Prefer queryset annotation when present (avoids property/annotation clash).
        annotated = self.__dict__.get("unread_buzz_count")
        if annotated is not None:
            return annotated
        return self.buzzes.filter(seen_by_operators=False).count()

    def can_review(self):
        return self.status in FINISHED_FOR_REVIEW and not self.review_comment


class EmergencyTransition(models.Model):
    request = models.ForeignKey(
        EmergencyRequest,
        on_delete=models.CASCADE,
        related_name="transitions",
    )
    from_status = models.CharField(max_length=32, choices=RequestStatus.choices)
    to_status = models.CharField(max_length=32, choices=RequestStatus.choices)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="emergency_transitions",
    )
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.from_status} → {self.to_status}"


class EmergencyBuzz(models.Model):
    request = models.ForeignKey(
        EmergencyRequest,
        on_delete=models.CASCADE,
        related_name="buzzes",
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="emergency_buzzes",
    )
    seen_by_operators = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Buzz on #{self.request_id} by {self.from_user}"
