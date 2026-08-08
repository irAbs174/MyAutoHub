from django.core.management.base import BaseCommand

from apps.cars.category_seed import ensure_categories


class Command(BaseCommand):
    help = "Seed practical car categories (اقتصادی، SUV، هیبرید, …)."

    def handle(self, *args, **options):
        created = ensure_categories()
        self.stdout.write(
            self.style.SUCCESS(f"Categories ready ({created} created).")
        )
