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

    def test_filter_by_trim_and_horsepower(self):
        res = self.client.get(
            reverse("cars:list"),
            {"trim": self.camry.trim_id, "hp_min": 150, "hp_max": 200},
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual({c.pk for c in res.context["cars"]}, {self.camry.pk})

    def test_filter_by_transmission_and_seats(self):
        from apps.cars.models import Dimensions, TechnicalSpec

        TechnicalSpec.objects.create(car=self.camry, transmission="CVT", drivetrain="FWD")
        TechnicalSpec.objects.create(
            car=self.x3, transmission="Automatic", drivetrain="xDrive"
        )
        Dimensions.objects.create(car=self.camry, seats=5)
        Dimensions.objects.create(car=self.x3, seats=5)

        res = self.client.get(reverse("cars:list"), {"transmission": "cvt"})
        self.assertEqual({c.pk for c in res.context["cars"]}, {self.camry.pk})

        res = self.client.get(reverse("cars:list"), {"drivetrain": "awd"})
        self.assertEqual({c.pk for c in res.context["cars"]}, {self.x3.pk})

        res = self.client.get(reverse("cars:list"), {"seats": "5"})
        self.assertEqual({c.pk for c in res.context["cars"]}, {self.camry.pk, self.x3.pk})

    def test_filter_by_manufacturer(self):
        self.toyota.manufacturer = "Toyota Motor"
        self.toyota.save(update_fields=["manufacturer"])
        res = self.client.get(
            reverse("cars:list"), {"manufacturer": "Toyota Motor"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            {c.pk for c in res.context["cars"]}, {self.camry.pk, self.corolla.pk}
        )

    def test_filter_by_country_flags(self):
        iran = Brand.objects.create(name="PeugeotIR", country="Iran")
        japan = Brand.objects.create(name="ToyotaJP", country="Japan")
        usa = Brand.objects.create(name="FordUS", country="USA")
        ir_model = CarModel.objects.create(brand=iran, name="206")
        jp_model = CarModel.objects.create(brand=japan, name="Corolla")
        us_model = CarModel.objects.create(brand=usa, name="Mustang")
        ir_car = make_car(ir_model, year=2020, trim_name="Base", is_published=True)
        jp_car = make_car(jp_model, year=2022, trim_name="X", is_published=True)
        us_car = make_car(us_model, year=2021, trim_name="GT", is_published=True)

        res = self.client.get(reverse("cars:list"), {"country": "iran"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual({c.pk for c in res.context["cars"]}, {ir_car.pk})
        self.assertContains(res, "🇮🇷")
        # Iran is the first country chip after "All".
        filters = res.context["country_filters"]
        self.assertEqual(filters[0]["key"], "iran")
        self.assertNotIn("saudi", {item["key"] for item in filters})

        res = self.client.get(reverse("cars:list"), {"country": "japan"})
        japan_ids = {c.pk for c in res.context["cars"]}
        self.assertIn(jp_car.pk, japan_ids)
        # Seeded Toyota country="JP" also matches the Japan aliases.
        self.assertIn(self.camry.pk, japan_ids)
        self.assertContains(res, "🇯🇵")

        res = self.client.get(reverse("cars:list"), {"country": "usa"})
        self.assertEqual({c.pk for c in res.context["cars"]}, {us_car.pk})
        self.assertContains(res, "🇺🇸")
        self.assertNotIn(jp_car.pk, {c.pk for c in res.context["cars"]})

    def test_brands_page(self):
        Brand.objects.create(name="PublicBrand", country="Iran")
        res = self.client.get(reverse("cars:brands"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "PublicBrand")
        self.assertContains(res, "🇮🇷")

    def test_categories_page(self):
        from apps.cars.models import Category

        Category.objects.create(
            slug="suv-test", name="SUV Test", name_en="SUV Test", sort_order=1
        )
        res = self.client.get(reverse("cars:categories"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "SUV Test")

    def test_category_detail_and_catalog_filter(self):
        from apps.cars.models import Category

        category = Category.objects.create(
            slug="family-test", name="Family Test", name_en="Family Test"
        )
        self.camry.categories.add(category)
        self.camry.model.categories.add(category)

        res = self.client.get(reverse("cars:category_detail", kwargs={"slug": category.slug}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Family Test")
        self.assertContains(res, self.camry.model.name)

        res = self.client.get(reverse("cars:list"), {"category": category.pk})
        self.assertEqual(res.status_code, 200)
        self.assertEqual({c.pk for c in res.context["cars"]}, {self.camry.pk})

    def test_detail_shows_related_sections(self):
        from apps.cars.models import (
            Category,
            CommonFailure,
            Feature,
            FeatureAvailability,
            MarketInfo,
            TechnicalSpec,
        )

        TechnicalSpec.objects.create(
            car=self.camry, engine="2.5L", engine_code="A25A", torque_nm=224
        )
        Feature.objects.create(
            car=self.camry,
            name="Sunroof",
            category="comfort",
            key="sunroof",
            availability=FeatureAvailability.STANDARD,
        )
        cat = Category.objects.create(slug="sedan-test", name="Sedan", name_fa="سدان")
        self.camry.categories.add(cat)
        self.camry.market_status = "assembled"
        self.camry.importer = "Demo Importer"
        self.camry.save(update_fields=["market_status", "importer"])
        CommonFailure.objects.create(
            car=self.camry,
            area="engine",
            title="Oil leak",
            symptoms="Oil spots under car",
        )
        MarketInfo.objects.create(
            car=self.camry, market_price_new=1000, liquidity_score=8
        )
        res = self.client.get(reverse("cars:detail", args=[self.camry.pk]))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "2.5L")
        self.assertContains(res, "A25A")
        self.assertContains(res, "Sunroof")
        self.assertContains(res, "Oil leak")
        self.assertContains(res, "Demo Importer")
        self.assertContains(res, "سدان")
        self.assertIn("gallery_images", res.context)

    def test_detail_gallery_see_more_when_many_photos(self):
        from apps.cars.models import CarPhoto
        from django.core.files.uploadedfile import SimpleUploadedFile

        tiny = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00"
            b"\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00"
            b"\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
        )
        for i in range(6):
            CarPhoto.objects.create(
                car=self.camry,
                image=SimpleUploadedFile(f"g{i}.gif", tiny, content_type="image/gif"),
                sort_order=i,
            )
        res = self.client.get(reverse("cars:detail", args=[self.camry.pk]))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["gallery_images"]), 6)
        self.assertEqual(len(res.context["gallery_preview"]), 5)
        self.assertEqual(res.context["gallery_extra_count"], 1)
        self.assertContains(res, "car-gallery-more")
        self.assertContains(res, "+1")


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
