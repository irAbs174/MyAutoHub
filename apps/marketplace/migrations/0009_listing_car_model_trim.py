import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cars", "0002_add_cover_images"),
        ("marketplace", "0008_listing_optional_langs"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="car_model",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="listings",
                to="cars.carmodel",
            ),
        ),
        migrations.AddField(
            model_name="listing",
            name="trim",
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
