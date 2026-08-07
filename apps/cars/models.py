from django.db import models
from django.urls import reverse


class Brand(models.Model):
    name = models.CharField(max_length=80, unique=True)
    country = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=80)

    class Meta:
        ordering = ["brand__name", "name"]
        unique_together = ("brand", "name")

    def __str__(self):
        return f"{self.brand} {self.name}"


class Car(models.Model):
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="cars")
    year = models.PositiveIntegerField()
    trim = models.CharField(max_length=80, blank=True)
    horsepower = models.PositiveIntegerField(null=True, blank=True)
    fuel_type = models.CharField(max_length=40, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="cars/covers/", blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-year", "model__brand__name", "model__name"]

    def __str__(self):
        return f"{self.model} ({self.year})"

    def get_absolute_url(self):
        return reverse("cars:detail", kwargs={"pk": self.pk})

    @property
    def main_image(self):
        if self.cover_image:
            return self.cover_image
        photo = self.photos.order_by("sort_order", "id").first()
        return photo.image if photo else None


class CarPhoto(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="cars/gallery/")
    caption = models.CharField(max_length=160, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"Photo {self.pk} for {self.car}"
