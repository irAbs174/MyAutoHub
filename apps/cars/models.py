from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


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


class Trim(models.Model):
    car_model = models.ForeignKey(
        CarModel, on_delete=models.CASCADE, related_name="trims"
    )
    name = models.CharField(max_length=80)

    class Meta:
        ordering = ["car_model__brand__name", "car_model__name", "name"]
        unique_together = ("car_model", "name")

    def __str__(self):
        return f"{self.car_model} {self.name}"


class Car(models.Model):
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="cars")
    year = models.PositiveIntegerField()
    trim = models.ForeignKey(
        Trim,
        on_delete=models.PROTECT,
        related_name="cars",
        null=True,
        blank=True,
    )
    horsepower = models.PositiveIntegerField(null=True, blank=True)
    fuel_type = models.CharField(max_length=40, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="cars/covers/", blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-year", "model__brand__name", "model__name"]

    def __str__(self):
        parts = [str(self.model), str(self.year)]
        if self.trim_id:
            parts.append(self.trim.name)
        return " ".join(parts)

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


class TechnicalSpec(models.Model):
    car = models.OneToOneField(
        Car, on_delete=models.CASCADE, related_name="technical_spec"
    )
    engine = models.CharField(max_length=120, blank=True)
    displacement_cc = models.PositiveIntegerField(null=True, blank=True)
    cylinders = models.PositiveSmallIntegerField(null=True, blank=True)
    transmission = models.CharField(max_length=80, blank=True)
    drivetrain = models.CharField(max_length=40, blank=True)
    top_speed_kmh = models.PositiveIntegerField(null=True, blank=True)
    accel_0_100 = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    economy_city = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True
    )
    economy_highway = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True
    )
    emission_standard = models.CharField(max_length=40, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Specs for {self.car}"


class Dimensions(models.Model):
    car = models.OneToOneField(
        Car, on_delete=models.CASCADE, related_name="dimensions"
    )
    length_mm = models.PositiveIntegerField(null=True, blank=True)
    width_mm = models.PositiveIntegerField(null=True, blank=True)
    height_mm = models.PositiveIntegerField(null=True, blank=True)
    wheelbase_mm = models.PositiveIntegerField(null=True, blank=True)
    curb_weight_kg = models.PositiveIntegerField(null=True, blank=True)
    cargo_l = models.PositiveIntegerField(null=True, blank=True)
    seats = models.PositiveSmallIntegerField(null=True, blank=True)
    ground_clearance_mm = models.PositiveIntegerField(null=True, blank=True)
    fuel_tank_l = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "dimensions"

    def __str__(self):
        return f"Dimensions for {self.car}"


class FeatureCategory(models.TextChoices):
    SAFETY = "safety", _("Safety")
    COMFORT = "comfort", _("Comfort")
    TECH = "tech", _("Tech")
    EXTERIOR = "exterior", _("Exterior")
    OTHER = "other", _("Other")


class Feature(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="features")
    category = models.CharField(
        max_length=20,
        choices=FeatureCategory.choices,
        default=FeatureCategory.OTHER,
    )
    name = models.CharField(max_length=120)
    value = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class MaintenanceItem(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="maintenance_items"
    )
    title = models.CharField(max_length=160)
    interval_km = models.PositiveIntegerField(null=True, blank=True)
    interval_months = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    estimated_cost = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    class Meta:
        ordering = ["interval_km", "interval_months", "title"]

    def __str__(self):
        return self.title


class FluidType(models.TextChoices):
    ENGINE_OIL = "engine_oil", _("Engine oil")
    COOLANT = "coolant", _("Coolant")
    BRAKE = "brake", _("Brake fluid")
    TRANSMISSION = "transmission", _("Transmission fluid")
    WASHER = "washer", _("Washer fluid")
    OTHER = "other", _("Other")


class FluidSpec(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="fluids")
    fluid_type = models.CharField(max_length=20, choices=FluidType.choices)
    specification = models.CharField(max_length=120, blank=True)
    capacity = models.CharField(max_length=40, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["fluid_type"]

    def __str__(self):
        return f"{self.get_fluid_type_display()} ({self.car})"


class TirePosition(models.TextChoices):
    ALL = "all", _("All")
    FRONT = "front", _("Front")
    REAR = "rear", _("Rear")


class TireSpec(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="tires")
    position = models.CharField(
        max_length=10, choices=TirePosition.choices, default=TirePosition.ALL
    )
    size = models.CharField(max_length=40)
    pressure_psi = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    load_index = models.CharField(max_length=10, blank=True)
    speed_rating = models.CharField(max_length=5, blank=True)

    class Meta:
        ordering = ["position", "size"]

    def __str__(self):
        return f"{self.size} ({self.get_position_display()})"


class BatterySpec(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="batteries")
    group_size = models.CharField(max_length=20, blank=True)
    voltage = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    cca = models.PositiveIntegerField(null=True, blank=True)
    chemistry = models.CharField(max_length=40, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "battery specs"

    def __str__(self):
        return f"Battery for {self.car}"


class ServiceScheduleItem(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="service_schedule"
    )
    mileage_km = models.PositiveIntegerField(null=True, blank=True)
    months = models.PositiveIntegerField(null=True, blank=True)
    tasks = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "mileage_km", "months"]

    def __str__(self):
        return f"Service @ {self.mileage_km or '—'} km"


class OBDSeverity(models.TextChoices):
    INFO = "info", _("Info")
    WARNING = "warning", _("Warning")
    CRITICAL = "critical", _("Critical")


class OBDCode(models.Model):
    car_model = models.ForeignKey(
        CarModel, on_delete=models.CASCADE, related_name="obd_codes"
    )
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    severity = models.CharField(
        max_length=10,
        choices=OBDSeverity.choices,
        default=OBDSeverity.INFO,
    )

    class Meta:
        ordering = ["code"]
        unique_together = ("car_model", "code")

    def __str__(self):
        return f"{self.code} — {self.title}"


class Part(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="parts")
    name = models.CharField(max_length=160)
    oem_number = models.CharField(max_length=80, blank=True)
    category = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class CarCurrency(models.TextChoices):
    TOMAN = "تومان", _("Iran (تومان)")
    IRR = "IRR", _("Iran (IRR)")
    USD = "USD", _("United States (USD)")
    AED = "AED", _("United Arab Emirates (AED)")
    EUR = "EUR", _("Euro (EUR)")


class CarPrice(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="prices")
    label = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(
        max_length=8,
        choices=CarCurrency.choices,
        default=CarCurrency.TOMAN,
    )
    source = models.CharField(max_length=160, blank=True)
    notes = models.TextField(blank=True)
    recorded_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-recorded_at", "label"]

    def __str__(self):
        return f"{self.label}: {self.amount} {self.currency}"


class Dealer(models.Model):
    name = models.CharField(max_length=160)
    city = models.CharField(max_length=80, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    website = models.URLField(blank=True)
    brands = models.ManyToManyField(Brand, blank=True, related_name="dealers")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("places:dealer_detail", kwargs={"pk": self.pk})


class RepairShop(models.Model):
    name = models.CharField(max_length=160)
    city = models.CharField(max_length=80, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    website = models.URLField(blank=True)
    brands = models.ManyToManyField(Brand, blank=True, related_name="repair_shops")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("places:repair_shop_detail", kwargs={"pk": self.pk})
