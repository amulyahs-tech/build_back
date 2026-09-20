from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database import get_db
from backend.app.models import EnvironmentalImpact, Transaction
from backend.app.schemas import (
    EnvironmentalImpactResponse, EnvironmentalSummaryResponse, EnvironmentalCalculateRequest
)
from backend.app.ml.environmental_calculator import calculate_environmental_impact

router = APIRouter(prefix="/api/environmental", tags=["Environmental & Circular LCA"])


@router.get("/summary", response_model=EnvironmentalSummaryResponse)
def get_environmental_summary(db: Session = Depends(get_db)):
    """Retrieve cumulative platform environmental savings: landfill tonnes, CO2e, and materials."""
    total_tonnes = db.query(func.sum(EnvironmentalImpact.estimated_weight_tonnes)).scalar() or 0.0
    total_co2 = db.query(func.sum(EnvironmentalImpact.estimated_co2_saving_kg)).scalar() or 0.0
    total_virgin = db.query(func.sum(EnvironmentalImpact.virgin_material_preserved_kg)).scalar() or 0.0
    total_trees = db.query(func.sum(EnvironmentalImpact.trees_equivalent)).scalar() or 0.0
    total_tx = db.query(Transaction).filter(Transaction.status == "completed").count()

    # Material breakdown
    breakdown_rows = db.query(
        EnvironmentalImpact.material_type,
        func.sum(EnvironmentalImpact.estimated_weight_tonnes)
    ).group_by(EnvironmentalImpact.material_type).all()

    breakdown = {row[0]: round(float(row[1] or 0.0), 2) for row in breakdown_rows}

    return {
        "total_landfill_diverted_tonnes": round(float(total_tonnes), 2),
        "total_co2_saved_kg": round(float(total_co2), 1),
        "total_virgin_material_saved_kg": round(float(total_virgin), 1),
        "total_trees_equivalent": round(float(total_trees), 1),
        "total_transactions": total_tx,
        "material_breakdown": breakdown
    }


@router.get("/calculate", response_model=EnvironmentalImpactResponse)
def calculate_arbitrary_impact_get(
    material_name: str = "Bricks",
    quantity: float = 1000.0,
    unit: str = "Pieces"
):
    """Estimate LCA environmental impact for user-entered material and quantity via GET."""
    return calculate_environmental_impact(material_name, quantity, unit)


@router.post("/calculate", response_model=EnvironmentalImpactResponse)
def calculate_arbitrary_impact_post(payload: EnvironmentalCalculateRequest):
    """Estimate LCA environmental impact for user-entered material and quantity via POST."""
    return calculate_environmental_impact(payload.material_name, payload.quantity, payload.unit)

