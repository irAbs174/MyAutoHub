from django.test import Client, TestCase, override_settings
from django.urls import reverse

from apps.cars.models import Brand, Car, CarModel, Dealer, RepairShop, Trim


def _make_car(model, *, year, trim_name, **kwargs):
    trim, _ = Trim.objects.get_or_create(car_model=model, name=trim_name)
    return Car.objects.create(model=model, year=year, trim=trim, **kwargs)


@override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
class PublicApiTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST="localhost")

    def test_hub_is_public(self):
        response = self.client.get("/api/public/hub/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        for key in (
            "cars",
            "listings",
            "videos",
            "stories",
            "prices",
            "emergency_services",
            "brands",
            "social_links",
        ):
            self.assertIn(key, payload)

    def test_cars_is_public(self):
        response = self.client.get("/api/public/cars/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("results", payload)
        self.assertIn("count", payload)

    def test_car_detail_api(self):
        brand = Brand.objects.create(name="Peugeot")
        model = CarModel.objects.create(brand=brand, name="206")
        car = _make_car(model, year=2018, trim_name="TU5", is_published=True)
        Dealer.objects.create(name="Peugeot House", is_published=True).brands.add(brand)

        response = self.client.get(f"/api/public/cars/{car.pk}/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["trim"], "TU5")
        self.assertEqual(payload["trim_name"], "TU5")
        self.assertIn("features", payload)
        self.assertIn("obd_codes", payload)
        self.assertEqual(payload["dealers"][0]["name"], "Peugeot House")

    def test_dealers_and_repair_shops_api(self):
        brand = Brand.objects.create(name="Kia")
        dealer = Dealer.objects.create(name="Kia Dealer", is_published=True)
        dealer.brands.add(brand)
        shop = RepairShop.objects.create(name="Kia Shop", is_published=True)
        shop.brands.add(brand)

        dealers = self.client.get("/api/public/dealers/", {"brand": brand.pk})
        self.assertEqual(dealers.status_code, 200)
        self.assertEqual(dealers.json()["results"][0]["name"], "Kia Dealer")

        shops = self.client.get("/api/public/repair-shops/", {"brand": "Kia"})
        self.assertEqual(shops.status_code, 200)
        self.assertEqual(shops.json()["results"][0]["name"], "Kia Shop")

    def test_search_suggest_finds_car(self):
        brand = Brand.objects.create(name="Peugeot")
        model = CarModel.objects.create(brand=brand, name="206")
        _make_car(model, year=2018, trim_name="TU5", is_published=True)

        response = self.client.get("/api/public/search/", {"q": "Peugeot"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["q"], "Peugeot")
        self.assertTrue(payload["results"])
        first = payload["results"][0]
        self.assertEqual(first["category"], "car")
        self.assertIn("Peugeot", first["title"])
        self.assertIn("url", first)

    def test_search_suggest_empty_query(self):
        response = self.client.get("/api/public/search/", {"q": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["results"], [])


@override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
class SearchViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST="localhost")
        brand = Brand.objects.create(name="Peugeot")
        model = CarModel.objects.create(brand=brand, name="206")
        _make_car(model, year=2018, trim_name="TU5", is_published=True)

    def test_search_page_loads(self):
        response = self.client.get(reverse("core:search"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="q"')

    def test_search_finds_car(self):
        response = self.client.get(reverse("core:search"), {"q": "Peugeot"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Peugeot")
        self.assertContains(response, "206")

    def test_search_empty_query_has_no_sections(self):
        response = self.client.get(reverse("core:search"), {"q": "zzzz-no-match"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 0)
        self.assertContains(response, 'class="empty')


@override_settings(
    ALLOWED_HOSTS=["localhost", "testserver"],
    SITE_URL="https://app.example.com",
)
class SeoEndpointsTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST="localhost")

    def test_robots_txt(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain; charset=utf-8")
        body = response.content.decode()
        self.assertIn("Disallow: /admin/", body)
        self.assertIn("Disallow: /panel/", body)
        self.assertIn("Sitemap: https://app.example.com/sitemap.xml", body)

    def test_sitemap_xml(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn("<urlset", body)
        self.assertIn("/fa/", body)
        self.assertIn("/en/", body)
        self.assertIn("/ar/", body)
        self.assertIn("hreflang=", body)

    def test_home_has_seo_meta(self):
        response = self.client.get("/fa/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rel="canonical"')
        self.assertContains(response, 'property="og:title"')
        self.assertContains(response, 'application/ld+json')
        self.assertContains(response, 'hreflang="en"')

    def test_search_is_noindex(self):
        response = self.client.get(reverse("core:search"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'content="noindex, follow"')

