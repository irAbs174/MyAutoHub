# Generated manually for trilingual content fields

from django.db import migrations, models


def copy_listing_langs(apps, schema_editor):
    Listing = apps.get_model("marketplace", "Listing")
    for item in Listing.objects.all():
        title = item.title or ""
        description = item.description or ""
        item.title_fa = title
        item.title_en = title
        item.title_ar = title
        item.description_fa = description
        item.description_en = description
        item.description_ar = description
        item.save(
            update_fields=[
                "title_fa",
                "title_en",
                "title_ar",
                "description_fa",
                "description_en",
                "description_ar",
            ]
        )


class Migration(migrations.Migration):
    dependencies = [
        ("marketplace", "0006_add_gallery_photos"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="title_fa",
            field=models.CharField(max_length=160, null=True, verbose_name="Title (فارسی)"),
        ),
        migrations.AddField(
            model_name="listing",
            name="title_en",
            field=models.CharField(max_length=160, null=True, verbose_name="Title (English)"),
        ),
        migrations.AddField(
            model_name="listing",
            name="title_ar",
            field=models.CharField(max_length=160, null=True, verbose_name="Title (العربية)"),
        ),
        migrations.AddField(
            model_name="listing",
            name="description_fa",
            field=models.TextField(null=True, verbose_name="Description (فارسی)"),
        ),
        migrations.AddField(
            model_name="listing",
            name="description_en",
            field=models.TextField(null=True, verbose_name="Description (English)"),
        ),
        migrations.AddField(
            model_name="listing",
            name="description_ar",
            field=models.TextField(null=True, verbose_name="Description (العربية)"),
        ),
        migrations.RunPython(copy_listing_langs, migrations.RunPython.noop),
        migrations.RemoveField(model_name="listing", name="title"),
        migrations.RemoveField(model_name="listing", name="description"),
        migrations.AlterField(
            model_name="listing",
            name="title_fa",
            field=models.CharField(max_length=160, verbose_name="Title (فارسی)"),
        ),
        migrations.AlterField(
            model_name="listing",
            name="title_en",
            field=models.CharField(max_length=160, verbose_name="Title (English)"),
        ),
        migrations.AlterField(
            model_name="listing",
            name="title_ar",
            field=models.CharField(max_length=160, verbose_name="Title (العربية)"),
        ),
        migrations.AlterField(
            model_name="listing",
            name="description_fa",
            field=models.TextField(verbose_name="Description (فارسی)"),
        ),
        migrations.AlterField(
            model_name="listing",
            name="description_en",
            field=models.TextField(verbose_name="Description (English)"),
        ),
        migrations.AlterField(
            model_name="listing",
            name="description_ar",
            field=models.TextField(verbose_name="Description (العربية)"),
        ),
    ]
