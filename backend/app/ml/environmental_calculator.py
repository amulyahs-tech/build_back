from typing import Dict, Any, Optional

# Embodied Carbon & Density Factors (derived from ICE Bath Inventory of Carbon & Energy and EPD database)
MATERIAL_ENVIRONMENTAL_FACTORS = {
    "Bricks": {"weight_per_unit_kg": 3.0, "embodied_carbon_per_kg": 0.24, "virgin_ratio": 1.0},
    "Concrete": {"weight_per_unit_kg": 1000.0, "embodied_carbon_per_kg": 0.18, "virgin_ratio": 1.0},
    "Cement Blocks": {"weight_per_unit_kg": 18.0, "embodied_carbon_per_kg": 0.32, "virgin_ratio": 1.0},
    "Steel / Rebar": {"weight_per_unit_kg": 1.0, "embodied_carbon_per_kg": 1.85, "virgin_ratio": 1.0},
    "Wood / Timber": {"weight_per_unit_kg": 20.0, "embodied_carbon_per_kg": 0.45, "virgin_ratio": 1.0},
    "Tiles": {"weight_per_unit_kg": 2.5, "embodied_carbon_per_kg": 0.65, "virgin_ratio": 1.0},
    "Glass": {"weight_per_unit_kg": 5.0, "embodied_carbon_per_kg": 0.85, "virgin_ratio": 1.0},
    "PVC Pipes": {"weight_per_unit_kg": 2.2, "embodied_carbon_per_kg": 1.95, "virgin_ratio": 1.0},
    "Metal Pipes": {"weight_per_unit_kg": 6.5, "embodied_carbon_per_kg": 1.70, "virgin_ratio": 1.0},
    "Doors": {"weight_per_unit_kg": 35.0, "embodied_carbon_per_kg": 0.50, "virgin_ratio": 1.0},
    "Windows": {"weight_per_unit_kg": 25.0, "embodied_carbon_per_kg": 0.75, "virgin_ratio": 1.0},
    "Granite": {"weight_per_unit_kg": 35.0, "embodied_carbon_per_kg": 0.60, "virgin_ratio": 1.0},
    "Marble": {"weight_per_unit_kg": 30.0, "embodied_carbon_per_kg": 0.55, "virgin_ratio": 1.0},
    "Stones": {"weight_per_unit_kg": 1000.0, "embodied_carbon_per_kg": 0.08, "virgin_ratio": 1.0},
    "Sand": {"weight_per_unit_kg": 1000.0, "embodied_carbon_per_kg": 0.05, "virgin_ratio": 1.0},
    "Roofing Materials": {"weight_per_unit_kg": 12.0, "embodied_carbon_per_kg": 0.90, "virgin_ratio": 1.0},
    "Ceramic Materials": {"weight_per_unit_kg": 3.0, "embodied_carbon_per_kg": 0.60, "virgin_ratio": 1.0},
    "Mixed Construction Waste": {"weight_per_unit_kg": 1000.0, "embodied_carbon_per_kg": 0.12, "virgin_ratio": 1.0},
    "Other / Debris": {"weight_per_unit_kg": 1000.0, "embodied_carbon_per_kg": 0.10, "virgin_ratio": 1.0}
}


def calculate_environmental_impact(
    material_name: str,
    quantity: float,
    unit: str = "Pieces"
) -> Dict[str, Any]:
    """Calculates landfill diversion in tonnes, avoided carbon in kg CO2e, and tree equivalents."""
    factors = MATERIAL_ENVIRONMENTAL_FACTORS.get(
        material_name,
        {"weight_per_unit_kg": 5.0, "embodied_carbon_per_kg": 0.35, "virgin_ratio": 1.0}
    )

    unit_lower = unit.lower()
    if "tonne" in unit_lower or "ton" in unit_lower:
        total_weight_kg = quantity * 1000.0
    elif "kg" in unit_lower:
        total_weight_kg = quantity
    else:
        total_weight_kg = quantity * factors["weight_per_unit_kg"]

    diverted_tonnes = round(total_weight_kg / 1000.0, 3)

    # Avoided carbon emissions = weight * avoided virgin embodied carbon factor
    avoided_co2_kg = round(total_weight_kg * factors["embodied_carbon_per_kg"], 1)

    # Virgin raw material preserved (aggregates, raw ore, limestone, virgin wood)
    virgin_preserved_kg = round(total_weight_kg * factors["virgin_ratio"], 1)

    # Equivalent trees planted: 1 mature tree absorbs ~22 kg CO2e per year
    trees_equivalent = round(avoided_co2_kg / 22.0, 1)

    return {
        "material_type": material_name,
        "quantity": quantity,
        "unit": unit,
        "estimated_weight_tonnes": float(diverted_tonnes),
        "estimated_co2_saving_kg": float(avoided_co2_kg),
        "virgin_material_preserved_kg": float(virgin_preserved_kg),
        "trees_equivalent": float(trees_equivalent),
        "disclaimer": (
            "Environmental calculations are advisory estimates based on published construction lifecycle embodied carbon "
            "coefficients (Inventory of Carbon & Energy / EPDs) and assume 80% virgin material substitution efficiency."
        )
    }
