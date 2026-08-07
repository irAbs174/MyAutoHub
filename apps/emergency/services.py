from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from .models import (
    FINISHED_FOR_REVIEW,
    TERMINAL_STATUSES,
    EmergencyBuzz,
    EmergencyRequest,
    EmergencyTransition,
    RequestStatus,
)


def is_emergency_operator(user) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name=settings.EMERGENCY_OPERATORS_GROUP).exists()


def is_emergency_operator_admin(user) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return is_emergency_operator(user) and user.is_staff


ALLOWED_TRANSITIONS = {
    RequestStatus.WAIT_FOR_ACCEPT: {
        RequestStatus.PROCESSING,
        RequestStatus.CANCELLED,
    },
    RequestStatus.PROCESSING: {
        RequestStatus.FINISH_SUCCESS,
        RequestStatus.FINISH_FAILED,
        RequestStatus.CANCELLED,
    },
}


def _assert_transition_allowed(from_status: str, to_status: str) -> None:
    allowed = ALLOWED_TRANSITIONS.get(from_status, set())
    if to_status not in allowed:
        raise ValidationError(
            _("Cannot change status from %(from)s to %(to)s.")
            % {"from": from_status, "to": to_status}
        )


def _assert_actor_may_transition(user, from_status: str, to_status: str) -> None:
    if to_status == RequestStatus.PROCESSING:
        if not is_emergency_operator(user):
            raise PermissionDenied(_("Only emergency operators can accept requests."))
        return

    if to_status in (RequestStatus.FINISH_SUCCESS, RequestStatus.FINISH_FAILED):
        if not is_emergency_operator_admin(user):
            raise PermissionDenied(
                _("Only emergency operator administrators can finish requests.")
            )
        return

    if to_status == RequestStatus.CANCELLED:
        # Caller checks ownership separately for non-operators.
        return

    raise ValidationError(
        _("Unsupported target status: %(status)s") % {"status": to_status}
    )


@transaction.atomic
def create_emergency_request(*, requester, service, description, saved_location=None, latitude=None, longitude=None):
    request = EmergencyRequest(
        requester=requester,
        service=service,
        description=description,
        saved_location=saved_location,
        latitude=latitude,
        longitude=longitude,
        status=RequestStatus.WAIT_FOR_ACCEPT,
    )
    request.full_clean()
    request.save()
    EmergencyTransition.objects.create(
        request=request,
        from_status=RequestStatus.WAIT_FOR_ACCEPT,
        to_status=RequestStatus.WAIT_FOR_ACCEPT,
        actor=requester,
        note=_("Request submitted"),
    )
    return request


@transaction.atomic
def transition_request(*, emergency_request, actor, to_status, note=""):
    from_status = emergency_request.status
    if from_status in TERMINAL_STATUSES:
        raise ValidationError(_("This request is already closed."))

    _assert_transition_allowed(from_status, to_status)
    _assert_actor_may_transition(actor, from_status, to_status)

    if to_status == RequestStatus.CANCELLED:
        if emergency_request.requester_id != actor.id and not is_emergency_operator(actor):
            raise PermissionDenied(_("You can only cancel your own requests."))

    emergency_request.status = to_status
    emergency_request.save(update_fields=["status", "updated_at"])
    EmergencyTransition.objects.create(
        request=emergency_request,
        from_status=from_status,
        to_status=to_status,
        actor=actor,
        note=note,
    )
    if to_status == RequestStatus.PROCESSING:
        emergency_request.buzzes.filter(seen_by_operators=False).update(
            seen_by_operators=True
        )
    return emergency_request


@transaction.atomic
def buzz_request(*, emergency_request, user):
    if emergency_request.requester_id != user.id and not is_emergency_operator(user):
        raise PermissionDenied(_("You cannot buzz this request."))
    if emergency_request.status in TERMINAL_STATUSES:
        raise ValidationError(_("Cannot buzz a closed request."))
    return EmergencyBuzz.objects.create(request=emergency_request, from_user=user)


@transaction.atomic
def add_public_review(*, emergency_request, user, comment, rating=None):
    if emergency_request.requester_id != user.id:
        raise PermissionDenied(_("Only the requester can leave a review."))
    if emergency_request.status not in FINISHED_FOR_REVIEW:
        raise ValidationError(_("Reviews are only allowed after the request finishes."))
    if emergency_request.review_comment:
        raise ValidationError(_("A review was already submitted."))
    emergency_request.review_comment = comment
    emergency_request.review_rating = rating
    emergency_request.reviewed_at = timezone.now()
    emergency_request.full_clean()
    emergency_request.save(
        update_fields=["review_comment", "review_rating", "reviewed_at", "updated_at"]
    )
    return emergency_request
