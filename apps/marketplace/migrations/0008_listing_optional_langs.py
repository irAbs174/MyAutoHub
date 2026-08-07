from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marketplace", "0007_trilingual_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="title_fa",
            field=models.CharField(
                blank=True, default="", max_length=160, verbose_name="Title (فارسی)"
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="title_en",
            field=models.CharField(
                blank=True, default="", max_length=160, verbose_name="Title (English)"
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="title_ar",
            field=models.CharField(
                blank=True, default="", max_length=160, verbose_name="Title (العربية)"
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="description_fa",
            field=models.TextField(
                blank=True, default="", verbose_name="Description (فارسی)"
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="description_en",
            field=models.TextField(
                blank=True, default="", verbose_name="Description (English)"
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="description_ar",
            field=models.TextField(
                blank=True, default="", verbose_name="Description (العربية)"
            ),
        ),
    ]
