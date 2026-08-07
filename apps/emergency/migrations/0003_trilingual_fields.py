# Generated manually for trilingual content fields

from django.db import migrations, models


def copy_emergency_service_langs(apps, schema_editor):
    EmergencyService = apps.get_model("emergency", "EmergencyService")
    for svc in EmergencyService.objects.all():
        name = svc.name or ""
        description = svc.description or ""
        coverage = svc.coverage_notes or ""
        svc.name_fa = name
        svc.name_en = name
        svc.name_ar = name
        svc.description_fa = description
        svc.description_en = description
        svc.description_ar = description
        svc.coverage_notes_fa = coverage
        svc.coverage_notes_en = coverage
        svc.coverage_notes_ar = coverage
        svc.save(
            update_fields=[
                "name_fa",
                "name_en",
                "name_ar",
                "description_fa",
                "description_en",
                "description_ar",
                "coverage_notes_fa",
                "coverage_notes_en",
                "coverage_notes_ar",
            ]
        )


class Migration(migrations.Migration):
    dependencies = [
        ("emergency", "0002_add_cover_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="emergencyservice",
            name="name_fa",
            field=models.CharField(max_length=120, null=True, verbose_name="Name (فارسی)"),
        ),
        migrations.AddField(
            model_name="emergencyservice",
            name="name_en",
            field=models.CharField(max_length=120, null=True, verbose_name="Name (English)"),
        ),
        migrations.AddField(
            model_name="emergencyservice",
            name="name_ar",
            field=models.CharField(max_length=120, null=True, verbose_name="Name (العربية)"),
        ),
        migrations.AddField(
            model_name="emergencyservice",
            name="description_fa",
            field=models.TextField(blank=True, verbose_name="Description (فارسی)"),
        ),
        migrations.AddField(
            model_name="emergencyservice",
            name="description_en",
            field=models.TextField(blank=True, verbose_name="Description (English)"),
        ),
        migrations.AddField(
            model_name="emergencyservice",
            name="description_ar",
            field=models.TextField(blank=True, verbose_name="Description (العربية)"),
        ),
        migrations.AddField(
            model_name="emergencyservice",
            name="coverage_notes_fa",
            field=models.TextField(blank=True, verbose_name="Coverage notes (فارسی)"),
        ),
        migrations.AddField(
            model_name="emergencyservice",
            name="coverage_notes_en",
            field=models.TextField(blank=True, verbose_name="Coverage notes (English)"),
        ),
        migrations.AddField(
            model_name="emergencyservice",
            name="coverage_notes_ar",
            field=models.TextField(blank=True, verbose_name="Coverage notes (العربية)"),
        ),
        migrations.RunPython(copy_emergency_service_langs, migrations.RunPython.noop),
        migrations.RemoveField(model_name="emergencyservice", name="name"),
        migrations.RemoveField(model_name="emergencyservice", name="description"),
        migrations.RemoveField(model_name="emergencyservice", name="coverage_notes"),
        migrations.AlterField(
            model_name="emergencyservice",
            name="name_fa",
            field=models.CharField(max_length=120, verbose_name="Name (فارسی)"),
        ),
        migrations.AlterField(
            model_name="emergencyservice",
            name="name_en",
            field=models.CharField(max_length=120, verbose_name="Name (English)"),
        ),
        migrations.AlterField(
            model_name="emergencyservice",
            name="name_ar",
            field=models.CharField(max_length=120, verbose_name="Name (العربية)"),
        ),
        migrations.AlterModelOptions(
            name="emergencyservice",
            options={"ordering": ["name_fa"]},
        ),
    ]
