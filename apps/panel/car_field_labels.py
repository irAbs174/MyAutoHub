"""Translatable labels for the panel car create/edit form."""

from django.utils.translation import gettext_lazy as _

CAR_LABELS = {
    "model": _("Model"),
    "year": _("Year"),
    "trim": _("Trim"),
    "horsepower": _("Horsepower"),
    "fuel_type": _("Fuel type"),
    "name_fa": _("Name"),
    "name_en": _("Name"),
    "name_ar": _("Name"),
    "official_name_fa": _("Official name"),
    "official_name_en": _("Official name"),
    "official_name_ar": _("Official name"),
    "description_fa": _("Description"),
    "description_en": _("Description"),
    "description_ar": _("Description"),
    "model_code": _("Model code"),
    "chassis_code": _("Chassis code"),
    "generation": _("Generation"),
    "facelift": _("Facelift"),
    "body_style": _("Body style"),
    "manufacturer": _("Manufacturer"),
    "importer": _("Importer"),
    "assembler": _("Assembler"),
    "country_of_origin": _("Country of origin"),
    "country_of_assembly": _("Assembly country"),
    "introduced_year": _("Introduced year"),
    "iran_entry_year": _("Iran entry year"),
    "production_start_year": _("Production start year"),
    "production_end_year": _("Production end year"),
    "market_status": _("Market status"),
    "doors": _("Doors"),
    "categories": _("Categories"),
    "cover_image": _("Cover image"),
    "is_published": _("Published"),
}

TECHNICAL_SPEC_LABELS = {
    "engine": _("Engine"),
    "displacement_cc": _("Displacement (cc)"),
    "cylinders": _("Cylinders"),
    "transmission": _("Transmission"),
    "drivetrain": _("Drivetrain"),
    "top_speed_kmh": _("Top speed (km/h)"),
    "accel_0_100": _("Acceleration 0–100 (s)"),
    "economy_city": _("City consumption"),
    "economy_highway": _("Highway consumption"),
    "emission_standard": _("Emission standard"),
    "notes": _("Notes"),
    "engine_code": _("Engine code"),
    "engine_type": _("Engine type"),
    "cylinder_arrangement": _("Cylinder arrangement"),
    "valves": _("Valves"),
    "camshaft": _("Camshaft"),
    "aspiration": _("Aspiration"),
    "supercharged": _("Supercharged"),
    "fuel_injection": _("Fuel injection"),
    "fuel_type_detail": _("Fuel type (detail)"),
    "power_hp": _("Power (hp)"),
    "power_rpm": _("Power RPM"),
    "torque_nm": _("Torque (Nm)"),
    "torque_rpm": _("Torque RPM"),
    "compression_ratio": _("Compression ratio"),
    "engine_oil_capacity_l": _("Engine oil capacity (L)"),
    "engine_oil_type": _("Engine oil type"),
    "coolant_capacity_l": _("Coolant capacity (L)"),
    "cooling_system": _("Cooling system"),
    "gearbox_type": _("Gearbox type"),
    "gears": _("Gears"),
    "transmission_mode": _("Transmission mode"),
    "clutch_type": _("Clutch type"),
    "reverse_gears": _("Reverse gears"),
    "drive_modes": _("Drive modes"),
    "tiptronic": _("Tiptronic"),
    "paddle_shifters": _("Paddle shifters"),
    "economy_combined": _("Combined consumption"),
    "range_km": _("Range (km)"),
    "co2_g_km": _("CO₂ (g/km)"),
    "towing_capacity_kg": _("Towing capacity (kg)"),
}

DIMENSIONS_LABELS = {
    "length_mm": _("Length (mm)"),
    "width_mm": _("Width (mm)"),
    "height_mm": _("Height (mm)"),
    "wheelbase_mm": _("Wheelbase (mm)"),
    "curb_weight_kg": _("Curb weight (kg)"),
    "cargo_l": _("Cargo volume (L)"),
    "seats": _("Seats"),
    "ground_clearance_mm": _("Ground clearance (mm)"),
    "fuel_tank_l": _("Fuel tank (L)"),
    "track_front_mm": _("Front track (mm)"),
    "track_rear_mm": _("Rear track (mm)"),
    "turning_circle_m": _("Turning circle (m)"),
    "cargo_seats_folded_l": _("Cargo seats folded (L)"),
    "cabin_volume_l": _("Cabin volume (L)"),
    "gross_weight_kg": _("Gross weight (kg)"),
    "payload_kg": _("Payload (kg)"),
    "doors": _("Doors"),
}

SUSPENSION_LABELS = {
    "front_type": _("Front suspension"),
    "front_shock": _("Front shock"),
    "front_spring": _("Front spring"),
    "rear_type": _("Rear suspension"),
    "rear_shock": _("Rear shock"),
    "rear_spring": _("Rear spring"),
    "steering_system": _("Steering system"),
    "steering_type": _("Steering type"),
    "steering_assist": _("Steering assist"),
    "turning_radius_m": _("Turning radius (m)"),
    "notes": _("Notes"),
}

BRAKE_LABELS = {
    "front_brake": _("Front brake"),
    "rear_brake": _("Rear brake"),
    "front_type": _("Front brake type"),
    "rear_type": _("Rear brake type"),
    "abs": _("ABS"),
    "ebd": _("EBD"),
    "ba": _("Brake assist (BA)"),
    "esp": _("ESP"),
    "tcs": _("TCS"),
    "auto_hold": _("Auto Hold"),
    "electric_parking_brake": _("Electric parking brake"),
    "aeb": _("AEB"),
    "assist_systems": _("Assist systems"),
    "notes": _("Notes"),
}

WHEEL_LABELS = {
    "rim_size": _("Rim size"),
    "rim_material": _("Rim material"),
    "front_tire_size": _("Front tire size"),
    "rear_tire_size": _("Rear tire size"),
    "spare_tire": _("Spare tire"),
    "spare_type": _("Spare type"),
    "tpms": _("TPMS"),
    "standard_pressure": _("Standard pressure"),
    "notes": _("Notes"),
}

CABIN_LABELS = {
    "dashboard_material": _("Dashboard material"),
    "seat_material": _("Seat material"),
    "upholstery": _("Upholstery"),
    "seat_count": _("Seat count"),
    "driver_seat_adjust": _("Driver seat adjustment"),
    "passenger_seat_adjust": _("Passenger seat adjustment"),
    "rear_seat_adjust": _("Rear seat adjustment"),
    "front_legroom_mm": _("Front legroom (mm)"),
    "rear_legroom_mm": _("Rear legroom (mm)"),
    "headroom_mm": _("Headroom (mm)"),
    "armrest": _("Armrest"),
    "cupholders": _("Cup holders"),
    "rear_ac_vents": _("Rear AC vents"),
    "power_tailgate": _("Power tailgate"),
    "rear_seats_fold": _("Folding rear seats"),
    "notes": _("Notes"),
}

MULTIMEDIA_LABELS = {
    "center_display": _("Center display"),
    "display_size_inch": _("Display size (inch)"),
    "audio_system": _("Audio system"),
    "speakers": _("Speakers"),
    "amplifier": _("Amplifier"),
    "subwoofer": _("Subwoofer"),
    "bluetooth": _("Bluetooth"),
    "usb": _("USB"),
    "aux": _("AUX"),
    "wifi": _("Wi-Fi"),
    "apple_carplay": _("Apple CarPlay"),
    "android_auto": _("Android Auto"),
    "navigation": _("Navigation"),
    "mirrorlink": _("MirrorLink"),
    "voice_control": _("Voice control"),
    "phone_connectivity": _("Phone connectivity"),
    "digital_cluster": _("Digital cluster"),
    "head_up_display": _("Head-up display"),
    "notes": _("Notes"),
}

MARKET_LABELS = {
    "factory_price": _("Factory price"),
    "market_price_new": _("Market price (new)"),
    "market_price_used": _("Market price (used)"),
    "currency": _("Currency"),
    "depreciation_pct": _("Depreciation (%)"),
    "liquidity_score": _("Liquidity score"),
    "demand_score": _("Demand score"),
    "popularity_score": _("Popularity score"),
    "maintenance_cost_annual": _("Annual maintenance cost"),
    "insurance_cost_annual": _("Annual insurance cost"),
    "service_cost_avg": _("Average service cost"),
    "parts_price_index": _("Parts price index"),
    "parts_availability": _("Parts availability"),
    "mechanic_availability": _("Mechanic availability"),
    "notes": _("Notes"),
    "recorded_at": _("Recorded at"),
}

PHOTO_LABELS = {
    "image": _("Image"),
    "caption": _("Caption"),
    "sort_order": _("Sort order"),
}

FEATURE_LABELS = {
    "category": _("Category"),
    "key": _("Feature key"),
    "name": _("Feature name"),
    "value": _("Value"),
    "availability": _("Availability"),
}

MAINTENANCE_LABELS = {
    "title": _("Title"),
    "interval_km": _("Interval (km)"),
    "interval_months": _("Interval (months)"),
    "description": _("Description"),
    "estimated_cost": _("Estimated cost"),
}

FLUID_LABELS = {
    "fluid_type": _("Fluid type"),
    "specification": _("Specification"),
    "grade": _("Grade"),
    "capacity": _("Capacity"),
    "interval_km": _("Interval (km)"),
    "interval_months": _("Interval (months)"),
    "estimated_cost": _("Estimated cost"),
    "notes": _("Notes"),
}

TIRE_LABELS = {
    "position": _("Position"),
    "size": _("Size"),
    "pressure_psi": _("Pressure (psi)"),
    "load_index": _("Load index"),
    "speed_rating": _("Speed rating"),
    "rim_size": _("Rim size"),
    "rim_material": _("Rim material"),
}

BATTERY_LABELS = {
    "group_size": _("Group size"),
    "voltage": _("Voltage"),
    "cca": _("CCA"),
    "chemistry": _("Chemistry"),
    "notes": _("Notes"),
}

SERVICE_LABELS = {
    "mileage_km": _("Mileage (km)"),
    "months": _("Months"),
    "tasks": _("Tasks"),
    "sort_order": _("Sort order"),
}

PART_LABELS = {
    "name": _("Part name"),
    "oem_number": _("OEM number"),
    "category": _("Category"),
    "is_consumable": _("Consumable"),
    "interval_km": _("Interval (km)"),
    "interval_months": _("Interval (months)"),
    "estimated_cost": _("Estimated cost"),
    "notes": _("Notes"),
}

FAILURE_LABELS = {
    "area": _("Area"),
    "title": _("Title"),
    "severity": _("Severity"),
    "likelihood": _("Likelihood"),
    "repair_cost_min": _("Repair cost (min)"),
    "repair_cost_max": _("Repair cost (max)"),
    "currency": _("Currency"),
    "symptoms": _("Symptoms"),
    "notes": _("Notes"),
}

PRICE_LABELS = {
    "label": _("Label"),
    "amount": _("Amount"),
    "currency": _("Currency"),
    "source": _("Source"),
    "year_for_price": _("Year for price"),
    "mileage_km": _("Mileage (km)"),
    "notes": _("Notes"),
    "recorded_at": _("Recorded at"),
}


def apply_field_labels(form, labels):
    for name, label in labels.items():
        if name in form.fields:
            form.fields[name].label = label
