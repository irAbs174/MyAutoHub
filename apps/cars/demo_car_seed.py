"""Full demo catalog profiles used by seed_demo."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from apps.cars.models import (
    BatterySpec,
    BodyStyle,
    BrakeSpec,
    CabinSpec,
    CarCurrency,
    CommonFailure,
    Dimensions,
    FailureArea,
    FailureLikelihood,
    FailureSeverity,
    Feature,
    FeatureAvailability,
    FeatureCategory,
    FluidSpec,
    FluidType,
    MaintenanceItem,
    MarketInfo,
    MarketStatus,
    MultimediaSpec,
    OBDCode,
    OBDSeverity,
    Part,
    ServiceScheduleItem,
    SuspensionSpec,
    TechnicalSpec,
    TirePosition,
    TireSpec,
    WheelSpec,
)
from apps.core.i18n_content import tri_fields

# brand -> model -> profile metadata shared by year variants
MODEL_PROFILES = {
    ("BMW", "M4"): {
        "body_style": BodyStyle.COUPE,
        "categories": ("sport", "luxury"),
        "generation": "G82",
        "chassis_code": "G82",
        "model_code": "M4",
        "doors": 2,
        "market_status": MarketStatus.IMPORTED,
        "country_of_origin": "Germany",
        "country_of_assembly": "Germany",
        "introduced_year": 2020,
        "iran_entry_year": 2022,
        "name_fa": "بی‌ام‌و M4",
        "name_en": "BMW M4",
        "name_ar": "بي إم دبليو M4",
        "official_name_fa": "بی‌ام‌و M4 Competition",
        "official_name_en": "BMW M4 Competition",
        "official_name_ar": "بي إم دبليو M4 Competition",
        "tech": {
            "engine": "3.0L Twin-Turbo I6",
            "engine_code": "S58B30",
            "engine_type": "Inline-6",
            "cylinder_arrangement": "I6",
            "displacement_cc": 2993,
            "cylinders": 6,
            "valves": 24,
            "camshaft": "DOHC",
            "aspiration": "twin-turbo",
            "fuel_injection": "Direct injection",
            "fuel_type_detail": "gasoline",
            "power_hp": 503,
            "power_rpm": 6250,
            "torque_nm": 650,
            "torque_rpm": 2750,
            "compression_ratio": "9.3:1",
            "transmission": "8-speed automatic",
            "gearbox_type": "AT",
            "gears": 8,
            "transmission_mode": "automatic",
            "drivetrain": "RWD",
            "paddle_shifters": True,
            "tiptronic": True,
            "drive_modes": "Comfort, Sport, Sport Plus",
            "top_speed_kmh": 290,
            "accel_0_100": Decimal("3.9"),
            "economy_city": Decimal("14.2"),
            "economy_highway": Decimal("9.8"),
            "economy_combined": Decimal("11.5"),
            "emission_standard": "Euro 6d",
            "co2_g_km": 262,
            "engine_oil_capacity_l": Decimal("7.0"),
            "engine_oil_type": "0W-30 LL-01",
            "coolant_capacity_l": Decimal("10.5"),
            "cooling_system": "Liquid",
        },
        "dims": {
            "length_mm": 4794,
            "width_mm": 1887,
            "height_mm": 1393,
            "wheelbase_mm": 2857,
            "curb_weight_kg": 1730,
            "cargo_l": 440,
            "seats": 4,
            "doors": 2,
            "ground_clearance_mm": 120,
            "fuel_tank_l": Decimal("59.0"),
            "turning_circle_m": Decimal("12.2"),
            "gross_weight_kg": 2150,
        },
        "tire_size": "275/35R19",
        "rim_size": "19 inch",
        "price_toman": Decimal("18500000000"),
    },
    ("BMW", "320i"): {
        "body_style": BodyStyle.SEDAN,
        "categories": ("sedan", "family", "luxury"),
        "generation": "G20",
        "chassis_code": "G20",
        "doors": 4,
        "market_status": MarketStatus.IMPORTED,
        "country_of_origin": "Germany",
        "introduced_year": 2018,
        "iran_entry_year": 2019,
        "name_fa": "بی‌ام‌و 320i",
        "name_en": "BMW 320i",
        "name_ar": "بي إم دبليو 320i",
        "tech": {
            "engine": "2.0L Turbo I4",
            "engine_code": "B48B20",
            "displacement_cc": 1998,
            "cylinders": 4,
            "valves": 16,
            "camshaft": "DOHC",
            "aspiration": "turbo",
            "power_hp": 184,
            "torque_nm": 300,
            "transmission": "8-speed automatic",
            "gearbox_type": "AT",
            "gears": 8,
            "drivetrain": "RWD",
            "top_speed_kmh": 235,
            "accel_0_100": Decimal("7.1"),
            "economy_combined": Decimal("6.8"),
            "emission_standard": "Euro 6",
            "paddle_shifters": True,
        },
        "dims": {
            "length_mm": 4709,
            "width_mm": 1827,
            "height_mm": 1442,
            "wheelbase_mm": 2851,
            "curb_weight_kg": 1545,
            "cargo_l": 480,
            "seats": 5,
            "doors": 4,
            "fuel_tank_l": Decimal("59.0"),
        },
        "tire_size": "225/50R17",
        "rim_size": "17 inch",
        "price_toman": Decimal("7200000000"),
    },
    ("BMW", "X3"): {
        "body_style": BodyStyle.SUV,
        "categories": ("suv", "family", "luxury"),
        "generation": "G01",
        "doors": 5,
        "market_status": MarketStatus.IMPORTED,
        "country_of_origin": "USA",
        "introduced_year": 2017,
        "iran_entry_year": 2018,
        "name_fa": "بی‌ام‌و X3",
        "name_en": "BMW X3",
        "name_ar": "بي إم دبليو X3",
        "tech": {
            "engine": "2.0L Turbo I4",
            "displacement_cc": 1998,
            "cylinders": 4,
            "aspiration": "turbo",
            "power_hp": 248,
            "torque_nm": 350,
            "transmission": "8-speed automatic",
            "gearbox_type": "AT",
            "gears": 8,
            "drivetrain": "AWD",
            "top_speed_kmh": 235,
            "accel_0_100": Decimal("6.3"),
            "economy_combined": Decimal("8.1"),
            "emission_standard": "Euro 6",
        },
        "dims": {
            "length_mm": 4708,
            "width_mm": 1891,
            "height_mm": 1676,
            "wheelbase_mm": 2864,
            "curb_weight_kg": 1820,
            "cargo_l": 550,
            "cargo_seats_folded_l": 1600,
            "seats": 5,
            "doors": 5,
            "ground_clearance_mm": 204,
            "fuel_tank_l": Decimal("65.0"),
        },
        "tire_size": "245/50R19",
        "rim_size": "19 inch",
        "price_toman": Decimal("9800000000"),
    },
    ("Porsche", "911"): {
        "body_style": BodyStyle.COUPE,
        "categories": ("sport", "luxury"),
        "generation": "992",
        "chassis_code": "992",
        "doors": 2,
        "market_status": MarketStatus.IMPORTED,
        "country_of_origin": "Germany",
        "introduced_year": 2019,
        "iran_entry_year": 2021,
        "name_fa": "پورشه 911",
        "name_en": "Porsche 911",
        "name_ar": "بورشه 911",
        "tech": {
            "engine": "3.0L Twin-Turbo Flat-6",
            "engine_code": "9A2",
            "engine_type": "Boxer-6",
            "displacement_cc": 2981,
            "cylinders": 6,
            "aspiration": "twin-turbo",
            "power_hp": 379,
            "torque_nm": 450,
            "transmission": "8-speed PDK",
            "gearbox_type": "DCT",
            "gears": 8,
            "drivetrain": "RWD",
            "paddle_shifters": True,
            "top_speed_kmh": 293,
            "accel_0_100": Decimal("4.2"),
            "economy_combined": Decimal("10.8"),
            "emission_standard": "Euro 6d",
        },
        "dims": {
            "length_mm": 4519,
            "width_mm": 1852,
            "height_mm": 1298,
            "wheelbase_mm": 2450,
            "curb_weight_kg": 1505,
            "cargo_l": 132,
            "seats": 4,
            "doors": 2,
            "fuel_tank_l": Decimal("64.0"),
        },
        "tire_size": "245/35R20",
        "rim_size": "20 inch",
        "price_toman": Decimal("28000000000"),
    },
    ("Hyundai", "N Vision 74"): {
        "body_style": BodyStyle.COUPE,
        "categories": ("sport", "hybrid", "luxury"),
        "generation": "Concept",
        "doors": 2,
        "market_status": MarketStatus.IMPORTED,
        "country_of_origin": "South Korea",
        "introduced_year": 2022,
        "name_fa": "هیوندای N Vision 74",
        "name_en": "Hyundai N Vision 74",
        "name_ar": "هيونداي N Vision 74",
        "tech": {
            "engine": "Hydrogen fuel-cell hybrid",
            "engine_type": "FCEV hybrid",
            "power_hp": 670,
            "torque_nm": 900,
            "transmission": "Single-speed",
            "gearbox_type": "AT",
            "gears": 1,
            "drivetrain": "AWD",
            "top_speed_kmh": 250,
            "accel_0_100": Decimal("4.0"),
            "range_km": 600,
            "emission_standard": "Zero local",
            "fuel_type_detail": "hydrogen/electric",
        },
        "dims": {
            "length_mm": 4685,
            "width_mm": 1955,
            "height_mm": 1335,
            "wheelbase_mm": 2900,
            "curb_weight_kg": 1950,
            "seats": 2,
            "doors": 2,
            "fuel_tank_l": Decimal("42.0"),
        },
        "tire_size": "275/35R21",
        "rim_size": "21 inch",
        "price_toman": Decimal("0"),
    },
    ("Hyundai", "Tucson"): {
        "body_style": BodyStyle.CROSSOVER,
        "categories": ("crossover", "family", "suv"),
        "generation": "NX4",
        "doors": 5,
        "market_status": MarketStatus.IMPORTED,
        "country_of_origin": "South Korea",
        "introduced_year": 2020,
        "iran_entry_year": 2021,
        "name_fa": "هیوندای توسان",
        "name_en": "Hyundai Tucson",
        "name_ar": "هيونداي توسان",
        "tech": {
            "engine": "2.5L I4",
            "displacement_cc": 2497,
            "cylinders": 4,
            "aspiration": "NA",
            "power_hp": 187,
            "torque_nm": 241,
            "transmission": "8-speed automatic",
            "gearbox_type": "AT",
            "gears": 8,
            "drivetrain": "FWD",
            "top_speed_kmh": 201,
            "accel_0_100": Decimal("9.0"),
            "economy_combined": Decimal("8.2"),
            "emission_standard": "Euro 6",
        },
        "dims": {
            "length_mm": 4630,
            "width_mm": 1865,
            "height_mm": 1665,
            "wheelbase_mm": 2755,
            "curb_weight_kg": 1580,
            "cargo_l": 539,
            "seats": 5,
            "doors": 5,
            "ground_clearance_mm": 181,
            "fuel_tank_l": Decimal("54.0"),
        },
        "tire_size": "235/55R19",
        "rim_size": "19 inch",
        "price_toman": Decimal("4500000000"),
    },
    ("Hyundai", "Elantra"): {
        "body_style": BodyStyle.SEDAN,
        "categories": ("sedan", "family", "urban"),
        "generation": "CN7",
        "doors": 4,
        "market_status": MarketStatus.IMPORTED,
        "country_of_origin": "South Korea",
        "introduced_year": 2020,
        "iran_entry_year": 2021,
        "name_fa": "هیوندای الانترا",
        "name_en": "Hyundai Elantra",
        "name_ar": "هيونداي إلنترا",
        "tech": {
            "engine": "2.0L I4",
            "displacement_cc": 1999,
            "cylinders": 4,
            "power_hp": 147,
            "torque_nm": 179,
            "transmission": "CVT",
            "gearbox_type": "CVT",
            "drivetrain": "FWD",
            "top_speed_kmh": 190,
            "accel_0_100": Decimal("9.8"),
            "economy_combined": Decimal("6.9"),
            "emission_standard": "Euro 6",
        },
        "dims": {
            "length_mm": 4675,
            "width_mm": 1825,
            "height_mm": 1430,
            "wheelbase_mm": 2720,
            "curb_weight_kg": 1310,
            "cargo_l": 474,
            "seats": 5,
            "doors": 4,
            "fuel_tank_l": Decimal("47.0"),
        },
        "tire_size": "205/55R16",
        "rim_size": "16 inch",
        "price_toman": Decimal("2800000000"),
    },
    ("Bugatti", "Chiron"): {
        "body_style": BodyStyle.COUPE,
        "categories": ("sport", "luxury"),
        "generation": "Chiron",
        "doors": 2,
        "market_status": MarketStatus.IMPORTED,
        "country_of_origin": "France",
        "introduced_year": 2016,
        "name_fa": "بوگاتی شیرون",
        "name_en": "Bugatti Chiron",
        "name_ar": "بوجاتي شيرون",
        "tech": {
            "engine": "8.0L Quad-Turbo W16",
            "engine_type": "W16",
            "displacement_cc": 7993,
            "cylinders": 16,
            "aspiration": "quad-turbo",
            "power_hp": 1500,
            "torque_nm": 1600,
            "transmission": "7-speed DCT",
            "gearbox_type": "DCT",
            "gears": 7,
            "drivetrain": "AWD",
            "paddle_shifters": True,
            "top_speed_kmh": 420,
            "accel_0_100": Decimal("2.4"),
            "economy_combined": Decimal("22.5"),
            "emission_standard": "Euro 6",
        },
        "dims": {
            "length_mm": 4544,
            "width_mm": 2038,
            "height_mm": 1212,
            "wheelbase_mm": 2711,
            "curb_weight_kg": 1995,
            "cargo_l": 44,
            "seats": 2,
            "doors": 2,
            "fuel_tank_l": Decimal("100.0"),
        },
        "tire_size": "285/30R20",
        "rim_size": "20 inch",
        "price_toman": Decimal("150000000000"),
    },
    ("Toyota", "Corolla"): {
        "body_style": BodyStyle.SEDAN,
        "categories": ("sedan", "family", "economy"),
        "generation": "E210",
        "doors": 4,
        "market_status": MarketStatus.IMPORTED,
        "country_of_origin": "Japan",
        "introduced_year": 2018,
        "iran_entry_year": 2019,
        "name_fa": "تویوتا کرولا",
        "name_en": "Toyota Corolla",
        "name_ar": "تويوتا كورولا",
        "tech": {
            "engine": "2.0L I4",
            "displacement_cc": 1987,
            "cylinders": 4,
            "power_hp": 169,
            "torque_nm": 200,
            "transmission": "CVT",
            "gearbox_type": "CVT",
            "drivetrain": "FWD",
            "top_speed_kmh": 180,
            "accel_0_100": Decimal("9.5"),
            "economy_city": Decimal("7.1"),
            "economy_highway": Decimal("5.4"),
            "economy_combined": Decimal("6.2"),
            "emission_standard": "Euro 6",
        },
        "dims": {
            "length_mm": 4630,
            "width_mm": 1780,
            "height_mm": 1435,
            "wheelbase_mm": 2700,
            "curb_weight_kg": 1380,
            "cargo_l": 470,
            "seats": 5,
            "doors": 4,
            "fuel_tank_l": Decimal("50.0"),
        },
        "tire_size": "205/55R16",
        "rim_size": "16 inch",
        "price_toman": Decimal("3200000000"),
    },
    ("Toyota", "Camry"): {
        "body_style": BodyStyle.SEDAN,
        "categories": ("sedan", "family", "hybrid"),
        "generation": "XV70",
        "doors": 4,
        "market_status": MarketStatus.IMPORTED,
        "country_of_origin": "Japan",
        "introduced_year": 2017,
        "iran_entry_year": 2018,
        "name_fa": "تویوتا کمری",
        "name_en": "Toyota Camry",
        "name_ar": "تويوتا كامري",
        "tech": {
            "engine": "2.5L Hybrid I4",
            "displacement_cc": 2487,
            "cylinders": 4,
            "power_hp": 301,
            "torque_nm": 221,
            "transmission": "eCVT",
            "gearbox_type": "CVT",
            "drivetrain": "FWD",
            "top_speed_kmh": 180,
            "accel_0_100": Decimal("7.4"),
            "economy_combined": Decimal("5.1"),
            "emission_standard": "Euro 6",
            "fuel_type_detail": "hybrid",
        },
        "dims": {
            "length_mm": 4885,
            "width_mm": 1840,
            "height_mm": 1455,
            "wheelbase_mm": 2825,
            "curb_weight_kg": 1620,
            "cargo_l": 524,
            "seats": 5,
            "doors": 4,
            "fuel_tank_l": Decimal("50.0"),
        },
        "tire_size": "235/45R18",
        "rim_size": "18 inch",
        "price_toman": Decimal("5500000000"),
    },
    ("Iran Khodro", "Samand"): {
        "body_style": BodyStyle.SEDAN,
        "categories": ("sedan", "economy", "family"),
        "generation": "LX",
        "doors": 4,
        "market_status": MarketStatus.DISCONTINUED,
        "country_of_origin": "Iran",
        "country_of_assembly": "Iran",
        "manufacturer": "ایران‌خودرو",
        "assembler": "ایران‌خودرو",
        "introduced_year": 2001,
        "iran_entry_year": 2001,
        "production_start_year": 2001,
        "production_end_year": 2022,
        "name_fa": "سمند",
        "name_en": "Samand",
        "name_ar": "سمند",
        "tech": {
            "engine": "1.8L XU7",
            "engine_code": "XU7JP/L3",
            "displacement_cc": 1761,
            "cylinders": 4,
            "power_hp": 100,
            "torque_nm": 153,
            "transmission": "5-speed manual",
            "gearbox_type": "MT",
            "gears": 5,
            "transmission_mode": "manual",
            "drivetrain": "FWD",
            "top_speed_kmh": 185,
            "accel_0_100": Decimal("13.0"),
            "economy_combined": Decimal("8.5"),
            "emission_standard": "Euro 2",
        },
        "dims": {
            "length_mm": 4502,
            "width_mm": 1720,
            "height_mm": 1460,
            "wheelbase_mm": 2670,
            "curb_weight_kg": 1220,
            "cargo_l": 500,
            "seats": 5,
            "doors": 4,
            "fuel_tank_l": Decimal("60.0"),
        },
        "tire_size": "185/65R15",
        "rim_size": "15 inch",
        "price_toman": Decimal("450000000"),
    },
    ("Iran Khodro", "Dena"): {
        "body_style": BodyStyle.SEDAN,
        "categories": ("sedan", "family"),
        "generation": "Plus",
        "doors": 4,
        "market_status": MarketStatus.PRODUCTION,
        "country_of_origin": "Iran",
        "country_of_assembly": "Iran",
        "manufacturer": "ایران‌خودرو",
        "assembler": "ایران‌خودرو",
        "introduced_year": 2011,
        "iran_entry_year": 2011,
        "production_start_year": 2011,
        "name_fa": "دنا",
        "name_en": "Dena",
        "name_ar": "دينا",
        "tech": {
            "engine": "1.7L EF7",
            "engine_code": "EF7",
            "displacement_cc": 1648,
            "cylinders": 4,
            "power_hp": 113,
            "torque_nm": 155,
            "transmission": "5-speed manual",
            "gearbox_type": "MT",
            "gears": 5,
            "transmission_mode": "manual",
            "drivetrain": "FWD",
            "top_speed_kmh": 190,
            "accel_0_100": Decimal("12.0"),
            "economy_combined": Decimal("7.8"),
            "emission_standard": "Euro 4",
        },
        "dims": {
            "length_mm": 4554,
            "width_mm": 1720,
            "height_mm": 1462,
            "wheelbase_mm": 2671,
            "curb_weight_kg": 1280,
            "cargo_l": 480,
            "seats": 5,
            "doors": 4,
            "fuel_tank_l": Decimal("60.0"),
        },
        "tire_size": "185/65R15",
        "rim_size": "15 inch",
        "price_toman": Decimal("780000000"),
    },
}


def get_profile(brand_name: str, model_name: str) -> dict:
    return MODEL_PROFILES.get((brand_name, model_name), {})


def apply_car_model_meta(car_model, brand_name: str, model_name: str, category_map: dict):
    profile = get_profile(brand_name, model_name)
    if not profile:
        return
    updates = {
        "name_fa": profile.get("name_fa", ""),
        "name_en": profile.get("name_en", model_name),
        "name_ar": profile.get("name_ar", ""),
        "official_name": profile.get("official_name_en")
        or profile.get("name_en")
        or model_name,
        "model_code": profile.get("model_code", ""),
        "chassis_code": profile.get("chassis_code", ""),
        "generation": profile.get("generation", ""),
        "body_style": profile.get("body_style", ""),
        "introduced_year": profile.get("introduced_year"),
        "iran_entry_year": profile.get("iran_entry_year"),
        "production_start_year": profile.get("production_start_year"),
        "production_end_year": profile.get("production_end_year"),
    }
    for key, value in updates.items():
        setattr(car_model, key, value)
    car_model.save()
    slugs = profile.get("categories") or ()
    cats = [category_map[s] for s in slugs if s in category_map]
    if cats:
        car_model.categories.set(cats)


def apply_car_identity(car, brand_name: str, model_name: str, horsepower: int, fuel_type: str):
    profile = get_profile(brand_name, model_name)
    display = f"{brand_name} {model_name}"
    car.horsepower = horsepower
    car.fuel_type = fuel_type
    car.is_published = True
    for key, value in tri_fields(
        description=(
            f"{display} — full demo catalog entry with technical, cabin, "
            f"market and service data for MyAutoHub."
        ),
        name=profile.get("name_en") or display,
        official_name=profile.get("official_name_en")
        or profile.get("name_en")
        or display,
    ).items():
        # Prefer localized names from profile when present
        setattr(car, key, value)
    if profile.get("name_fa"):
        car.name_fa = profile["name_fa"]
    if profile.get("name_en"):
        car.name_en = profile["name_en"]
    if profile.get("name_ar"):
        car.name_ar = profile["name_ar"]
    if profile.get("official_name_fa"):
        car.official_name_fa = profile["official_name_fa"]
    if profile.get("official_name_en"):
        car.official_name_en = profile["official_name_en"]
    if profile.get("official_name_ar"):
        car.official_name_ar = profile["official_name_ar"]

    car.model_code = profile.get("model_code", "")
    car.chassis_code = profile.get("chassis_code", "")
    car.generation = profile.get("generation", "")
    car.body_style = profile.get("body_style", "")
    car.doors = profile.get("doors")
    car.manufacturer = profile.get("manufacturer") or brand_name
    car.assembler = profile.get("assembler", "")
    car.importer = profile.get("importer", "")
    car.country_of_origin = profile.get("country_of_origin", "")
    car.country_of_assembly = profile.get("country_of_assembly", "")
    car.introduced_year = profile.get("introduced_year")
    car.iran_entry_year = profile.get("iran_entry_year")
    car.production_start_year = profile.get("production_start_year")
    car.production_end_year = profile.get("production_end_year")
    car.market_status = profile.get("market_status", MarketStatus.IMPORTED)
    car.save()


def seed_full_car_details(car, brand_name: str, model_name: str, category_map: dict):
    """Attach complete related specs for a demo car (idempotent overwrite)."""
    profile = get_profile(brand_name, model_name)
    tech = dict(profile.get("tech") or {})
    dims = dict(profile.get("dims") or {})
    hp = car.horsepower or tech.get("power_hp") or 150
    if not tech:
        tech = {
            "engine": f"{hp} hp engine",
            "displacement_cc": 2000,
            "cylinders": 4,
            "transmission": "Automatic",
            "gearbox_type": "AT",
            "gears": 6,
            "drivetrain": "FWD",
            "power_hp": hp,
            "top_speed_kmh": 180,
            "accel_0_100": Decimal("9.5"),
            "economy_combined": Decimal("7.5"),
            "emission_standard": "Euro 5",
        }
    if not dims:
        dims = {
            "length_mm": 4500,
            "width_mm": 1800,
            "height_mm": 1450,
            "wheelbase_mm": 2700,
            "curb_weight_kg": 1400,
            "cargo_l": 450,
            "seats": 5,
            "doors": 4,
            "fuel_tank_l": Decimal("50.0"),
        }

    TechnicalSpec.objects.update_or_create(car=car, defaults=tech)
    Dimensions.objects.update_or_create(car=car, defaults=dims)

    SuspensionSpec.objects.update_or_create(
        car=car,
        defaults={
            "front_type": "MacPherson strut",
            "front_shock": "Gas",
            "front_spring": "Coil",
            "rear_type": "Multi-link",
            "rear_shock": "Gas",
            "rear_spring": "Coil",
            "steering_system": "Rack and pinion",
            "steering_type": "Power steering",
            "steering_assist": "electric",
            "turning_radius_m": dims.get("turning_circle_m") or Decimal("11.5"),
        },
    )
    BrakeSpec.objects.update_or_create(
        car=car,
        defaults={
            "front_brake": "Ventilated disc",
            "rear_brake": "Disc",
            "front_type": "disc",
            "rear_type": "disc",
            "abs": True,
            "ebd": True,
            "ba": True,
            "esp": True,
            "tcs": True,
            "auto_hold": hp >= 200,
            "electric_parking_brake": hp >= 180,
            "aeb": hp >= 180,
            "assist_systems": "ABS, EBD, BA, ESP, TCS",
        },
    )
    tire_size = profile.get("tire_size", "215/55R17")
    rim_size = profile.get("rim_size", "17 inch")
    WheelSpec.objects.update_or_create(
        car=car,
        defaults={
            "rim_size": rim_size,
            "rim_material": "Alloy",
            "front_tire_size": tire_size,
            "rear_tire_size": tire_size,
            "spare_tire": True,
            "spare_type": "Temporary",
            "tpms": True,
            "standard_pressure": "35 psi front / 35 psi rear",
        },
    )
    CabinSpec.objects.update_or_create(
        car=car,
        defaults={
            "dashboard_material": "Soft-touch plastic",
            "seat_material": "Leather" if hp >= 200 else "Fabric",
            "upholstery": "leather" if hp >= 200 else "fabric",
            "seat_count": dims.get("seats") or 5,
            "driver_seat_adjust": "Power 8-way" if hp >= 180 else "Manual 6-way",
            "passenger_seat_adjust": "Power 6-way" if hp >= 250 else "Manual",
            "rear_seat_adjust": "40/60 split fold",
            "front_legroom_mm": 1070,
            "rear_legroom_mm": 920,
            "headroom_mm": 980,
            "armrest": True,
            "cupholders": True,
            "rear_ac_vents": True,
            "power_tailgate": hp >= 240,
            "rear_seats_fold": True,
        },
    )
    MultimediaSpec.objects.update_or_create(
        car=car,
        defaults={
            "center_display": True,
            "display_size_inch": Decimal("10.25") if hp >= 180 else Decimal("8.0"),
            "audio_system": "Premium" if hp >= 300 else "Standard",
            "speakers": 12 if hp >= 300 else 6,
            "amplifier": hp >= 250,
            "subwoofer": hp >= 300,
            "bluetooth": True,
            "usb": True,
            "aux": True,
            "wifi": hp >= 200,
            "apple_carplay": True,
            "android_auto": True,
            "navigation": hp >= 180,
            "voice_control": True,
            "phone_connectivity": "Bluetooth / USB",
            "digital_cluster": hp >= 200,
            "head_up_display": hp >= 350,
        },
    )

    Feature.objects.filter(car=car).delete()
    feature_rows = [
        (FeatureCategory.SAFETY, "abs", "ABS", "Yes"),
        (FeatureCategory.SAFETY, "esp", "ESP / Stability control", "Yes"),
        (FeatureCategory.SAFETY, "airbags", "Airbags", "6+" if hp >= 180 else "2"),
        (FeatureCategory.COMFORT, "ac", "Climate control", "Auto" if hp >= 180 else "Manual"),
        (FeatureCategory.COMFORT, "cruise", "Cruise control", "Adaptive" if hp >= 250 else "Standard"),
        (FeatureCategory.TECH, "camera", "Rear camera", "Yes"),
        (FeatureCategory.TECH, "sensors", "Parking sensors", "Front & rear" if hp >= 200 else "Rear"),
        (FeatureCategory.MULTIMEDIA, "carplay", "Apple CarPlay", "Yes"),
        (FeatureCategory.MULTIMEDIA, "android", "Android Auto", "Yes"),
        (FeatureCategory.EXTERIOR, "alloy", "Alloy wheels", rim_size),
        (FeatureCategory.CABIN, "seats", "Seat material", "Leather" if hp >= 200 else "Fabric"),
    ]
    Feature.objects.bulk_create(
        [
            Feature(
                car=car,
                category=cat,
                key=key,
                name=name,
                value=value,
                availability=FeatureAvailability.STANDARD,
            )
            for cat, key, name, value in feature_rows
        ]
    )

    MaintenanceItem.objects.filter(car=car).delete()
    MaintenanceItem.objects.bulk_create(
        [
            MaintenanceItem(
                car=car,
                title="Engine oil & filter",
                interval_km=10000,
                interval_months=12,
                description="Synthetic oil change with OEM filter.",
                estimated_cost=Decimal("3500000"),
            ),
            MaintenanceItem(
                car=car,
                title="Cabin & air filters",
                interval_km=20000,
                interval_months=24,
                description="Replace cabin and engine air filters.",
                estimated_cost=Decimal("1800000"),
            ),
            MaintenanceItem(
                car=car,
                title="Brake fluid flush",
                interval_km=40000,
                interval_months=36,
                description="DOT fluid replacement and bleed.",
                estimated_cost=Decimal("2500000"),
            ),
        ]
    )

    FluidSpec.objects.filter(car=car).delete()
    FluidSpec.objects.bulk_create(
        [
            FluidSpec(
                car=car,
                fluid_type=FluidType.ENGINE_OIL,
                specification=tech.get("engine_oil_type") or "5W-30",
                grade="API SN",
                capacity=str(tech.get("engine_oil_capacity_l") or "4.5") + " L",
                interval_km=10000,
                interval_months=12,
                estimated_cost=Decimal("3200000"),
            ),
            FluidSpec(
                car=car,
                fluid_type=FluidType.COOLANT,
                specification="Long-life coolant",
                capacity=str(tech.get("coolant_capacity_l") or "6.0") + " L",
                interval_km=60000,
                interval_months=48,
            ),
            FluidSpec(
                car=car,
                fluid_type=FluidType.BRAKE,
                specification="DOT 4",
                capacity="0.7 L",
                interval_km=40000,
                interval_months=36,
            ),
            FluidSpec(
                car=car,
                fluid_type=FluidType.TRANSMISSION,
                specification=tech.get("gearbox_type") or "ATF",
                capacity="7.0 L",
                interval_km=60000,
                interval_months=48,
            ),
        ]
    )

    TireSpec.objects.filter(car=car).delete()
    TireSpec.objects.create(
        car=car,
        position=TirePosition.ALL,
        size=tire_size,
        pressure_psi=Decimal("35.0"),
        load_index="91",
        speed_rating="V" if hp >= 200 else "H",
        rim_size=rim_size,
        rim_material="Alloy",
    )

    BatterySpec.objects.filter(car=car).delete()
    BatterySpec.objects.create(
        car=car,
        group_size="55" if hp < 300 else "70",
        voltage=Decimal("12.0"),
        cca=600 if hp < 300 else 800,
        chemistry="AGM",
        notes="Demo OEM-equivalent battery.",
    )

    ServiceScheduleItem.objects.filter(car=car).delete()
    ServiceScheduleItem.objects.bulk_create(
        [
            ServiceScheduleItem(
                car=car,
                mileage_km=10000,
                months=12,
                tasks="Oil, oil filter, inspection",
                sort_order=1,
            ),
            ServiceScheduleItem(
                car=car,
                mileage_km=20000,
                months=24,
                tasks="Oil, filters, brake inspection, tire rotation",
                sort_order=2,
            ),
            ServiceScheduleItem(
                car=car,
                mileage_km=40000,
                months=36,
                tasks="Major service: fluids, plugs, belts check",
                sort_order=3,
            ),
        ]
    )

    Part.objects.filter(car=car).delete()
    Part.objects.bulk_create(
        [
            Part(
                car=car,
                name="Cabin air filter",
                oem_number=f"OEM-{car.pk}-CABIN",
                category="Filters",
                is_consumable=True,
                interval_km=20000,
                estimated_cost=Decimal("900000"),
            ),
            Part(
                car=car,
                name="Engine oil filter",
                oem_number=f"OEM-{car.pk}-OIL",
                category="Filters",
                is_consumable=True,
                interval_km=10000,
                estimated_cost=Decimal("450000"),
            ),
            Part(
                car=car,
                name="Front brake pads",
                oem_number=f"OEM-{car.pk}-BRK",
                category="Brakes",
                is_consumable=True,
                interval_km=40000,
                estimated_cost=Decimal("4500000"),
            ),
            Part(
                car=car,
                name="Spark plugs set",
                oem_number=f"OEM-{car.pk}-PLG",
                category="Ignition",
                is_consumable=True,
                interval_km=60000,
                estimated_cost=Decimal("2800000"),
            ),
        ]
    )

    CommonFailure.objects.filter(car=car).delete()
    CommonFailure.objects.bulk_create(
        [
            CommonFailure(
                car=car,
                area=FailureArea.ENGINE,
                title="Carbon buildup on intake valves",
                severity=FailureSeverity.MEDIUM,
                likelihood=FailureLikelihood.OCCASIONAL,
                repair_cost_min=Decimal("8000000"),
                repair_cost_max=Decimal("18000000"),
                currency=CarCurrency.TOMAN,
                symptoms="Rough idle, hesitation under load.",
                notes="More common on direct-injection engines.",
            ),
            CommonFailure(
                car=car,
                area=FailureArea.SUSPENSION,
                title="Front control arm bushings wear",
                severity=FailureSeverity.LOW,
                likelihood=FailureLikelihood.COMMON,
                repair_cost_min=Decimal("5000000"),
                repair_cost_max=Decimal("12000000"),
                currency=CarCurrency.TOMAN,
                symptoms="Clunks over bumps, uneven tire wear.",
            ),
            CommonFailure(
                car=car,
                area=FailureArea.ELECTRICAL,
                title="Battery drain / parasitic draw",
                severity=FailureSeverity.MEDIUM,
                likelihood=FailureLikelihood.OCCASIONAL,
                repair_cost_min=Decimal("2000000"),
                repair_cost_max=Decimal("9000000"),
                currency=CarCurrency.TOMAN,
                symptoms="Dead battery after sitting overnight.",
            ),
        ]
    )

    price = profile.get("price_toman")
    if price is None:
        price = Decimal(hp) * Decimal("18000000")
    used = (price * Decimal("0.72")).quantize(Decimal("1")) if price else Decimal("0")
    MarketInfo.objects.update_or_create(
        car=car,
        defaults={
            "factory_price": price or None,
            "market_price_new": price or None,
            "market_price_used": used or None,
            "currency": CarCurrency.TOMAN,
            "depreciation_pct": Decimal("12.50"),
            "liquidity_score": 7 if brand_name in {"Toyota", "Hyundai", "Iran Khodro"} else 4,
            "demand_score": 8 if brand_name in {"Toyota", "Hyundai"} else 5,
            "popularity_score": 7,
            "maintenance_cost_annual": Decimal("45000000") if hp < 300 else Decimal("180000000"),
            "insurance_cost_annual": Decimal("30000000") if hp < 300 else Decimal("250000000"),
            "service_cost_avg": Decimal("8000000") if hp < 300 else Decimal("45000000"),
            "parts_price_index": 8 if brand_name == "Iran Khodro" else 5,
            "parts_availability": 9 if brand_name == "Iran Khodro" else 4,
            "mechanic_availability": 9 if brand_name == "Iran Khodro" else 5,
            "notes": "Demo Iran-market snapshot for catalog browsing.",
            "recorded_at": date(2026, 8, 1),
        },
    )

    from apps.cars.models import CarPrice

    CarPrice.objects.filter(car=car).delete()
    # CarPrice.amount is max_digits=12; keep full toman on MarketInfo.
    max_price = Decimal("9999999999.99")
    if price:
        if price <= max_price:
            price_amount = price
            used_amount = min(used, max_price)
            price_currency = CarCurrency.TOMAN
        else:
            # Rough toman→USD for overflow-safe demo price rows.
            price_amount = (price / Decimal("900000")).quantize(Decimal("1"))
            used_amount = (used / Decimal("900000")).quantize(Decimal("1"))
            price_currency = CarCurrency.USD
        CarPrice.objects.create(
            car=car,
            label="Market new (demo)",
            amount=price_amount,
            currency=price_currency,
            source="Demo seed",
            recorded_at=date(2026, 8, 1),
            year_for_price=car.year,
        )
        CarPrice.objects.create(
            car=car,
            label="Market used (demo)",
            amount=used_amount,
            currency=price_currency,
            source="Demo seed",
            recorded_at=date(2026, 8, 1),
            year_for_price=car.year,
            mileage_km=45000,
        )

    slugs = profile.get("categories") or ()
    cats = [category_map[s] for s in slugs if s in category_map]
    if cats:
        car.categories.set(cats)

    OBDCode.objects.update_or_create(
        car_model=car.model,
        code="P0300",
        defaults={
            "title": "Random/Multiple Cylinder Misfire",
            "description": "Demo OBD code for catalog browsing.",
            "severity": OBDSeverity.WARNING,
        },
    )
    OBDCode.objects.update_or_create(
        car_model=car.model,
        code="P0420",
        defaults={
            "title": "Catalyst System Efficiency Below Threshold",
            "description": "Demo catalyst efficiency code.",
            "severity": OBDSeverity.WARNING,
        },
    )
    OBDCode.objects.update_or_create(
        car_model=car.model,
        code="P0171",
        defaults={
            "title": "System Too Lean (Bank 1)",
            "description": "Demo lean condition code.",
            "severity": OBDSeverity.INFO,
        },
    )
