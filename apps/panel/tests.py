from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from apps.cars.models import Brand, Car, CarModel, Trim
from apps.core.i18n_content import tri_fields
from apps.emergency.models import EmergencyRequest, EmergencyService, RequestStatus
from apps.stories.models import Story
from apps.youtube.models import YoutubeVideo

User = get_user_model()


def _empty_formset(prefix, extra=0):
    return {
        f"{prefix}-TOTAL_FORMS": str(extra),
        f"{prefix}-INITIAL_FORMS": "0",
        f"{prefix}-MIN_NUM_FORMS": "0",
        f"{prefix}-MAX_NUM_FORMS": "1000",
    }


def _car_related_post_extras():
    data = {}
    for field in (
        "engine",
        "displacement_cc",
        "cylinders",
        "transmission",
        "drivetrain",
        "top_speed_kmh",
        "accel_0_100",
        "economy_city",
        "economy_highway",
        "emission_standard",
        "notes",
    ):
        data[f"spec-{field}"] = ""
    for field in (
        "length_mm",
        "width_mm",
        "height_mm",
        "wheelbase_mm",
        "curb_weight_kg",
        "cargo_l",
        "seats",
        "ground_clearance_mm",
        "fuel_tank_l",
    ):
        data[f"dims-{field}"] = ""
    data.update(_empty_formset("photos", extra=1))
    data["photos-0-image"] = ""
    data["photos-0-caption"] = ""
    data["photos-0-sort_order"] = "0"
    for prefix in (
        "features",
        "maintenance",
        "fluids",
        "tires",
        "batteries",
        "service",
        "parts",
        "prices",
    ):
        data.update(_empty_formset(prefix, extra=0))
    return data


class PanelAccessTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            "staffer", password="pass12345", is_staff=True
        )
        self.user = User.objects.create_user("member", password="pass12345")
        self.service = EmergencyService.objects.create(**tri_fields(name="Tow"))

    def test_anonymous_redirects_to_login(self):
        response = self.client.get(reverse("panel:overview"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_non_staff_forbidden(self):
        self.client.login(username="member", password="pass12345")
        response = self.client.get(reverse("panel:overview"))
        self.assertEqual(response.status_code, 403)

    def test_panel_has_language_switcher(self):
        self.client.login(username="staffer", password="pass12345")
        response = self.client.get(reverse("panel:overview"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'action="{0}"'.format(reverse("set_language")))
        self.assertContains(response, 'name="language"')

    def test_staff_can_open_overview(self):
        self.client.login(username="staffer", password="pass12345")
        response = self.client.get(reverse("panel:overview"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="admin-index"')
        self.assertContains(response, reverse("panel:listing_list"))
        self.assertContains(response, reverse("panel:price_list"))

    def test_non_staff_forbidden_on_content_lists(self):
        self.client.login(username="member", password="pass12345")
        for name in ("panel:car_list", "panel:youtube_list", "panel:story_list"):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 403, name)

    def test_staff_can_open_content_lists(self):
        self.client.login(username="staffer", password="pass12345")
        for name in ("panel:car_list", "panel:youtube_list", "panel:story_list"):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)


class PanelEmergencyTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            "adminop", password="pass12345", is_staff=True
        )
        group, _ = Group.objects.get_or_create(name="emergency_operators")
        self.staff.groups.add(group)
        self.requester = User.objects.create_user("driver", password="pass12345")
        self.service = EmergencyService.objects.create(**tri_fields(name="Battery"))
        self.emergency = EmergencyRequest.objects.create(
            requester=self.requester,
            service=self.service,
            description="Flat battery",
            latitude="35.689200",
            longitude="51.389000",
            status=RequestStatus.WAIT_FOR_ACCEPT,
        )
        self.client.login(username="adminop", password="pass12345")

    def test_queue_lists_request(self):
        response = self.client.get(reverse("panel:emergency_request_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Battery")
        self.assertContains(response, f"#{self.emergency.pk}")

    def test_service_create(self):
        response = self.client.post(
            reverse("panel:emergency_service_create"),
            {
                "name_fa": "Fuel delivery",
                "name_en": "Fuel delivery",
                "name_ar": "Fuel delivery",
                "description_fa": "Bring petrol",
                "description_en": "Bring petrol",
                "description_ar": "Bring petrol",
                "coverage_notes_fa": "City only",
                "coverage_notes_en": "City only",
                "coverage_notes_ar": "City only",
                "is_active": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            EmergencyService.objects.filter(name_en="Fuel delivery").exists()
        )

    def test_accept_via_panel(self):
        response = self.client.post(
            reverse("panel:emergency_request_verify", args=[self.emergency.pk]),
            {
                "to_status": RequestStatus.PROCESSING,
                "note": "On the way",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.emergency.refresh_from_db()
        self.assertEqual(self.emergency.status, RequestStatus.PROCESSING)


class PanelSuperuserTests(TestCase):
    def setUp(self):
        self.requester = User.objects.create_user("driver", password="pass12345")
        self.service = EmergencyService.objects.create(**tri_fields(name="Battery"))
        self.emergency = EmergencyRequest.objects.create(
            requester=self.requester,
            service=self.service,
            description="Flat battery",
            latitude="35.689200",
            longitude="51.389000",
            status=RequestStatus.WAIT_FOR_ACCEPT,
        )

    def test_staff_without_operator_group_cannot_accept(self):
        User.objects.create_user("staffer", password="pass12345", is_staff=True)
        self.client.login(username="staffer", password="pass12345")
        response = self.client.post(
            reverse("panel:emergency_request_verify", args=[self.emergency.pk]),
            {
                "to_status": RequestStatus.PROCESSING,
                "note": "Should fail",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.emergency.refresh_from_db()
        self.assertEqual(self.emergency.status, RequestStatus.WAIT_FOR_ACCEPT)

    def test_superuser_without_operator_group_can_accept(self):
        User.objects.create_user(
            "super",
            password="pass12345",
            is_staff=True,
            is_superuser=True,
        )
        self.client.login(username="super", password="pass12345")
        response = self.client.post(
            reverse("panel:emergency_request_verify", args=[self.emergency.pk]),
            {
                "to_status": RequestStatus.PROCESSING,
                "note": "On the way",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.emergency.refresh_from_db()
        self.assertEqual(self.emergency.status, RequestStatus.PROCESSING)


class PanelContentTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            "editor", password="pass12345", is_staff=True
        )
        self.brand = Brand.objects.create(name="Toyota", country="Japan")
        self.car_model = CarModel.objects.create(brand=self.brand, name="Corolla")
        self.client.login(username="editor", password="pass12345")

    def test_car_create_and_edit(self):
        trim_se = Trim.objects.create(car_model=self.car_model, name="SE")
        trim_xse = Trim.objects.create(car_model=self.car_model, name="XSE")
        extras = _car_related_post_extras()
        response = self.client.post(
            reverse("panel:car_create"),
            {
                "model": self.car_model.pk,
                "year": 2024,
                "trim": trim_se.pk,
                "horsepower": 169,
                "fuel_type": "gasoline",
                "description": "Compact sedan",
                "is_published": True,
                **extras,
            },
        )
        self.assertEqual(response.status_code, 302)
        car = Car.objects.get(model=self.car_model, year=2024)
        self.assertEqual(car.trim.name, "SE")

        response = self.client.post(
            reverse("panel:car_edit", args=[car.pk]),
            {
                "model": self.car_model.pk,
                "year": 2024,
                "trim": trim_xse.pk,
                "horsepower": 169,
                "fuel_type": "gasoline",
                "description": "Updated",
                "is_published": True,
                **extras,
            },
        )
        self.assertEqual(response.status_code, 302)
        car.refresh_from_db()
        self.assertEqual(car.trim.name, "XSE")
        self.assertEqual(car.description, "Updated")

    def test_brand_and_model_create(self):
        response = self.client.post(
            reverse("panel:brand_create"),
            {"name": "Honda", "country": "Japan"},
        )
        self.assertEqual(response.status_code, 302)
        brand = Brand.objects.get(name="Honda")

        response = self.client.post(
            reverse("panel:car_model_create"),
            {"brand": brand.pk, "name": "Civic"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CarModel.objects.filter(brand=brand, name="Civic").exists())

    def test_youtube_create_and_edit(self):
        response = self.client.post(
            reverse("panel:youtube_create"),
            {
                "title": "Track day",
                "youtube_id": "dQw4w9WgXcQ",
                "description": "Fun laps",
                "is_published": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        video = YoutubeVideo.objects.get(youtube_id="dQw4w9WgXcQ")

        response = self.client.post(
            reverse("panel:youtube_edit", args=[video.pk]),
            {
                "title": "Track day highlights",
                "youtube_id": "dQw4w9WgXcQ",
                "description": "Best laps",
                "is_published": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        video.refresh_from_db()
        self.assertEqual(video.title, "Track day highlights")
        self.assertFalse(video.is_published)

    def test_story_create_and_edit(self):
        response = self.client.post(
            reverse("panel:story_create"),
            {
                "title_fa": "داستان",
                "title_en": "Our launch",
                "title_ar": "قصتنا",
                "excerpt_fa": "",
                "excerpt_en": "How we started",
                "excerpt_ar": "",
                "body_fa": "متن فارسی",
                "body_en": "English body",
                "body_ar": "النص العربي",
                "slug": "",
                "author": "",
                "is_published": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        story = Story.objects.get(title_en="Our launch")
        self.assertEqual(story.author_id, self.staff.pk)
        self.assertEqual(story.slug, "our-launch")

        response = self.client.post(
            reverse("panel:story_edit", args=[story.pk]),
            {
                "title_fa": "داستان",
                "title_en": "Our launch updated",
                "title_ar": "قصتنا",
                "excerpt_fa": "",
                "excerpt_en": "How we started",
                "excerpt_ar": "",
                "body_fa": "متن فارسی",
                "body_en": "English body revised",
                "body_ar": "النص العربي",
                "slug": story.slug,
                "author": self.staff.pk,
                "is_published": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        story.refresh_from_db()
        self.assertEqual(story.title_en, "Our launch updated")
        self.assertEqual(story.body_en, "English body revised")

    def test_listing_and_price_create(self):
        from apps.marketplace.models import Listing
        from apps.pricing.models import PriceReference

        response = self.client.get(reverse("panel:overview"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="admin-index"')
        self.assertContains(response, reverse("panel:listing_list"))
        self.assertContains(response, reverse("panel:price_list"))

        response = self.client.post(
            reverse("panel:listing_create"),
            {
                "seller": self.staff.pk,
                "title_fa": "فروش",
                "title_en": "For sale",
                "title_ar": "للبيع",
                "description_fa": "",
                "description_en": "Nice car",
                "description_ar": "",
                "price": "120000000",
                "currency": "تومان",
                "car_model": self.car_model.pk,
                "trim": "",
                "year": 2020,
                "mileage_km": 40000,
                "city": "Tehran",
                "status": "active",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Listing.objects.filter(title_en="For sale").exists())

        response = self.client.post(
            reverse("panel:price_create"),
            {
                "title_fa": "تعویض روغن",
                "title_en": "Oil change",
                "title_ar": "تغيير الزيت",
                "category_fa": "سرویس",
                "category_en": "Service",
                "category_ar": "خدمة",
                "amount": "1500000",
                "currency": "تومان",
                "notes_fa": "",
                "notes_en": "",
                "notes_ar": "",
                "source_fa": "",
                "source_en": "",
                "source_ar": "",
                "is_published": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PriceReference.objects.filter(title_en="Oil change").exists())
