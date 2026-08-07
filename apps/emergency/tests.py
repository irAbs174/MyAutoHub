from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import SavedLocation
from apps.core.i18n_content import tri_fields
from apps.emergency.models import (
    EmergencyBuzz,
    EmergencyRequest,
    EmergencyService,
    RequestStatus,
)
from apps.emergency.services import (
    add_public_review,
    buzz_request,
    create_emergency_request,
    transition_request,
)

User = get_user_model()


class EmergencyServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("driver", password="pass12345")
        self.other = User.objects.create_user("other", password="pass12345")
        self.operator = User.objects.create_user("op", password="pass12345")
        self.admin_op = User.objects.create_user(
            "adminop", password="pass12345", is_staff=True
        )
        group, _ = Group.objects.get_or_create(name="emergency_operators")
        self.operator.groups.add(group)
        self.admin_op.groups.add(group)
        self.service = EmergencyService.objects.create(
            **tri_fields(name="Towing", description="Flatbed tow")
        )
        self.location = SavedLocation.objects.create(
            user=self.user,
            label="Home",
            latitude=Decimal("35.689200"),
            longitude=Decimal("51.389000"),
        )

    def test_submit_requires_location(self):
        with self.assertRaises(ValidationError):
            create_emergency_request(
                requester=self.user,
                service=self.service,
                description="Need help",
            )

    def test_submit_starts_wait_for_accept(self):
        req = create_emergency_request(
            requester=self.user,
            service=self.service,
            description="Battery dead",
            saved_location=self.location,
        )
        self.assertEqual(req.status, RequestStatus.WAIT_FOR_ACCEPT)
        self.assertEqual(req.transitions.count(), 1)

    def test_operator_can_verify_to_processing(self):
        req = create_emergency_request(
            requester=self.user,
            service=self.service,
            description="Flat tire",
            latitude=Decimal("35.7"),
            longitude=Decimal("51.4"),
        )
        transition_request(
            emergency_request=req,
            actor=self.operator,
            to_status=RequestStatus.PROCESSING,
            note="On the way",
        )
        req.refresh_from_db()
        self.assertEqual(req.status, RequestStatus.PROCESSING)

    def test_regular_user_cannot_verify(self):
        req = create_emergency_request(
            requester=self.user,
            service=self.service,
            description="Locked out",
            saved_location=self.location,
        )
        with self.assertRaises(PermissionDenied):
            transition_request(
                emergency_request=req,
                actor=self.other,
                to_status=RequestStatus.PROCESSING,
            )

    def test_only_admin_operator_can_finish(self):
        req = create_emergency_request(
            requester=self.user,
            service=self.service,
            description="Need jump",
            saved_location=self.location,
        )
        transition_request(
            emergency_request=req,
            actor=self.operator,
            to_status=RequestStatus.PROCESSING,
        )
        with self.assertRaises(PermissionDenied):
            transition_request(
                emergency_request=req,
                actor=self.operator,
                to_status=RequestStatus.FINISH_SUCCESS,
            )
        transition_request(
            emergency_request=req,
            actor=self.admin_op,
            to_status=RequestStatus.FINISH_SUCCESS,
        )
        req.refresh_from_db()
        self.assertEqual(req.status, RequestStatus.FINISH_SUCCESS)

    def test_superuser_can_accept_and_finish_without_operator_group(self):
        superuser = User.objects.create_user(
            "super",
            password="pass12345",
            is_staff=True,
            is_superuser=True,
        )
        req = create_emergency_request(
            requester=self.user,
            service=self.service,
            description="Need tow",
            saved_location=self.location,
        )
        transition_request(
            emergency_request=req,
            actor=superuser,
            to_status=RequestStatus.PROCESSING,
        )
        req.refresh_from_db()
        self.assertEqual(req.status, RequestStatus.PROCESSING)
        transition_request(
            emergency_request=req,
            actor=superuser,
            to_status=RequestStatus.FINISH_SUCCESS,
        )
        req.refresh_from_db()
        self.assertEqual(req.status, RequestStatus.FINISH_SUCCESS)

    def test_review_only_after_finished(self):
        req = create_emergency_request(
            requester=self.user,
            service=self.service,
            description="Out of fuel",
            saved_location=self.location,
        )
        with self.assertRaises(ValidationError):
            add_public_review(
                emergency_request=req,
                user=self.user,
                comment="Great help",
            )
        transition_request(
            emergency_request=req,
            actor=self.operator,
            to_status=RequestStatus.PROCESSING,
        )
        transition_request(
            emergency_request=req,
            actor=self.admin_op,
            to_status=RequestStatus.FINISH_SUCCESS,
        )
        add_public_review(
            emergency_request=req,
            user=self.user,
            comment="Quick and friendly",
            rating=5,
        )
        req.refresh_from_db()
        self.assertEqual(req.review_comment, "Quick and friendly")

    def test_buzz_creates_notification(self):
        req = create_emergency_request(
            requester=self.user,
            service=self.service,
            description="Accident nearby",
            saved_location=self.location,
        )
        buzz = buzz_request(emergency_request=req, user=self.user)
        self.assertFalse(buzz.seen_by_operators)
        self.assertEqual(EmergencyBuzz.objects.filter(request=req).count(), 1)

    def test_submit_view_requires_login(self):
        url = reverse("emergency:submit")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username="driver", password="pass12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_api_submit_and_search(self):
        self.client.login(username="driver", password="pass12345")
        response = self.client.post(
            reverse("api_submit"),
            data={
                "service_id": self.service.id,
                "description": "API help",
                "latitude": "35.689200",
                "longitude": "51.389000",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], RequestStatus.WAIT_FOR_ACCEPT)
        search = self.client.get(reverse("api_search"))
        self.assertEqual(search.status_code, 200)
        self.assertTrue(len(search.json()) >= 1)
