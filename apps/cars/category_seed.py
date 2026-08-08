DEFAULT_CATEGORIES = [
    ("economy", "Economy", "اقتصادی", "Economy", "اقتصادي", 10),
    ("family", "Family", "خانوادگی", "Family", "عائلي", 20),
    ("urban", "Urban", "شهری", "Urban", "حضري", 30),
    ("sport", "Sport", "اسپرت", "Sport", "رياضي", 40),
    ("luxury", "Luxury", "لوکس", "Luxury", "فاخر", 50),
    ("suv", "SUV", "SUV", "SUV", "SUV", 60),
    ("crossover", "Crossover", "کراس‌اوور", "Crossover", "كروس أوفر", 70),
    ("sedan", "Sedan", "سدان", "Sedan", "سيدان", 80),
    ("hatchback", "Hatchback", "هاچ‌بک", "Hatchback", "هاتشباك", 90),
    ("pickup", "Pickup", "وانت", "Pickup", "بيك أب", 100),
    ("mpv", "MPV", "MPV", "MPV", "MPV", 110),
    ("offroad", "Off-road", "آفرود", "Off-road", "طرق وعرة", 120),
    ("hybrid", "Hybrid", "هیبرید", "Hybrid", "هجين", 130),
    ("plugin-hybrid", "Plugin hybrid", "پلاگین هیبرید", "Plugin hybrid", "هجين قابل للشحن", 140),
    ("electric", "Electric", "برقی", "Electric", "كهربائي", 150),
]


def ensure_categories():
    from apps.cars.models import Category

    created = 0
    for slug, name, name_fa, name_en, name_ar, sort_order in DEFAULT_CATEGORIES:
        obj, was_created = Category.objects.get_or_create(
            slug=slug,
            defaults={
                "name": name,
                "name_fa": name_fa,
                "name_en": name_en,
                "name_ar": name_ar,
                "sort_order": sort_order,
            },
        )
        if was_created:
            created += 1
        elif not obj.name_ar:
            obj.name_ar = name_ar
            obj.save(update_fields=["name_ar"])
    return created
