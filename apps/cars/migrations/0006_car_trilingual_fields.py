# Generated manually for car trilingual content fields

from django.db import migrations, models


def copy_car_langs(apps, schema_editor):
    Car = apps.get_model("cars", "Car")
    for car in Car.objects.all():
        description = getattr(car, "description", None) or ""
        official = getattr(car, "official_name", None) or ""
        update_fields = []
        if description:
            car.description_fa = description
            car.description_en = description
            car.description_ar = description
            update_fields.extend(
                ["description_fa", "description_en", "description_ar"]
            )
        if official:
            car.official_name_fa = official
            car.official_name_en = official
            car.official_name_ar = official
            update_fields.extend(
                ["official_name_fa", "official_name_en", "official_name_ar"]
            )
        if update_fields:
            car.save(update_fields=update_fields)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("cars", "0005_expand_full_catalog"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="description_fa",
            field=models.TextField(
                blank=True, default="", verbose_name="Description (فارسی)"
            ),
        ),
        migrations.AddField(
            model_name="car",
            name="description_en",
            field=models.TextField(
                blank=True, default="", verbose_name="Description (English)"
            ),
        ),
        migrations.AddField(
            model_name="car",
            name="description_ar",
            field=models.TextField(
                blank=True, default="", verbose_name="Description (العربية)"
            ),
        ),
        migrations.AddField(
            model_name="car",
            name="official_name_fa",
            field=models.CharField(
                blank=True,
                default="",
                max_length=160,
                verbose_name="Official name (فارسی)",
            ),
        ),
        migrations.AddField(
            model_name="car",
            name="official_name_en",
            field=models.CharField(
                blank=True,
                default="",
                max_length=160,
                verbose_name="Official name (English)",
            ),
        ),
        migrations.AddField(
            model_name="car",
            name="official_name_ar",
            field=models.CharField(
                blank=True,
                default="",
                max_length=160,
                verbose_name="Official name (العربية)",
            ),
        ),
        migrations.AddField(
            model_name="car",
            name="name_ar",
            field=models.CharField(
                blank=True,
                default="",
                max_length=120,
                verbose_name="Display name (العربية)",
            ),
        ),
        migrations.AddField(
            model_name="carmodel",
            name="name_ar",
            field=models.CharField(
                blank=True,
                max_length=120,
                verbose_name="Name (العربية)",
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="name_ar",
            field=models.CharField(
                blank=True,
                max_length=80,
                verbose_name="Name (العربية)",
            ),
        ),
        migrations.AlterField(
            model_name="car",
            name="name_fa",
            field=models.CharField(
                blank=True,
                default="",
                max_length=120,
                verbose_name="Display name (فارسی)",
            ),
        ),
        migrations.AlterField(
            model_name="car",
            name="name_en",
            field=models.CharField(
                blank=True,
                default="",
                max_length=120,
                verbose_name="Display name (English)",
            ),
        ),
        migrations.AlterField(
            model_name="carmodel",
            name="name_fa",
            field=models.CharField(
                blank=True, max_length=120, verbose_name="Name (فارسی)"
            ),
        ),
        migrations.AlterField(
            model_name="carmodel",
            name="name_en",
            field=models.CharField(
                blank=True, max_length=120, verbose_name="Name (English)"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="name_fa",
            field=models.CharField(
                blank=True, max_length=80, verbose_name="Name (فارسی)"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="name_en",
            field=models.CharField(
                blank=True, max_length=80, verbose_name="Name (English)"
            ),
        ),
        migrations.RunPython(copy_car_langs, noop_reverse),
        migrations.RemoveField(
            model_name="car",
            name="description",
        ),
        migrations.RemoveField(
            model_name="car",
            name="official_name",
        ),
    ]
