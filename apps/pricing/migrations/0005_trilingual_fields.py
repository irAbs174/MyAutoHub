# Generated manually for trilingual content fields

from django.db import migrations, models


def copy_price_langs(apps, schema_editor):
    PriceReference = apps.get_model("pricing", "PriceReference")
    for item in PriceReference.objects.all():
        title = item.title or ""
        category = item.category or ""
        notes = item.notes or ""
        source = item.source or ""
        item.title_fa = title
        item.title_en = title
        item.title_ar = title
        item.category_fa = category
        item.category_en = category
        item.category_ar = category
        item.notes_fa = notes
        item.notes_en = notes
        item.notes_ar = notes
        item.source_fa = source
        item.source_en = source
        item.source_ar = source
        item.save(
            update_fields=[
                "title_fa",
                "title_en",
                "title_ar",
                "category_fa",
                "category_en",
                "category_ar",
                "notes_fa",
                "notes_en",
                "notes_ar",
                "source_fa",
                "source_en",
                "source_ar",
            ]
        )


class Migration(migrations.Migration):
    dependencies = [
        ("pricing", "0004_add_gallery_photos"),
    ]

    operations = [
        migrations.AddField(
            model_name="pricereference",
            name="title_fa",
            field=models.CharField(max_length=160, null=True, verbose_name="Title (فارسی)"),
        ),
        migrations.AddField(
            model_name="pricereference",
            name="title_en",
            field=models.CharField(max_length=160, null=True, verbose_name="Title (English)"),
        ),
        migrations.AddField(
            model_name="pricereference",
            name="title_ar",
            field=models.CharField(max_length=160, null=True, verbose_name="Title (العربية)"),
        ),
        migrations.AddField(
            model_name="pricereference",
            name="category_fa",
            field=models.CharField(blank=True, max_length=80, verbose_name="Category (فارسی)"),
        ),
        migrations.AddField(
            model_name="pricereference",
            name="category_en",
            field=models.CharField(blank=True, max_length=80, verbose_name="Category (English)"),
        ),
        migrations.AddField(
            model_name="pricereference",
            name="category_ar",
            field=models.CharField(blank=True, max_length=80, verbose_name="Category (العربية)"),
        ),
        migrations.AddField(
            model_name="pricereference",
            name="notes_fa",
            field=models.TextField(blank=True, verbose_name="Notes (فارسی)"),
        ),
        migrations.AddField(
            model_name="pricereference",
            name="notes_en",
            field=models.TextField(blank=True, verbose_name="Notes (English)"),
        ),
        migrations.AddField(
            model_name="pricereference",
            name="notes_ar",
            field=models.TextField(blank=True, verbose_name="Notes (العربية)"),
        ),
        migrations.AddField(
            model_name="pricereference",
            name="source_fa",
            field=models.CharField(blank=True, max_length=160, verbose_name="Source (فارسی)"),
        ),
        migrations.AddField(
            model_name="pricereference",
            name="source_en",
            field=models.CharField(blank=True, max_length=160, verbose_name="Source (English)"),
        ),
        migrations.AddField(
            model_name="pricereference",
            name="source_ar",
            field=models.CharField(blank=True, max_length=160, verbose_name="Source (العربية)"),
        ),
        migrations.RunPython(copy_price_langs, migrations.RunPython.noop),
        migrations.RemoveField(model_name="pricereference", name="title"),
        migrations.RemoveField(model_name="pricereference", name="category"),
        migrations.RemoveField(model_name="pricereference", name="notes"),
        migrations.RemoveField(model_name="pricereference", name="source"),
        migrations.AlterField(
            model_name="pricereference",
            name="title_fa",
            field=models.CharField(max_length=160, verbose_name="Title (فارسی)"),
        ),
        migrations.AlterField(
            model_name="pricereference",
            name="title_en",
            field=models.CharField(max_length=160, verbose_name="Title (English)"),
        ),
        migrations.AlterField(
            model_name="pricereference",
            name="title_ar",
            field=models.CharField(max_length=160, verbose_name="Title (العربية)"),
        ),
        migrations.AlterModelOptions(
            name="pricereference",
            options={"ordering": ["category_fa", "title_fa"]},
        ),
    ]
