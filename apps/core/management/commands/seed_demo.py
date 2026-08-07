"""
Load demo data for local development.

Usage:
  python manage.py seed_demo
  python manage.py seed_demo --flush   # delete demo-tagged rows first (safe-ish)
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import SavedLocation
from apps.cars.models import (
    BatterySpec,
    Brand,
    Car,
    CarModel,
    CarPhoto,
    CarPrice,
    Dealer,
    Dimensions,
    Feature,
    FluidSpec,
    FluidType,
    MaintenanceItem,
    OBDCode,
    Part,
    RepairShop,
    ServiceScheduleItem,
    TechnicalSpec,
    TireSpec,
    Trim,
)
from apps.core.i18n_content import tri_fields
from apps.emergency.models import EmergencyService, RequestStatus
from apps.emergency.services import (
    buzz_request,
    create_emergency_request,
    transition_request,
)
from apps.marketplace.models import Listing, ListingStatus
from apps.pricing.models import PriceReference
from apps.stories.models import Story
from apps.youtube.models import YoutubeVideo

User = get_user_model()

DEMO_PASSWORD = "demo12345"


class Command(BaseCommand):
    help = "Seed the database with demo users and sample content for all apps."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Remove previously seeded demo users and related rows before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            self._flush_demo()

        users = self._seed_users()
        locations = self._seed_locations(users)
        services = self._seed_emergency_services()
        self._seed_emergency_requests(users, services, locations)
        self._seed_pricing()
        self._seed_marketplace(users)
        self._seed_cars()
        self._seed_youtube()
        self._seed_stories(users)

        self.stdout.write(self.style.SUCCESS("Demo data ready."))
        self.stdout.write("")
        self.stdout.write("Log in with any of these accounts (password for all):")
        self.stdout.write(f"  password: {DEMO_PASSWORD}")
        for label, user in users.items():
            flags = []
            if user.is_superuser:
                flags.append("superuser")
            if user.is_staff:
                flags.append("staff")
            if user.groups.filter(name="emergency_operators").exists():
                flags.append("operator")
            flag_txt = f" ({', '.join(flags)})" if flags else ""
            self.stdout.write(f"  · {user.username}{flag_txt} -{label}")

    def _placeholder(self, slug: str, color: tuple[int, int, int], label: str, size=(960, 600)):
        """Create a simple branded JPEG for demo media."""
        from io import BytesIO

        from PIL import Image, ImageDraw, ImageFont

        img = Image.new("RGB", size, color)
        draw = ImageDraw.Draw(img)
        band = (
            min(255, color[0] + 35),
            min(255, color[1] + 45),
            min(255, color[2] + 40),
        )
        draw.rectangle([0, size[1] - 140, size[0], size[1]], fill=band)
        draw.ellipse([size[0] - 220, -60, size[0] + 40, 200], fill=band)
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", 42)
            small = ImageFont.truetype("DejaVuSans.ttf", 22)
        except OSError:
            font = ImageFont.load_default()
            small = font
        draw.text((40, 40), "MyAutoHub", fill=(255, 255, 255), font=small)
        draw.text((40, size[1] - 100), label[:42], fill=(255, 255, 255), font=font)
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=86)
        return ContentFile(buf.getvalue(), name=f"{slug}.jpg")

    def _ensure_image(self, instance, field_name: str, slug: str, color, label: str):
        field = getattr(instance, field_name)
        if field:
            return
        content = self._placeholder(slug, color, label)
        getattr(instance, field_name).save(content.name, content, save=True)

    def _flush_demo(self):
        usernames = [
            "admin",
            "driver",
            "seller",
            "operator",
            "opadmin",
            "author",
        ]
        qs = User.objects.filter(username__in=usernames)
        count = qs.count()
        qs.delete()
        # Orphan catalog content without demo owners
        PriceReference.objects.filter(title_en__startswith="[Demo]").delete()
        YoutubeVideo.objects.filter(title__startswith="[Demo]").delete()
        Story.objects.filter(title_en__startswith="[Demo]").delete()
        Brand.objects.filter(name__in=["Toyota", "BMW", "Iran Khodro", "Hyundai"]).delete()
        EmergencyService.objects.filter(name_en__startswith="[Demo]").delete()
        self.stdout.write(self.style.WARNING(f"Flushed {count} demo user(s) and tagged demo rows."))

    def _seed_users(self):
        group, _ = Group.objects.get_or_create(name="emergency_operators")

        def ensure(username, *, email, is_staff=False, is_superuser=False, operator=False):
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "is_staff": is_staff,
                    "is_superuser": is_superuser,
                },
            )
            if created or not user.has_usable_password():
                user.set_password(DEMO_PASSWORD)
            user.email = email
            user.is_staff = is_staff or user.is_staff
            user.is_superuser = is_superuser or user.is_superuser
            user.save()
            if operator:
                group.user_set.add(user)
            return user

        return {
            "admin": ensure(
                "admin",
                email="admin@myautohub.local",
                is_staff=True,
                is_superuser=True,
            ),
            "driver": ensure("driver", email="driver@myautohub.local"),
            "seller": ensure("seller", email="seller@myautohub.local"),
            "operator": ensure(
                "operator",
                email="operator@myautohub.local",
                operator=True,
            ),
            "opadmin": ensure(
                "opadmin",
                email="opadmin@myautohub.local",
                is_staff=True,
                operator=True,
            ),
            "author": ensure("author", email="author@myautohub.local"),
        }

    def _seed_locations(self, users):
        specs = [
            (users["driver"], "Home", "Valiasr St, Tehran", "35.721900", "51.406500", True),
            (users["driver"], "Office", "Saadat Abad, Tehran", "35.787200", "51.374800", False),
            (users["seller"], "Garage", "Karaj road, Tehran", "35.689200", "51.289000", True),
        ]
        locations = []
        for user, label, address, lat, lng, default in specs:
            loc, _ = SavedLocation.objects.get_or_create(
                user=user,
                label=label,
                defaults={
                    "address": address,
                    "latitude": Decimal(lat),
                    "longitude": Decimal(lng),
                    "is_default": default,
                },
            )
            locations.append(loc)
        return locations

    def _seed_emergency_services(self):
        specs = [
            ("[Demo] Towing", "Flatbed and wheel-lift towing across Greater Tehran.", "24/7 within city ring"),
            ("[Demo] Jump start", "Battery boost and quick health check.", "Metro area"),
            ("[Demo] Flat tire", "Spare mount or roadside plug when safe.", "Highways + city"),
            ("[Demo] Lockout", "Non-destructive vehicle entry assistance.", "City zones"),
            ("[Demo] Fuel delivery", "Emergency petrol/diesel top-up.", "Ring roads"),
        ]
        services = []
        colors = [
            (194, 65, 12),
            (180, 83, 9),
            (15, 118, 110),
            (67, 56, 202),
            (8, 145, 178),
        ]
        for idx, (name, description, coverage) in enumerate(specs):
            svc, _ = EmergencyService.objects.get_or_create(
                name_en=name,
                defaults={
                    **tri_fields(
                        name=name,
                        description=description,
                        coverage_notes=coverage,
                    ),
                    "is_active": True,
                },
            )
            self._ensure_image(
                svc,
                "cover_image",
                f"emergency-{idx}",
                colors[idx % len(colors)],
                name.replace("[Demo] ", ""),
            )
            services.append(svc)
        return services

    def _seed_emergency_requests(self, users, services, locations):
        driver = users["driver"]
        operator = users["operator"]
        opadmin = users["opadmin"]
        home = locations[0]
        towing, jump, tire, lockout, fuel = services

        # Waiting
        if not self._has_request(driver, towing, "Battery dead near home"):
            create_emergency_request(
                requester=driver,
                service=towing,
                description="Battery dead near home-need a tow to the garage.",
                saved_location=home,
            )

        # Processing + buzz
        if not self._has_request(driver, jump, "Won't start after rain"):
            req = create_emergency_request(
                requester=driver,
                service=jump,
                description="Won't start after rain. Hazard lights on, roadside safe.",
                latitude=Decimal("35.755000"),
                longitude=Decimal("51.410000"),
            )
            transition_request(
                emergency_request=req,
                actor=operator,
                to_status=RequestStatus.PROCESSING,
                note="Accepted-ETA 25 min",
            )
            buzz_request(emergency_request=req, user=driver)

        # Finished success + review
        if not self._has_request(driver, tire, "Punctured rear left"):
            req = create_emergency_request(
                requester=driver,
                service=tire,
                description="Punctured rear left on Hemmat expressway.",
                latitude=Decimal("35.740100"),
                longitude=Decimal("51.450200"),
            )
            transition_request(
                emergency_request=req,
                actor=operator,
                to_status=RequestStatus.PROCESSING,
                note="Accepted",
            )
            transition_request(
                emergency_request=req,
                actor=opadmin,
                to_status=RequestStatus.FINISH_SUCCESS,
                note="Spare mounted",
            )
            req.review_comment = "Fast and careful. Thank you!"
            req.review_rating = 5
            req.reviewed_at = timezone.now()
            req.save(update_fields=["review_comment", "review_rating", "reviewed_at", "updated_at"])

        # Cancelled
        if not self._has_request(driver, lockout, "Keys locked inside-cancelled"):
            req = create_emergency_request(
                requester=driver,
                service=lockout,
                description="Keys locked inside-cancelled after finding spare.",
                saved_location=home,
            )
            transition_request(
                emergency_request=req,
                actor=driver,
                to_status=RequestStatus.CANCELLED,
                note="Found spare key",
            )

        # Waiting fuel
        if not self._has_request(driver, fuel, "Ran out of petrol"):
            create_emergency_request(
                requester=driver,
                service=fuel,
                description="Ran out of petrol on Azadegan. Need 5 liters.",
                latitude=Decimal("35.650000"),
                longitude=Decimal("51.320000"),
            )

    def _has_request(self, requester, service, description_contains: str) -> bool:
        return requester.emergency_requests.filter(
            service=service,
            description__icontains=description_contains.split("—")[0].strip()[:24],
        ).exists() or requester.emergency_requests.filter(
            service=service,
            description__startswith=description_contains[:30],
        ).exists()

    def _seed_pricing(self):
        specs = [
            ("[Demo] Oil change (synthetic)", "Maintenance", "89.00", "USD", "Shop average", "Local garages"),
            ("[Demo] Brake pads (front pair)", "Parts", "120.00", "USD", "Parts + labor ballpark", "Market scan"),
            ("[Demo] Annual inspection", "Compliance", "45.00", "USD", "City average", "Municipal offices"),
            ("[Demo] Detail wash", "Care", "35.00", "USD", "Interior + exterior", "Hub partners"),
            ("[Demo] Used Corolla (2018–2020)", "Market", "14500.00", "USD", "Clean title, mid mileage", "Listings sample"),
            ("[Demo] Battery replacement", "Maintenance", "160.00", "USD", "Parts + install", "Parts shops"),
        ]
        for idx, (title, category, amount, currency, notes, source) in enumerate(specs):
            item, _ = PriceReference.objects.get_or_create(
                title_en=title,
                defaults={
                    **tri_fields(
                        title=title,
                        category=category,
                        notes=notes,
                        source=source,
                    ),
                    "amount": Decimal(amount),
                    "currency": currency,
                    "is_published": True,
                },
            )
            self._ensure_image(
                item,
                "cover_image",
                f"price-{idx}",
                (67, 56, 202),
                title.replace("[Demo] ", ""),
            )

    def _seed_marketplace(self, users):
        seller = users["seller"]
        driver = users["driver"]
        specs = [
            (
                seller,
                "2019 Peugeot 206",
                "One owner, full service history, AC cold. Ready for trade.",
                "9200.00",
                2019,
                78000,
                "Tehran",
                ListingStatus.ACTIVE,
            ),
            (
                seller,
                "2021 Hyundai Tucson",
                "Low mileage SUV, panoramic roof, dealer serviced.",
                "28500.00",
                2021,
                34000,
                "Karaj",
                ListingStatus.ACTIVE,
            ),
            (
                driver,
                "2015 Pride 111",
                "Daily runner, new tires last month. Selling to upgrade.",
                "4100.00",
                2015,
                142000,
                "Tehran",
                ListingStatus.ACTIVE,
            ),
            (
                seller,
                "2017 BMW 320i",
                "Sport line, leather, clean body. Price firm.",
                "19800.00",
                2017,
                91000,
                "Isfahan",
                ListingStatus.SOLD,
            ),
        ]
        for idx, (seller_user, title, description, price, year, mileage, city, status) in enumerate(specs):
            item, _ = Listing.objects.get_or_create(
                seller=seller_user,
                title_en=title,
                defaults={
                    **tri_fields(title=title, description=description),
                    "price": Decimal(price),
                    "currency": "USD",
                    "year": year,
                    "mileage_km": mileage,
                    "city": city,
                    "status": status,
                },
            )
            self._ensure_image(
                item,
                "cover_image",
                f"listing-{idx}",
                (22, 163, 74),
                title,
            )

    def _seed_cars(self):
        catalog = {
            "Toyota": {
                "country": "Japan",
                "models": {
                    "Corolla": [
                        {"year": 2022, "trim": "SE", "horsepower": 169, "fuel_type": "gasoline"},
                        {"year": 2020, "trim": "LE", "horsepower": 139, "fuel_type": "gasoline"},
                    ],
                    "Camry": [
                        {"year": 2023, "trim": "XSE", "horsepower": 301, "fuel_type": "hybrid"},
                    ],
                },
            },
            "BMW": {
                "country": "Germany",
                "models": {
                    "320i": [
                        {"year": 2021, "trim": "Sport", "horsepower": 184, "fuel_type": "gasoline"},
                    ],
                    "X3": [
                        {"year": 2022, "trim": "xDrive30i", "horsepower": 248, "fuel_type": "gasoline"},
                    ],
                },
            },
            "Iran Khodro": {
                "country": "Iran",
                "models": {
                    "Samand": [
                        {"year": 2019, "trim": "LX", "horsepower": 100, "fuel_type": "gasoline"},
                    ],
                    "Dena": [
                        {"year": 2021, "trim": "Plus", "horsepower": 113, "fuel_type": "gasoline"},
                    ],
                },
            },
            "Hyundai": {
                "country": "South Korea",
                "models": {
                    "Tucson": [
                        {"year": 2022, "trim": "Limited", "horsepower": 187, "fuel_type": "gasoline"},
                    ],
                    "Elantra": [
                        {"year": 2020, "trim": "SEL", "horsepower": 147, "fuel_type": "gasoline"},
                    ],
                },
            },
        }
        car_colors = [
            (15, 118, 110),
            (8, 145, 178),
            (30, 64, 175),
            (127, 29, 29),
            (55, 65, 81),
            (6, 95, 70),
        ]
        color_i = 0
        first_rich = True
        for brand_name, meta in catalog.items():
            brand, _ = Brand.objects.get_or_create(
                name=brand_name,
                defaults={"country": meta["country"]},
            )
            for model_name, cars in meta["models"].items():
                car_model, _ = CarModel.objects.get_or_create(brand=brand, name=model_name)
                OBDCode.objects.get_or_create(
                    car_model=car_model,
                    code="P0300",
                    defaults={
                        "title": "Random/Multiple Cylinder Misfire",
                        "description": "Demo OBD code for catalog browsing.",
                        "severity": "warning",
                    },
                )
                for spec in cars:
                    trim, _ = Trim.objects.get_or_create(
                        car_model=car_model, name=spec["trim"]
                    )
                    car, _ = Car.objects.get_or_create(
                        model=car_model,
                        year=spec["year"],
                        trim=trim,
                        defaults={
                            "horsepower": spec["horsepower"],
                            "fuel_type": spec["fuel_type"],
                            "description": (
                                f"{brand_name} {model_name} {spec['year']} "
                                f"{spec['trim']}"
                            ),
                            "is_published": True,
                        },
                    )
                    color = car_colors[color_i % len(car_colors)]
                    color_i += 1
                    label = f"{brand_name} {model_name}"
                    self._ensure_image(
                        car,
                        "cover_image",
                        f"car-{car.pk}-cover",
                        color,
                        label,
                    )
                    if car.photos.count() < 3:
                        for n, caption in enumerate(
                            ("Front angle", "Interior", "Rear detail"), start=1
                        ):
                            shade = tuple(max(0, c - n * 12) for c in color)
                            content = self._placeholder(
                                f"car-{car.pk}-{n}",
                                shade,
                                f"{label} · {caption}",
                                size=(900, 600),
                            )
                            photo = CarPhoto(car=car, caption=caption, sort_order=n)
                            photo.image.save(content.name, content, save=True)

                    if first_rich:
                        if not TechnicalSpec.objects.filter(car=car).exists():
                            self._seed_car_details(car)
                        first_rich = False

            dealer, _ = Dealer.objects.get_or_create(
                name=f"[Demo] {brand_name} Center",
                defaults={
                    "city": "Tehran",
                    "address": "Demo dealer address",
                    "phone": "+98-21-00000000",
                    "is_published": True,
                },
            )
            dealer.brands.add(brand)
            shop, _ = RepairShop.objects.get_or_create(
                name=f"[Demo] {brand_name} Service",
                defaults={
                    "city": "Tehran",
                    "address": "Demo repair shop address",
                    "phone": "+98-21-11111111",
                    "is_published": True,
                },
            )
            shop.brands.add(brand)

    def _seed_car_details(self, car):
        TechnicalSpec.objects.get_or_create(
            car=car,
            defaults={
                "engine": "2.0L I4",
                "displacement_cc": 2000,
                "cylinders": 4,
                "transmission": "CVT",
                "drivetrain": "FWD",
                "top_speed_kmh": 200,
                "accel_0_100": Decimal("8.5"),
                "economy_city": Decimal("7.5"),
                "economy_highway": Decimal("5.8"),
                "emission_standard": "Euro 6",
            },
        )
        Dimensions.objects.get_or_create(
            car=car,
            defaults={
                "length_mm": 4630,
                "width_mm": 1780,
                "height_mm": 1435,
                "wheelbase_mm": 2700,
                "curb_weight_kg": 1400,
                "cargo_l": 470,
                "seats": 5,
                "ground_clearance_mm": 150,
                "fuel_tank_l": Decimal("50.0"),
            },
        )
        Feature.objects.get_or_create(
            car=car, name="Adaptive cruise control", defaults={"category": "tech"}
        )
        Feature.objects.get_or_create(
            car=car, name="Lane keep assist", defaults={"category": "safety"}
        )
        MaintenanceItem.objects.get_or_create(
            car=car,
            title="Oil change",
            defaults={
                "interval_km": 10000,
                "interval_months": 12,
                "description": "Synthetic oil and filter.",
                "estimated_cost": Decimal("120.00"),
            },
        )
        FluidSpec.objects.get_or_create(
            car=car,
            fluid_type=FluidType.ENGINE_OIL,
            defaults={"specification": "0W-20", "capacity": "4.5 L"},
        )
        TireSpec.objects.get_or_create(
            car=car,
            size="215/55R17",
            defaults={"position": "all", "pressure_psi": Decimal("35.0")},
        )
        BatterySpec.objects.get_or_create(
            car=car,
            defaults={
                "group_size": "35",
                "voltage": Decimal("12.0"),
                "cca": 550,
                "chemistry": "AGM",
            },
        )
        ServiceScheduleItem.objects.get_or_create(
            car=car,
            mileage_km=20000,
            defaults={
                "months": 24,
                "tasks": "Oil, filters, brake inspection",
                "sort_order": 1,
            },
        )
        Part.objects.get_or_create(
            car=car,
            name="Cabin air filter",
            defaults={"oem_number": "OEM-DEMO-001", "category": "Filters"},
        )
        CarPrice.objects.get_or_create(
            car=car,
            label="MSRP (demo)",
            defaults={
                "amount": Decimal("25000.00"),
                "currency": "USD",
                "source": "Demo seed",
                "recorded_at": date(2024, 1, 1),
            },
        )

    def _seed_youtube(self):
        # Public demo / commonly used IDs for embed smoke tests
        specs = [
            ("[Demo] Winter roadside checklist", "jNQXAC9IVRw", date(2024, 11, 12)),
            ("[Demo] How to change a tire safely", "dQw4w9WgXcQ", date(2024, 6, 1)),
            ("[Demo] Buying a used car-inspection tips", "9bZkp7q19f0", date(2025, 1, 20)),
            ("[Demo] MyAutoHub community drive", "kJQP7kiw5Fk", date(2025, 3, 8)),
        ]
        for title, youtube_id, published in specs:
            YoutubeVideo.objects.get_or_create(
                youtube_id=youtube_id,
                defaults={
                    "title": title,
                    "description": "Demo video seeded for local browsing.",
                    "published_at": published,
                    "is_published": True,
                },
            )

    def _seed_stories(self, users):
        author = users["author"]
        now = timezone.now()
        specs = [
            (
                "[Demo] Night tow on Hemmat",
                "A quiet expressway, a dead battery, and a calm operator.",
                (
                    "It was past midnight when the dashboard lights flickered out. "
                    "I opened MyAutoHub, tapped Emergency, and pinned my spot.\n\n"
                    "Twenty minutes later hazards blinked behind me-flatbed ready, "
                    "no drama. That is the hub I want on the road."
                ),
                now - timedelta(days=12),
            ),
            (
                "[Demo] First listing sold",
                "Listing a daily driver and finding a fair buyer in the hub.",
                (
                    "I uploaded photos, set a clear price, and answered questions in the open. "
                    "No pressure, just people who care about cars.\n\n"
                    "Three days later the Pride had a new owner-and I had room for the next chapter."
                ),
                now - timedelta(days=5),
            ),
            (
                "[Demo] Friends who fix together",
                "A weekend of oil changes and coffee in the garage.",
                (
                    "We borrowed torque wrenches, compared oil grades, and argued gently about filters. "
                    "The catalog on MyAutoHub settled more than one debate.\n\n"
                    "Stories like this are why the hub feels like a place, not just an app."
                ),
                now - timedelta(days=1),
            ),
        ]
        for idx, (title, excerpt, body, published_at) in enumerate(specs):
            story, _ = Story.objects.get_or_create(
                title_en=title,
                defaults={
                    **tri_fields(title=title, excerpt=excerpt, body=body),
                    "author": author,
                    "is_published": True,
                    "published_at": published_at,
                },
            )
            self._ensure_image(
                story,
                "cover_image",
                f"story-{idx}",
                (8, 145, 178),
                title.replace("[Demo] ", ""),
            )
