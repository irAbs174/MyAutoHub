from django.core.management.base import BaseCommand
from django.db import transaction

from apps.cars.catalog_seed import (
    IRANIAN_CATALOG,
    IRANIAN_MANUFACTURERS,
    normalize_model_name,
)
from apps.cars.models import Brand, CarModel


class Command(BaseCommand):
    help = "Seed Iranian starter brands and car models into the catalog."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help=(
                "Delete brands whose manufacturer is in the Iranian starter set "
                "before seeding (does not touch unrelated demo brands)."
            ),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            deleted, _ = Brand.objects.filter(
                manufacturer__in=IRANIAN_MANUFACTURERS
            ).delete()
            self.stdout.write(
                self.style.WARNING(f"Flushed {deleted} Iranian catalog row(s).")
            )

        brands_created = 0
        brands_updated = 0
        models_created = 0

        for manufacturer, brands in IRANIAN_CATALOG.items():
            for brand_name, model_names in brands.items():
                brand, created = Brand.objects.get_or_create(
                    name=brand_name,
                    defaults={
                        "country": "Iran",
                        "manufacturer": manufacturer,
                    },
                )
                if created:
                    brands_created += 1
                else:
                    update_fields = []
                    if not brand.manufacturer:
                        brand.manufacturer = manufacturer
                        update_fields.append("manufacturer")
                    if not brand.country:
                        brand.country = "Iran"
                        update_fields.append("country")
                    if update_fields:
                        brand.save(update_fields=update_fields)
                        brands_updated += 1

                names = model_names or [brand_name]
                for raw_name in names:
                    model_name = normalize_model_name(brand_name, raw_name)
                    _, model_created = CarModel.objects.get_or_create(
                        brand=brand,
                        name=model_name,
                    )
                    if model_created:
                        models_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded Iranian catalog: "
                f"{brands_created} brand(s) created, "
                f"{brands_updated} brand(s) updated, "
                f"{models_created} model(s) created."
            )
        )
