from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from apps.cars.models import Brand, CarModel
from apps.core.i18n_content import tri_fields
from apps.marketplace.models import Currency, Listing, ListingInquiry, ListingStatus

User = get_user_model()


@override_settings(ALLOWED_HOSTS=["localhost", "testserver", "127.0.0.1"])
class MarketplaceBuySellTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST="localhost")
        self.seller = User.objects.create_user("seller1", password="pass12345")
        self.buyer = User.objects.create_user("buyer1", password="pass12345")
        self.brand = Brand.objects.create(name="Toyota", country="Japan")
        self.car_model = CarModel.objects.create(brand=self.brand, name="Corolla")
        self.listing = Listing.objects.create(
            seller=self.seller,
            **tri_fields(title="2018 Corolla", description="Clean daily driver"),
            car_model=self.car_model,
            trim="SE",
            price="12000.00",
            currency=Currency.TOMAN,
            year=2018,
            city="Tehran",
            status=ListingStatus.ACTIVE,
        )

    def test_browse_shows_active_listings(self):
        url = reverse("marketplace:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2018 Corolla")
        self.assertContains(response, "Toyota Corolla SE")
        self.assertContains(response, "marketplace/new/")

    def test_sell_form_currency_is_dropdown_default_toman(self):
        self.client.login(username="seller1", password="pass12345")
        response = self.client.get(reverse("marketplace:create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<select name="currency"')
        self.assertContains(response, '<select name="brand"')
        self.assertContains(response, '<select name="car_model"')
        self.assertContains(
            response,
            f'<option value="{Currency.TOMAN}" selected>',
            html=False,
        )
        self.assertContains(response, "Iran (تومان)")
        self.assertContains(response, 'id="brand-model-map"')
        self.assertContains(response, '"name": "Corolla"')

    def test_seller_can_create_listing(self):
        self.client.login(username="seller1", password="pass12345")
        url = reverse("marketplace:create")
        response = self.client.post(
            url,
            {
                "title_fa": "2020 Sportage",
                "title_en": "2020 Sportage",
                "title_ar": "2020 Sportage",
                "description_fa": "One owner",
                "description_en": "One owner",
                "description_ar": "One owner",
                "price": "18500",
                "currency": Currency.TOMAN,
                "year": "2020",
                "mileage_km": "45000",
                "city": "Karaj",
            },
        )
        self.assertEqual(response.status_code, 302)
        created = Listing.objects.get(title_en="2020 Sportage")
        self.assertEqual(created.seller_id, self.seller.id)
        self.assertEqual(created.currency, Currency.TOMAN)
        self.assertEqual(created.status, ListingStatus.ACTIVE)

    def test_seller_can_create_with_brand_model_trim(self):
        self.client.login(username="seller1", password="pass12345")
        response = self.client.post(
            reverse("marketplace:create"),
            {
                "title_en": "Toyota Corolla LE",
                "description_en": "Low mileage",
                "brand": str(self.brand.pk),
                "car_model": str(self.car_model.pk),
                "trim": "LE",
                "price": "15000",
                "currency": Currency.TOMAN,
                "year": "2019",
            },
        )
        self.assertEqual(response.status_code, 302)
        created = Listing.objects.get(title_en="Toyota Corolla LE")
        self.assertEqual(created.car_model_id, self.car_model.pk)
        self.assertEqual(created.trim, "LE")
        self.assertEqual(created.car_identity, "Toyota Corolla LE")
        detail = self.client.get(reverse("marketplace:detail", args=[created.pk]))
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, "Toyota Corolla LE")

    def test_create_rejects_model_from_other_brand(self):
        other_brand = Brand.objects.create(name="Kia")
        other_model = CarModel.objects.create(brand=other_brand, name="Sportage")
        self.client.login(username="seller1", password="pass12345")
        response = self.client.post(
            reverse("marketplace:create"),
            {
                "title_en": "Mismatched",
                "description_en": "Should fail",
                "brand": str(self.brand.pk),
                "car_model": str(other_model.pk),
                "price": "10000",
                "currency": Currency.TOMAN,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertFalse(Listing.objects.filter(title_en="Mismatched").exists())

    def test_seller_can_create_with_one_language_only(self):
        self.client.login(username="seller1", password="pass12345")
        response = self.client.post(
            reverse("marketplace:create"),
            {
                "title_fa": "پژو ۲۰۶",
                "description_fa": "یک مالک، آماده معامله",
                "price": "9200",
                "currency": Currency.TOMAN,
            },
        )
        self.assertEqual(response.status_code, 302)
        created = Listing.objects.get(title_fa="پژو ۲۰۶")
        self.assertEqual(created.title_en, "")
        self.assertEqual(created.description_en, "")
        self.assertEqual(created.title, "پژو ۲۰۶")

    def test_create_requires_at_least_one_language_pair(self):
        self.client.login(username="seller1", password="pass12345")
        response = self.client.post(
            reverse("marketplace:create"),
            {
                "title_fa": "Only title",
                "price": "1000",
                "currency": Currency.TOMAN,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertFalse(Listing.objects.filter(title_fa="Only title").exists())

    def test_buyer_can_message_seller(self):
        self.client.login(username="buyer1", password="pass12345")
        url = reverse("marketplace:inquire", args=[self.listing.pk])
        response = self.client.post(
            url,
            {"message": "Is this still available?", "contact_phone": "09120000000"},
        )
        self.assertEqual(response.status_code, 302)
        inquiry = ListingInquiry.objects.get(listing=self.listing)
        self.assertEqual(inquiry.buyer_id, self.buyer.id)
        self.assertIn("available", inquiry.message)

    def test_seller_cannot_inquire_own_listing(self):
        self.client.login(username="seller1", password="pass12345")
        url = reverse("marketplace:inquire", args=[self.listing.pk])
        response = self.client.post(url, {"message": "noop"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ListingInquiry.objects.count(), 0)

    def test_seller_can_mark_sold(self):
        self.client.login(username="seller1", password="pass12345")
        url = reverse("marketplace:mark_sold", args=[self.listing.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.status, ListingStatus.SOLD)
        browse = self.client.get(reverse("marketplace:list"))
        self.assertNotContains(browse, "2018 Corolla")

    def test_my_listings_requires_login(self):
        response = self.client.get(reverse("marketplace:mine"))
        self.assertEqual(response.status_code, 302)

    def test_seller_can_upload_multiple_photos(self):
        import base64

        from django.core.files.uploadedfile import SimpleUploadedFile

        png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        )
        self.client.login(username="seller1", password="pass12345")
        img1 = SimpleUploadedFile("front.png", png, content_type="image/png")
        img2 = SimpleUploadedFile("side.png", png, content_type="image/png")
        response = self.client.post(
            reverse("marketplace:create"),
            {
                "title_fa": "2017 Mazda 3",
                "title_en": "2017 Mazda 3",
                "title_ar": "2017 Mazda 3",
                "description_fa": "Clean hatch",
                "description_en": "Clean hatch",
                "description_ar": "Clean hatch",
                "price": "11000",
                "currency": Currency.TOMAN,
                "photos": [img1, img2],
            },
        )
        self.assertEqual(response.status_code, 302)
        created = Listing.objects.get(title_en="2017 Mazda 3")
        self.assertEqual(created.photos.count(), 2)
        self.assertTrue(bool(created.cover_image))
        detail = self.client.get(reverse("marketplace:detail", args=[created.pk]))
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, "gallery")
