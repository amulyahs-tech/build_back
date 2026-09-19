from typing import Dict, List, Any

# Construction Circular Economy Recommendations Catalog
REUSE_CATALOG: Dict[str, Dict[str, Any]] = {
    "Bricks": {
        "recyclability_tier": "Directly Reusable",
        "recyclability_rating": "High (95%)",
        "carbon_factor": 0.24,  # kg CO2e per piece
        "weight_per_unit_kg": 3.0,
        "grades": {
            "A": {
                "applications": ["Load-bearing masonry", "Exposed facade walls", "Architectural restoration", "Interior partitions"],
                "unsuitable": ["Underwater structures"],
                "processing": "Mortar chipping, gentle water wash"
            },
            "B": {
                "applications": ["Boundary walls", "Non-load-bearing partition walls", "Garden landscaping", "Paving edges"],
                "unsuitable": ["High-rise multi-story load-bearing pillars"],
                "processing": "Surface scraping, dusting"
            },
            "C": {
                "applications": ["Retaining wall fill", "Landscape planter boxes", "Sub-base flooring", "Dugout drainage"],
                "unsuitable": ["Structural walls", "Load-bearing columns"],
                "processing": "Sorting, removal of broken fragments"
            },
            "D": {
                "applications": ["Crushed brick aggregate for road base", "Permeable pathway gravel", "Lightweight concrete aggregate"],
                "unsuitable": ["All masonry walls"],
                "processing": "Mechanical jaw crushing, screening"
            },
            "E": {
                "applications": ["Landfill daily cover", "Sub-grade embankment stabilization"],
                "unsuitable": ["All construction and decorative uses"],
                "processing": "Heavy crushing and sorting"
            }
        }
    },
    "Concrete": {
        "recyclability_tier": "Reusable After Processing",
        "recyclability_rating": "High (90%)",
        "carbon_factor": 0.18,  # kg CO2e per kg
        "weight_per_unit_kg": 1000.0,
        "grades": {
            "A": {
                "applications": ["Precast structural element reuse", "Heavy modular retaining blocks", "Commercial paving slabs"],
                "unsuitable": ["Direct prestressed tension beams without ultrasonic pulse test"],
                "processing": "Rebar trim, pressure washing"
            },
            "B": {
                "applications": ["Foundation bed leveling", "Parking lot paving", "Erosion control riprap"],
                "unsuitable": ["Suspended bridge decks"],
                "processing": "Edge dressing"
            },
            "C": {
                "applications": ["Recycled Concrete Aggregate (RCA) for sub-base", "French drains", "Trench backfilling"],
                "unsuitable": ["Structural columns"],
                "processing": "Crushing to 20mm/40mm aggregate size"
            },
            "D": {
                "applications": ["Road base stabilization", "Pipe bedding layer", "Embankment core fill"],
                "unsuitable": ["Direct structural use"],
                "processing": "Heavy crushing, magnetic metal removal"
            },
            "E": {
                "applications": ["Mass bulk ground fill", "Quarry site remediation"],
                "unsuitable": ["Any building components"],
                "processing": "Bulk rubble sorting"
            }
        }
    },
    "Cement Blocks": {
        "recyclability_tier": "Directly Reusable",
        "recyclability_rating": "Moderate (85%)",
        "carbon_factor": 0.35,
        "weight_per_unit_kg": 18.0,
        "grades": {
            "A": ["Exterior compound walls", "Warehouse partitions", "Foundation footing blocks"],
            "B": ["Low-height garden walls", "Shed walling", "Duct encasements"],
            "C": ["Trench ballast", "Sub-pavement base"],
            "D": ["Crushed concrete block aggregate"],
            "E": ["Land stabilization fill"]
        }
    },
    "Steel / Rebar": {
        "recyclability_tier": "Recyclable / High Value",
        "recyclability_rating": "Infinite (100%)",
        "carbon_factor": 1.85,  # kg CO2e per kg of steel avoided
        "weight_per_unit_kg": 1.0,
        "grades": {
            "A": {
                "applications": ["TMT Rebar structural reinforcement", "Slab mesh", "Roof truss fabrication", "Column ties"],
                "unsuitable": ["Nuclear or seismic zone 5 critical beams without tensile testing"],
                "processing": "Wire brush rust removal, re-straightening"
            },
            "B": {
                "applications": ["Non-critical lintels", "Staircase railings", "Window grilles", "Perimeter security fencing"],
                "unsuitable": ["Heavy crane gantry beams"],
                "processing": "Surface de-rusting, anti-corrosive primer coating"
            },
            "C": {
                "applications": ["Temporary scaffolding ties", "Formwork bracing", "Septic tank cover reinforcement"],
                "unsuitable": ["Main structural beams"],
                "processing": "Cutting pitted ends"
            },
            "D": {
                "applications": ["Direct induction furnace remelting", "Recycled steel billet feedstock"],
                "unsuitable": ["Direct structural building usage"],
                "processing": "Shearing and scrap baling"
            },
            "E": {
                "applications": ["Industrial scrap recycling"],
                "unsuitable": ["Direct building use"],
                "processing": "Foundry melting"
            }
        }
    },
    "Wood / Timber": {
        "recyclability_tier": "Directly Reusable",
        "recyclability_rating": "High (90%)",
        "carbon_factor": 0.45,
        "weight_per_unit_kg": 12.0,
        "grades": {
            "A": {
                "applications": ["Architectural roof rafters", "Furniture making", "Hardwood flooring planks", "Exposed ceiling beams"],
                "unsuitable": ["Direct soil contact without pressure treatment"],
                "processing": "De-nailing, light planing, sealant coat"
            },
            "B": {
                "applications": ["Concrete formwork shuttering", "Door/window framing", "Shelving and partition studs"],
                "unsuitable": ["Heavy load timber bridges"],
                "processing": "De-nailing, sanding"
            },
            "C": {
                "applications": ["Packaging crates", "Site barricading fencing", "Pallet construction"],
                "unsuitable": ["Permanent structural frames"],
                "processing": "Trimming damaged ends"
            },
            "D": {
                "applications": ["Engineered particle board chips", "Wood pulp manufacturing", "Bio-char production"],
                "unsuitable": ["Building structures"],
                "processing": "Wood chipping, metal separation"
            },
            "E": {
                "applications": ["Biomass boiler fuel", "Compost carbon bulking"],
                "unsuitable": ["Construction"],
                "processing": "Shredding"
            }
        }
    },
    "Tiles": {
        "recyclability_tier": "Directly Reusable",
        "recyclability_rating": "Moderate (80%)",
        "carbon_factor": 0.55,
        "weight_per_unit_kg": 2.5,
        "grades": {
            "A": ["Full floor relaying", "Bathroom wall tiling", "Accent kitchen backsplashes"],
            "B": ["Utility room flooring", "Balcony tiling", "Roof terrace insulation tile layer"],
            "C": ["Mosaic tile art / Broken tile terrace waterproofing (China Mosaic)", "Garden pathway pavers"],
            "D": ["Sub-surface drainage bedding", "Crushed tile sand substitute"],
            "E": ["Masonry mortar additive after pulverization"]
        }
    },
    "Glass": {
        "recyclability_tier": "Recyclable",
        "recyclability_rating": "Infinite (100%)",
        "carbon_factor": 0.85,
        "weight_per_unit_kg": 5.0,
        "grades": {
            "A": ["Greenhouse panels", "Interior glass partition screens", "Window glazing replacement"],
            "B": ["Secondary skylights", "Cold-frame gardening covers", "Decorative frosted panels"],
            "C": ["Decorative terrazzo flooring chips", "Reflective mosaic craft"],
            "D": ["Cullet for glass container manufacturing", "Glass foam insulation manufacture"],
            "E": ["Glass sand substitute for concrete paving blocks"]
        }
    },
    "PVC Pipes": {
        "recyclability_tier": "Directly Reusable",
        "recyclability_rating": "High (90%)",
        "carbon_factor": 1.45,
        "weight_per_unit_kg": 2.0,
        "grades": {
            "A": ["Rainwater harvesting downspouts", "Underground drainage lines", "Electrical wiring conduit ducts"],
            "B": ["Agricultural drip line manifolds", "French drain perforated pipes", "Temporary storm lines"],
            "C": ["Landscape edging and plant protectors", "Cable management casing"],
            "D": ["Plastic mechanical shredding & regranulation into recycled conduit pipes"],
            "E": ["Industrial polymer reprocessing"]
        }
    },
    "Metal Pipes": {
        "recyclability_tier": "Directly Reusable",
        "recyclability_rating": "High (95%)",
        "carbon_factor": 1.65,
        "weight_per_unit_kg": 6.0,
        "grades": {
            "A": ["Plumbing distribution lines", "Structural canopy pillars", "Handrails and guard rails"],
            "B": ["Scaffolding standards", "Temporary water supply lines", "Gate posts"],
            "C": ["Signage posts", "Warehouse shelving frames"],
            "D": ["Foundry scrap for pipe extrusion"],
            "E": ["Metal recycling"]
        }
    },
    "Granite": {
        "recyclability_tier": "Directly Reusable",
        "recyclability_rating": "High (95%)",
        "carbon_factor": 0.60,
        "weight_per_unit_kg": 35.0,
        "grades": {
            "A": ["Kitchen countertops", "Staircase treads", "Premium exterior cladding"],
            "B": ["Window sills", "Garden step stones", "Compound wall coping"],
            "C": ["Cobblestone driveway paving", "Terrace skirting"],
            "D": ["Crushed decorative stone chips for landscaping"],
            "E": ["Heavy road embankment aggregate"]
        }
    },
    "Marble": {
        "recyclability_tier": "Directly Reusable",
        "recyclability_rating": "High (90%)",
        "carbon_factor": 0.50,
        "weight_per_unit_kg": 30.0,
        "grades": {
            "A": ["Living area floor relaying", "Fireplace surrounds", "Decorative table tops"],
            "B": ["Bathroom vanity tops", "Lobby wall tiles", "Threshold sills"],
            "C": ["Broken marble mosaic flooring", "Terrazzo matrix aggregate"],
            "D": ["Micronized calcium carbonate filler for plaster"],
            "E": ["Soil neutralization lime substitute"]
        }
    }
}

# Generic fallback for uncataloged materials
DEFAULT_CATALOG = {
    "recyclability_tier": "Reusable After Processing",
    "recyclability_rating": "Moderate (75%)",
    "carbon_factor": 0.40,
    "weight_per_unit_kg": 5.0,
    "grades": {
        "A": {
            "applications": ["Direct reuse in non-critical architectural features", "Site boundary protection", "Workshop fixtures"],
            "unsuitable": ["Primary load-bearing components"],
            "processing": "Cleaning, visual inspection"
        },
        "B": {
            "applications": ["Non-structural construction", "Temporary site facilities", "Pavement leveling"],
            "unsuitable": ["Structural elements"],
            "processing": "Sorting, trimming"
        },
        "C": {
            "applications": ["Backfill and drainage support", "Sub-grade road compaction"],
            "unsuitable": ["Exposed finishes"],
            "processing": "Crushing, sieving"
        },
        "D": {
            "applications": ["Industrial recycling feedstock"],
            "unsuitable": ["Any building reuse"],
            "processing": "Industrial sorting"
        },
        "E": {
            "applications": ["Inert landfill stabilization"],
            "unsuitable": ["All applications"],
            "processing": "Bulk handling"
        }
    }
}


def get_reuse_recommendations(material_name: str, quality_grade: str = "B") -> Dict[str, Any]:
    """Retrieves safe secondary applications, structural warnings, and circularity metrics."""
    grade = quality_grade.upper() if quality_grade in ["A", "B", "C", "D", "E"] else "B"

    info = REUSE_CATALOG.get(material_name, DEFAULT_CATALOG)
    tier = info.get("recyclability_tier", "Directly Reusable")
    grades_info = info.get("grades", DEFAULT_CATALOG["grades"])

    grade_data = grades_info.get(grade, grades_info.get("B", {}))

    if isinstance(grade_data, list):
        recommended = grade_data
        unsuitable = ["Primary seismic structural members", "High-stress load-bearing columns"]
        processing = "Cleaning and physical inspection"
    else:
        recommended = grade_data.get("applications", [])
        unsuitable = grade_data.get("unsuitable", ["Load-bearing structural columns without certification"])
        processing = grade_data.get("processing", "Cleaning and sorting")

    return {
        "material_name": material_name,
        "quality_grade": grade,
        "recyclability_tier": tier,
        "recyclability_rating": info.get("recyclability_rating", "Moderate"),
        "recommended_applications": recommended,
        "unsuitable_applications": unsuitable,
        "required_processing": processing,
        "carbon_factor": info.get("carbon_factor", 0.30),
        "weight_per_unit_kg": info.get("weight_per_unit_kg", 5.0),
        "safety_disclaimer": "AI recommendations are guidelines for circular material reuse. Verify structural integrity with a qualified civil engineer for structural applications."
    }
