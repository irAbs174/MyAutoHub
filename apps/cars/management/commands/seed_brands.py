from django.core.management.base import BaseCommand
from django.db import transaction

from apps.cars.catalog_seed import (
    INTERNATIONAL_CATALOG,
    IRANIAN_CATALOG,
    IRANIAN_MANUFACTURERS,
    international_brand_names,
    normalize_model_name,
)
from apps.cars.category_seed import ensure_categories
from apps.cars.models import Brand, CarModel


class Command(BaseCommand):
    help = "Seed Iranian and international brands/models into the catalog."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help=(
                "Delete seeded Iranian manufacturers and international catalog "
                "brands before seeding (does not touch unrelated demo brands)."
            ),
        )
        parser.add_argument(
            "--iran-only",
            action="store_true",
            help="Seed only the Iranian manufacturer catalog.",
        )
        parser.add_argument(
            "--international-only",
            action="store_true",
            help="Seed only the international brand catalog.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        cats = ensure_categories()
        self.stdout.write(self.style.SUCCESS(f"Categories ready ({cats} created)."))

        seed_iran = not options["international_only"]
        seed_intl = not options["iran_only"]

        if options["flush"]:
            deleted = 0
            if seed_iran:
                count, _ = Brand.objects.filter(
                    manufacturer__in=IRANIAN_MANUFACTURERS
                ).delete()
                deleted += count
            if seed_intl:
                count, _ = Brand.objects.filter(
                    name__in=international_brand_names()
                ).delete()
                deleted += count
            self.stdout.write(
                self.style.WARNING(f"Flushed {deleted} catalog brand row(s).")
            )

        brands_created = 0
        brands_updated = 0
        models_created = 0

        if seed_iran:
            c, u, m = self._seed_iranian()
            brands_created += c
            brands_updated += u
            models_created += m

        if seed_intl:
            c, u, m = self._seed_international()
            brands_created += c
            brands_updated += u
            models_created += m

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded catalog: "
                f"{brands_created} brand(s) created, "
                f"{brands_updated} brand(s) updated, "
                f"{models_created} model(s) created."
            )
        )

    def _seed_iranian(self) -> tuple[int, int, int]:
        brands_created = brands_updated = models_created = 0
        for manufacturer, brands in IRANIAN_CATALOG.items():
            for brand_name, model_names in brands.items():
                c, u, m = self._upsert_brand_models(
                    brand_name=brand_name,
                    model_names=model_names,
                    country="Iran",
                    manufacturer=manufacturer,
                )
                brands_created += c
                brands_updated += u
                models_created += m
        return brands_created, brands_updated, models_created

    def _seed_international(self) -> tuple[int, int, int]:
        brands_created = brands_updated = models_created = 0
        for country, brands in INTERNATIONAL_CATALOG.items():
            for brand_name, model_names in brands.items():
                c, u, m = self._upsert_brand_models(
                    brand_name=brand_name,
                    model_names=model_names,
                    country=country,
                    manufacturer=brand_name,
                )
                brands_created += c
                brands_updated += u
                models_created += m
        return brands_created, brands_updated, models_created

    def _upsert_brand_models(
        self,
        *,
        brand_name: str,
        model_names: list[str],
        country: str,
        manufacturer: str,
    ) -> tuple[int, int, int]:
        brands_created = brands_updated = models_created = 0
        brand, created = Brand.objects.get_or_create(
            name=brand_name,
            defaults={
                "country": country,
                "manufacturer": manufacturer,
            },
        )
        if created:
            brands_created = 1
        else:
            update_fields = []
            if not brand.manufacturer:
                brand.manufacturer = manufacturer
                update_fields.append("manufacturer")
            if not brand.country:
                brand.country = country
                update_fields.append("country")
            if update_fields:
                brand.save(update_fields=update_fields)
                brands_updated = 1

        names = model_names or [brand_name]
        for raw_name in names:
            model_name = normalize_model_name(brand_name, raw_name)
            _, model_created = CarModel.objects.get_or_create(
                brand=brand,
                name=model_name,
            )
            if model_created:
                models_created += 1

        return brands_created, brands_updated, models_created
