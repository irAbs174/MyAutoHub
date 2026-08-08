from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.i18n_content import localized


class MarketStatus(models.TextChoices):
    PRODUCTION = "production", _("In production")
    DISCONTINUED = "discontinued", _("Production stopped")
    IMPORTED = "imported", _("Imported")
    IMPORT_STOPPED = "import_stopped", _("Import stopped")
    ASSEMBLED = "assembled", _("Assembled locally")
    USED_AVAILABLE = "used_available", _("Used market available")


class BodyStyle(models.TextChoices):
    SEDAN = "sedan", _("Sedan")
    HATCHBACK = "hatchback", _("Hatchback")
    SUV = "suv", _("SUV")
    CROSSOVER = "crossover", _("Crossover")
    PICKUP = "pickup", _("Pickup")
    MPV = "mpv", _("MPV")
    COUPE = "coupe", _("Coupe")
    WAGON = "wagon", _("Wagon")
    CONVERTIBLE = "convertible", _("Convertible")
    VAN = "van", _("Van")
    OTHER = "other", _("Other")


class FeatureCategory(models.TextChoices):
    SAFETY = "safety", _("Safety")
    COMFORT = "comfort", _("Comfort")
    TECH = "tech", _("Tech")
    EXTERIOR = "exterior", _("Exterior")
    CABIN = "cabin", _("Cabin")
    MULTIMEDIA = "multimedia", _("Multimedia")
    OTHER = "other", _("Other")


class FeatureAvailability(models.TextChoices):
    STANDARD = "standard", _("Standard")
    NOT_AVAILABLE = "none", _("Not available")
    OPTIONAL = "optional", _("Optional")
    TRIM_SPECIFIC = "trim", _("Trim specific")


class FluidType(models.TextChoices):
    ENGINE_OIL = "engine_oil", _("Engine oil")
    COOLANT = "coolant", _("Coolant")
    BRAKE = "brake", _("Brake fluid")
    TRANSMISSION = "transmission", _("Transmission fluid")
    HYDRAULIC = "hydraulic", _("Hydraulic fluid")
    WASHER = "washer", _("Washer fluid")
    OTHER = "other", _("Other")


class TirePosition(models.TextChoices):
    ALL = "all", _("All")
    FRONT = "front", _("Front")
    REAR = "rear", _("Rear")


class OBDSeverity(models.TextChoices):
    INFO = "info", _("Info")
    WARNING = "warning", _("Warning")
    CRITICAL = "critical", _("Critical")


class CarCurrency(models.TextChoices):
    TOMAN = "تومان", _("Iran (تومان)")
    IRR = "IRR", _("Iran (IRR)")
    USD = "USD", _("United States (USD)")
    AED = "AED", _("United Arab Emirates (AED)")
    EUR = "EUR", _("Euro (EUR)")


class FailureArea(models.TextChoices):
    ENGINE = "engine", _("Engine")
    TRANSMISSION = "transmission", _("Transmission")
    ELECTRICAL = "electrical", _("Electrical")
    ECU = "ecu", _("ECU")
    SUSPENSION = "suspension", _("Suspension")
    BRAKES = "brakes", _("Brakes")
    AC = "ac", _("Air conditioning")
    HVAC = "hvac", _("Climate / HVAC")
    TURBO = "turbo", _("Turbo")
    TIMING = "timing", _("Timing belt / chain")
    CLUTCH = "clutch", _("Clutch")
    DIFFERENTIAL = "differential", _("Differential")
    BODY = "body", _("Body")
    PAINT = "paint", _("Paint")
    CABIN = "cabin", _("Cabin")
    OTHER = "other", _("Other")


class FailureSeverity(models.TextChoices):
    LOW = "low", _("Low")
    MEDIUM = "medium", _("Medium")
    HIGH = "high", _("High")
    CRITICAL = "critical", _("Critical")


class FailureLikelihood(models.TextChoices):
    RARE = "rare", _("Rare")
    OCCASIONAL = "occasional", _("Occasional")
    COMMON = "common", _("Common")
    VERY_COMMON = "very_common", _("Very common")


class ScoreField(models.PositiveSmallIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("null", True)
        kwargs.setdefault("blank", True)
        kwargs.setdefault(
            "validators",
            [MinValueValidator(1), MaxValueValidator(10)],
        )
        super().__init__(*args, **kwargs)


class Category(models.Model):
    """Practical / marketing tags: اقتصادی، خانوادگی، SUV، هیبرید, …"""

    slug = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=80)
    name_fa = models.CharField(
        max_length=80, blank=True, verbose_name=_("Name (فارسی)")
    )
    name_en = models.CharField(
        max_length=80, blank=True, verbose_name=_("Name (English)")
    )
    name_ar = models.CharField(
        max_length=80, blank=True, verbose_name=_("Name (العربية)")
    )
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return localized(self, "name") or self.name

    def get_absolute_url(self):
        return reverse("cars:category_detail", kwargs={"slug": self.slug})


class Brand(models.Model):
    name = models.CharField(max_length=80, unique=True)
    country = models.CharField(max_length=80, blank=True)
    manufacturer = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=80)
    name_fa = models.CharField(
        max_length=120, blank=True, verbose_name=_("Name (فارسی)")
    )
    name_en = models.CharField(
        max_length=120, blank=True, verbose_name=_("Name (English)")
    )
    name_ar = models.CharField(
        max_length=120, blank=True, verbose_name=_("Name (العربية)")
    )
    official_name = models.CharField(max_length=160, blank=True)
    model_code = models.CharField(max_length=80, blank=True)
    chassis_code = models.CharField(max_length=80, blank=True)
    generation = models.CharField(max_length=80, blank=True)
    body_style = models.CharField(
        max_length=20, choices=BodyStyle.choices, blank=True
    )
    introduced_year = models.PositiveIntegerField(null=True, blank=True)
    iran_entry_year = models.PositiveIntegerField(null=True, blank=True)
    production_start_year = models.PositiveIntegerField(null=True, blank=True)
    production_end_year = models.PositiveIntegerField(null=True, blank=True)
    categories = models.ManyToManyField(
        Category, blank=True, related_name="car_models"
    )

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
    description_fa = models.TextField(
        blank=True, default="", verbose_name=_("Description (فارسی)")
    )
    description_en = models.TextField(
        blank=True, default="", verbose_name=_("Description (English)")
    )
    description_ar = models.TextField(
        blank=True, default="", verbose_name=_("Description (العربية)")
    )
    cover_image = models.ImageField(upload_to="cars/covers/", blank=True)
    is_published = models.BooleanField(default=True)

    # Identity / Iran market passport
    official_name_fa = models.CharField(
        max_length=160, blank=True, default="", verbose_name=_("Official name (فارسی)")
    )
    official_name_en = models.CharField(
        max_length=160,
        blank=True,
        default="",
        verbose_name=_("Official name (English)"),
    )
    official_name_ar = models.CharField(
        max_length=160,
        blank=True,
        default="",
        verbose_name=_("Official name (العربية)"),
    )
    name_fa = models.CharField(
        max_length=120, blank=True, default="", verbose_name=_("Display name (فارسی)")
    )
    name_en = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Display name (English)"),
    )
    name_ar = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Display name (العربية)"),
    )
    model_code = models.CharField(max_length=80, blank=True)
    chassis_code = models.CharField(max_length=80, blank=True)
    generation = models.CharField(max_length=80, blank=True)
    facelift = models.CharField(max_length=80, blank=True)
    body_style = models.CharField(
        max_length=20, choices=BodyStyle.choices, blank=True
    )
    manufacturer = models.CharField(max_length=120, blank=True)
    importer = models.CharField(max_length=120, blank=True)
    assembler = models.CharField(max_length=120, blank=True)
    country_of_origin = models.CharField(max_length=80, blank=True)
    country_of_assembly = models.CharField(max_length=80, blank=True)
    introduced_year = models.PositiveIntegerField(null=True, blank=True)
    iran_entry_year = models.PositiveIntegerField(null=True, blank=True)
    production_start_year = models.PositiveIntegerField(null=True, blank=True)
    production_end_year = models.PositiveIntegerField(null=True, blank=True)
    market_status = models.CharField(
        max_length=20, choices=MarketStatus.choices, blank=True
    )
    doors = models.PositiveSmallIntegerField(null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True, related_name="cars")

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

    @property
    def description(self):
        return localized(self, "description")

    @property
    def official_name(self):
        return localized(self, "official_name")

    @property
    def display_name(self):
        return (
            localized(self, "name")
            or localized(self.model, "name")
            or self.model.name
        )

    @property
    def display_name_fa(self):
        return self.name_fa or self.model.name_fa or self.model.name

    @property
    def display_name_en(self):
        return self.name_en or self.model.name_en or self.model.name

    @property
    def display_name_ar(self):
        return self.name_ar or getattr(self.model, "name_ar", "") or self.model.name


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
    # Legacy / summary
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

    # Engine detail
    engine_code = models.CharField(max_length=80, blank=True)
    engine_type = models.CharField(max_length=80, blank=True)
    cylinder_arrangement = models.CharField(max_length=40, blank=True)
    valves = models.PositiveSmallIntegerField(null=True, blank=True)
    camshaft = models.CharField(max_length=40, blank=True)  # DOHC / SOHC
    aspiration = models.CharField(max_length=40, blank=True)  # NA / turbo / …
    supercharged = models.BooleanField(default=False)
    fuel_injection = models.CharField(max_length=80, blank=True)
    fuel_type_detail = models.CharField(max_length=40, blank=True)
    power_hp = models.PositiveIntegerField(null=True, blank=True)
    power_rpm = models.PositiveIntegerField(null=True, blank=True)
    torque_nm = models.PositiveIntegerField(null=True, blank=True)
    torque_rpm = models.PositiveIntegerField(null=True, blank=True)
    compression_ratio = models.CharField(max_length=20, blank=True)
    engine_oil_capacity_l = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    engine_oil_type = models.CharField(max_length=80, blank=True)
    coolant_capacity_l = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    cooling_system = models.CharField(max_length=80, blank=True)

    # Transmission detail
    gearbox_type = models.CharField(max_length=40, blank=True)  # AT / CVT / DCT / AMT
    gears = models.PositiveSmallIntegerField(null=True, blank=True)
    transmission_mode = models.CharField(max_length=40, blank=True)  # manual/auto
    clutch_type = models.CharField(max_length=80, blank=True)
    reverse_gears = models.PositiveSmallIntegerField(null=True, blank=True)
    drive_modes = models.CharField(max_length=160, blank=True)
    tiptronic = models.BooleanField(default=False)
    paddle_shifters = models.BooleanField(default=False)

    # Performance extras
    economy_combined = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True
    )
    range_km = models.PositiveIntegerField(null=True, blank=True)
    co2_g_km = models.PositiveIntegerField(null=True, blank=True)
    towing_capacity_kg = models.PositiveIntegerField(null=True, blank=True)

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
    track_front_mm = models.PositiveIntegerField(null=True, blank=True)
    track_rear_mm = models.PositiveIntegerField(null=True, blank=True)
    turning_circle_m = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    cargo_seats_folded_l = models.PositiveIntegerField(null=True, blank=True)
    cabin_volume_l = models.PositiveIntegerField(null=True, blank=True)
    gross_weight_kg = models.PositiveIntegerField(null=True, blank=True)
    payload_kg = models.PositiveIntegerField(null=True, blank=True)
    doors = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "dimensions"

    def __str__(self):
        return f"Dimensions for {self.car}"


class SuspensionSpec(models.Model):
    car = models.OneToOneField(
        Car, on_delete=models.CASCADE, related_name="suspension"
    )
    front_type = models.CharField(max_length=120, blank=True)
    front_shock = models.CharField(max_length=80, blank=True)
    front_spring = models.CharField(max_length=80, blank=True)
    rear_type = models.CharField(max_length=120, blank=True)
    rear_shock = models.CharField(max_length=80, blank=True)
    rear_spring = models.CharField(max_length=80, blank=True)
    steering_system = models.CharField(max_length=80, blank=True)
    steering_type = models.CharField(max_length=80, blank=True)
    steering_assist = models.CharField(max_length=40, blank=True)  # electric/hydraulic
    turning_radius_m = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Suspension for {self.car}"


class BrakeSpec(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name="brakes")
    front_brake = models.CharField(max_length=80, blank=True)
    rear_brake = models.CharField(max_length=80, blank=True)
    front_type = models.CharField(max_length=40, blank=True)  # disc/drum
    rear_type = models.CharField(max_length=40, blank=True)
    abs = models.BooleanField(default=False)
    ebd = models.BooleanField(default=False)
    ba = models.BooleanField(default=False)
    esp = models.BooleanField(default=False)
    tcs = models.BooleanField(default=False)
    auto_hold = models.BooleanField(default=False)
    electric_parking_brake = models.BooleanField(default=False)
    aeb = models.BooleanField(default=False)
    assist_systems = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Brakes for {self.car}"


class WheelSpec(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name="wheels")
    rim_size = models.CharField(max_length=40, blank=True)
    rim_material = models.CharField(max_length=40, blank=True)
    front_tire_size = models.CharField(max_length=40, blank=True)
    rear_tire_size = models.CharField(max_length=40, blank=True)
    spare_tire = models.BooleanField(default=False)
    spare_type = models.CharField(max_length=80, blank=True)
    tpms = models.BooleanField(default=False)
    standard_pressure = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Wheels for {self.car}"


class CabinSpec(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name="cabin")
    dashboard_material = models.CharField(max_length=80, blank=True)
    seat_material = models.CharField(max_length=80, blank=True)
    upholstery = models.CharField(max_length=40, blank=True)  # leather/fabric
    seat_count = models.PositiveSmallIntegerField(null=True, blank=True)
    driver_seat_adjust = models.CharField(max_length=120, blank=True)
    passenger_seat_adjust = models.CharField(max_length=120, blank=True)
    rear_seat_adjust = models.CharField(max_length=120, blank=True)
    front_legroom_mm = models.PositiveIntegerField(null=True, blank=True)
    rear_legroom_mm = models.PositiveIntegerField(null=True, blank=True)
    headroom_mm = models.PositiveIntegerField(null=True, blank=True)
    armrest = models.BooleanField(default=False)
    cupholders = models.BooleanField(default=False)
    rear_ac_vents = models.BooleanField(default=False)
    power_tailgate = models.BooleanField(default=False)
    rear_seats_fold = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Cabin for {self.car}"


class MultimediaSpec(models.Model):
    car = models.OneToOneField(
        Car, on_delete=models.CASCADE, related_name="multimedia"
    )
    center_display = models.BooleanField(default=False)
    display_size_inch = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    audio_system = models.CharField(max_length=120, blank=True)
    speakers = models.PositiveSmallIntegerField(null=True, blank=True)
    amplifier = models.BooleanField(default=False)
    subwoofer = models.BooleanField(default=False)
    bluetooth = models.BooleanField(default=False)
    usb = models.BooleanField(default=False)
    aux = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    apple_carplay = models.BooleanField(default=False)
    android_auto = models.BooleanField(default=False)
    navigation = models.BooleanField(default=False)
    mirrorlink = models.BooleanField(default=False)
    voice_control = models.BooleanField(default=False)
    phone_connectivity = models.CharField(max_length=120, blank=True)
    digital_cluster = models.BooleanField(default=False)
    head_up_display = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Multimedia for {self.car}"


class Feature(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="features")
    category = models.CharField(
        max_length=20,
        choices=FeatureCategory.choices,
        default=FeatureCategory.OTHER,
    )
    key = models.CharField(max_length=80, blank=True)
    name = models.CharField(max_length=120)
    value = models.CharField(max_length=160, blank=True)
    availability = models.CharField(
        max_length=20,
        choices=FeatureAvailability.choices,
        default=FeatureAvailability.STANDARD,
    )

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


class FluidSpec(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="fluids")
    fluid_type = models.CharField(max_length=20, choices=FluidType.choices)
    specification = models.CharField(max_length=120, blank=True)
    grade = models.CharField(max_length=40, blank=True)
    capacity = models.CharField(max_length=40, blank=True)
    interval_km = models.PositiveIntegerField(null=True, blank=True)
    interval_months = models.PositiveIntegerField(null=True, blank=True)
    estimated_cost = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["fluid_type"]

    def __str__(self):
        return f"{self.get_fluid_type_display()} ({self.car})"


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
    rim_size = models.CharField(max_length=40, blank=True)
    rim_material = models.CharField(max_length=40, blank=True)

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
    is_consumable = models.BooleanField(default=False)
    interval_km = models.PositiveIntegerField(null=True, blank=True)
    interval_months = models.PositiveIntegerField(null=True, blank=True)
    estimated_cost = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class CommonFailure(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="common_failures"
    )
    area = models.CharField(
        max_length=20, choices=FailureArea.choices, default=FailureArea.OTHER
    )
    title = models.CharField(max_length=160)
    severity = models.CharField(
        max_length=20,
        choices=FailureSeverity.choices,
        default=FailureSeverity.MEDIUM,
    )
    likelihood = models.CharField(
        max_length=20,
        choices=FailureLikelihood.choices,
        default=FailureLikelihood.OCCASIONAL,
    )
    repair_cost_min = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    repair_cost_max = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    currency = models.CharField(
        max_length=8,
        choices=CarCurrency.choices,
        default=CarCurrency.TOMAN,
    )
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["area", "title"]

    def __str__(self):
        return self.title


class MarketInfo(models.Model):
    """Iran market snapshot for a catalog car."""

    car = models.OneToOneField(
        Car, on_delete=models.CASCADE, related_name="market_info"
    )
    factory_price = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    market_price_new = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    market_price_used = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    currency = models.CharField(
        max_length=8,
        choices=CarCurrency.choices,
        default=CarCurrency.TOMAN,
    )
    depreciation_pct = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    liquidity_score = ScoreField()
    demand_score = ScoreField()
    popularity_score = ScoreField()
    maintenance_cost_annual = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    insurance_cost_annual = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    service_cost_avg = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    parts_price_index = ScoreField()
    parts_availability = ScoreField()
    mechanic_availability = ScoreField()
    notes = models.TextField(blank=True)
    recorded_at = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "market info"

    def __str__(self):
        return f"Market info for {self.car}"


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
    year_for_price = models.PositiveIntegerField(null=True, blank=True)
    mileage_km = models.PositiveIntegerField(null=True, blank=True)

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
