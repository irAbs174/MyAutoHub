from django.test import TestCase
from django.urls import reverse

from apps.cars.models import Brand, Car, CarModel, Trim


def make_car(model, *, year, trim_name, **kwargs):
    trim, _ = Trim.objects.get_or_create(car_model=model, name=trim_name)
    return Car.objects.create(model=model, year=year, trim=trim, **kwargs)


class CarCatalogFilterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        toyota = Brand.objects.create(name="Toyota", country="JP")
        bmw = Brand.objects.create(name="BMW", country="DE")
        camry = CarModel.objects.create(brand=toyota, name="Camry")
        corolla = CarModel.objects.create(brand=toyota, name="Corolla")
        x3 = CarModel.objects.create(brand=bmw, name="X3")

        cls.toyota = toyota
        cls.bmw = bmw
        cls.camry = make_car(
            camry,
            year=2022,
            trim_name="SE",
            horsepower=169,
            fuel_type="gasoline",
            is_published=True,
        )
        cls.corolla = make_car(
            corolla,
            year=2018,
            trim_name="LE",
            horsepower=139,
            fuel_type="gasoline",
            is_published=True,
        )
        cls.x3 = make_car(
            x3,
            year=2023,
            trim_name="xDrive30i",
            horsepower=248,
            fuel_type="hybrid",
            is_published=True,
        )
        make_car(
            camry,
            year=2010,
            trim_name="Hidden",
            horsepower=100,
            fuel_type="gasoline",
            is_published=False,
        )

    def test_list_shows_published_only(self):
        res = self.client.get(reverse("cars:list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["result_count"], 3)

    def test_filter_by_brand(self):
        res = self.client.get(reverse("cars:list"), {"brand": self.toyota.pk})
        self.assertEqual(res.status_code, 200)
        ids = {c.pk for c in res.context["cars"]}
        self.assertEqual(ids, {self.camry.pk, self.corolla.pk})

    def test_legacy_brand_name_param(self):
        res = self.client.get(reverse("cars:list"), {"brand": "Toyota"})
        self.assertEqual(res.status_code, 200)
        ids = {c.pk for c in res.context["cars"]}
        self.assertEqual(ids, {self.camry.pk, self.corolla.pk})

    def test_filter_by_fuel_aliases_petrol(self):
        res = self.client.get(reverse("cars:list"), {"fuel": "petrol"})
        self.assertEqual(res.status_code, 200)
        ids = {c.pk for c in res.context["cars"]}
        self.assertEqual(ids, {self.camry.pk, self.corolla.pk})

    def test_filter_year_range_and_sort(self):
        res = self.client.get(
            reverse("cars:list"),
            {"year_min": 2020, "year_max": 2025, "sort": "powerDesc"},
        )
        self.assertEqual(res.status_code, 200)
        cars = list(res.context["cars"])
        self.assertEqual([c.pk for c in cars], [self.x3.pk, self.camry.pk])

    def test_filter_model_and_search(self):
        res = self.client.get(
            reverse("cars:list"),
            {"brand": self.toyota.pk, "model": self.camry.model_id, "q": "SE"},
        )
        self.assertEqual(res.status_code, 200)
        ids = {c.pk for c in res.context["cars"]}
        self.assertEqual(ids, {self.camry.pk})

    def test_detail_shows_related_sections(self):
        from apps.cars.models import Feature, TechnicalSpec

        TechnicalSpec.objects.create(car=self.camry, engine="2.5L")
        Feature.objects.create(car=self.camry, name="Sunroof", category="comfort")
        res = self.client.get(reverse("cars:detail", args=[self.camry.pk]))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "2.5L")
        self.assertContains(res, "Sunroof")


class PlacesPublicTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        from apps.cars.models import Dealer, RepairShop

        cls.brand = Brand.objects.create(name="ToyotaPlaces", country="JP")
        cls.dealer = Dealer.objects.create(
            name="Tokyo Toyota", city="Tehran", is_published=True
        )
        cls.dealer.brands.add(cls.brand)
        cls.shop = RepairShop.objects.create(
            name="Fast Fix", city="Isfahan", is_published=True
        )
        cls.shop.brands.add(cls.brand)
        Dealer.objects.create(name="Hidden Dealer", is_published=False)

    def test_places_index(self):
        res = self.client.get(reverse("places:index"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Tokyo Toyota")
        self.assertContains(res, "Fast Fix")
        self.assertNotContains(res, "Hidden Dealer")

    def test_dealer_and_shop_detail(self):
        res = self.client.get(
            reverse("places:dealer_detail", args=[self.dealer.pk])
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Tokyo Toyota")
        res = self.client.get(
            reverse("places:repair_shop_detail", args=[self.shop.pk])
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Fast Fix")
