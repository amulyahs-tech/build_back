from typing import Dict, Any, Optional
import numpy as np

GRADE_THRESHOLDS = [
    (92.0, "A", "Excellent", "Like-new condition, zero to negligible micro-wear. Suitable for direct structural reuse."),
    (80.0, "B", "Good", "Light surface weathering or aesthetic blemishes. Fully sound for secondary construction."),
    (65.0, "C", "Moderate", "Noticeable cosmetic wear, chipped edges, or mortar residue. Suitable for non-load-bearing or landscaping."),
    (40.0, "D", "Poor", "Significant surface deterioration or fragmentation. Requires mechanical reprocessing or aggregate crushing."),
    (0.0, "E", "Very Poor", "Severe structural degradation, fractures, or contamination. Industrial recycling or downcycling only.")
]


def score_to_grade(score: float) -> tuple:
    """Maps a 0-100 score to Grade (A-E), condition name, and description."""
    clamped_score = max(0.0, min(100.0, score))
    for threshold, grade, name, desc in GRADE_THRESHOLDS:
        if clamped_score >= threshold:
            return grade, name, desc, clamped_score
    return "E", "Very Poor", GRADE_THRESHOLDS[-1][3], clamped_score


class QualityClassifier:
    """Multimodal Material Quality Evaluator combining visual metrics with age and damage data."""

    def __init__(self):
        self.disclaimer = (
            "DISCLAIMER: AI visual quality assessment is an advisory condition estimate based on surface characteristics "
            "and user-reported metrics. It does not replace on-site nondestructive physical, ultrasonic, or core-sample "
            "structural testing required for critical load-bearing applications."
        )

    def assess_quality(
        self,
        material_name: str,
        age_years: float = 1.0,
        damage_percentage: float = 10.0,
        original_usage: Optional[str] = "Residential Demolition",
        surface_wear: Optional[str] = "Light",
        visual_roughness: Optional[float] = None
    ) -> Dict[str, Any]:
        """Calculates 0-100 condition score and A-E grade."""
        base_score = 100.0

        # Penalize for age (diminishing penalty based on material permanence)
        age_decay_factor = 2.5
        if material_name in ["Steel / Rebar", "Concrete", "Granite", "Stones"]:
            age_decay_factor = 1.2
        elif material_name in ["Wood / Timber", "PVC Pipes"]:
            age_decay_factor = 3.5

        age_penalty = min(30.0, (age_years ** 0.8) * age_decay_factor)

        # Penalize for user-reported or detected damage percentage
        damage_penalty = min(45.0, (damage_percentage * 0.75))

        # Surface wear category modifier
        wear_penalties = {
            "None": 0.0,
            "Light": 4.0,
            "Moderate": 12.0,
            "Heavy": 24.0,
            "Severe": 38.0
        }
        surface_penalty = wear_penalties.get(surface_wear, 6.0)

        # Visual roughness/crack modifier if computed from image
        visual_penalty = 0.0
        if visual_roughness is not None:
            visual_penalty = min(15.0, visual_roughness * 10.0)

        final_score = base_score - age_penalty - damage_penalty - surface_penalty - visual_penalty

        grade, name, description, clamped_score = score_to_grade(final_score)

        # Pull safe secondary applications from reuse recommender
        from backend.app.ml.reuse_recommender import get_reuse_recommendations
        rec = get_reuse_recommendations(material_name, quality_grade=grade)

        return {
            "material_name": material_name,
            "quality_grade": grade,
            "quality_score": round(clamped_score, 1),
            "condition_name": name,
            "condition_description": description,
            "recommended_reuse": rec.get("recommended_applications", []),
            "unsuitable_uses": rec.get("unsuitable_applications", []),
            "disclaimer": self.disclaimer
        }


# Singleton instance
quality_classifier = QualityClassifier()
