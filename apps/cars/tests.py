from django.test import TestCase
from django.urls import reverse

from apps.cars.models import Brand, Car, CarModel


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
        cls.camry = Car.objects.create(
            model=camry,
            year=2022,
            trim="SE",
            horsepower=169,
            fuel_type="gasoline",
            is_published=True,
        )
        cls.corolla = Car.objects.create(
            model=corolla,
            year=2018,
            trim="LE",
            horsepower=139,
            fuel_type="gasoline",
            is_published=True,
        )
        cls.x3 = Car.objects.create(
            model=x3,
            year=2023,
            trim="xDrive30i",
            horsepower=248,
            fuel_type="hybrid",
            is_published=True,
        )
        Car.objects.create(
            model=camry,
            year=2010,
            trim="Hidden",
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
