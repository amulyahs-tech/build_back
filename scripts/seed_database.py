import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import logging
from backend.app.database import SessionLocal, engine, Base
from backend.app.models import (
    User, Material, Listing, PurchaseRequest, Transaction, EnvironmentalImpact, ModelFeedback
)
from backend.app.utils.security import get_password_hash

logger = logging.getLogger(__name__)

# Sample realistic material image paths (using standard curated web/placeholder images or clean SVG fallbacks)
MATERIAL_SEEDS = [
    {"name": "Reclaimed Red Bricks", "category": "Masonry", "reusability_tier": "Directly Reusable", "recyclability": "High", "carbon_factor": 0.24, "waste_factor": 0.003},
    {"name": "Fe-500 TMT Steel Rebar", "category": "Metals & Structural", "reusability_tier": "Directly Reusable", "recyclability": "Infinite", "carbon_factor": 1.85, "waste_factor": 0.001},
    {"name": "Recycled Coarse Concrete Aggregates", "category": "Aggregates & Masonry", "reusability_tier": "Reusable After Processing", "recyclability": "High", "carbon_factor": 0.18, "waste_factor": 1.0},
    {"name": "Reclaimed Teak Wood Doors & Panels", "category": "Joinery & Fixtures", "reusability_tier": "Directly Reusable", "recyclability": "High", "carbon_factor": 0.45, "waste_factor": 0.035},
    {"name": "Vitrified Ceramic Floor Tiles", "category": "Finishing & Ceramics", "reusability_tier": "Directly Reusable", "recyclability": "Moderate", "carbon_factor": 0.55, "waste_factor": 0.0025},
    {"name": "Heavy-Duty Rigid PVC Pipes", "category": "Plumbing & Conduits", "reusability_tier": "Directly Reusable", "recyclability": "High", "carbon_factor": 1.45, "waste_factor": 0.002},
    {"name": "Black Galaxy Polished Granite Slabs", "category": "Finishing & Flooring", "reusability_tier": "Directly Reusable", "recyclability": "High", "carbon_factor": 0.60, "waste_factor": 0.035},
    {"name": "White Makrana Marble Tiles", "category": "Finishing & Flooring", "reusability_tier": "Directly Reusable", "recyclability": "High", "carbon_factor": 0.50, "waste_factor": 0.030},
    {"name": "GI Galvanized Scaffolding Pipes", "category": "Plumbing & Structural", "reusability_tier": "Directly Reusable", "recyclability": "Infinite", "carbon_factor": 1.65, "waste_factor": 0.0065},
    {"name": "Autoclaved Aerated AAC Concrete Blocks", "category": "Masonry", "reusability_tier": "Directly Reusable", "recyclability": "Moderate", "carbon_factor": 0.35, "waste_factor": 0.015},
    {"name": "Tempered Architectural Window Glass", "category": "Glazing & Openings", "reusability_tier": "Recyclable", "recyclability": "Infinite", "carbon_factor": 0.85, "waste_factor": 0.005},
    {"name": "Mangalore Clay Terracotta Roof Tiles", "category": "Exterior & Roofing", "reusability_tier": "Directly Reusable", "recyclability": "High", "carbon_factor": 0.30, "waste_factor": 0.002},
    {"name": "Washed Coarse River Sand", "category": "Aggregates", "reusability_tier": "Directly Reusable", "recyclability": "High", "carbon_factor": 0.05, "waste_factor": 1.0},
    {"name": "Granite Cobblestones & Paving Stones", "category": "Aggregates & Masonry", "reusability_tier": "Directly Reusable", "recyclability": "High", "carbon_factor": 0.08, "waste_factor": 0.008},
    {"name": "Antique Sal Wood Structural Rafters", "category": "Lumber & Carpentry", "reusability_tier": "Directly Reusable", "recyclability": "High", "carbon_factor": 0.45, "waste_factor": 0.025},
    {"name": "UPVC Double-Glazed Soundproof Windows", "category": "Joinery & Fixtures", "reusability_tier": "Directly Reusable", "recyclability": "High", "carbon_factor": 1.20, "waste_factor": 0.025},
    {"name": "Heavy Duty Copper Busbars & Wiring", "category": "Electrical & Systems", "reusability_tier": "Recyclable / High Value", "recyclability": "Infinite", "carbon_factor": 2.80, "waste_factor": 0.001},
    {"name": "Heavy Interlocking Concrete Pavers", "category": "Masonry", "reusability_tier": "Directly Reusable", "recyclability": "High", "carbon_factor": 0.20, "waste_factor": 0.004},
    {"name": "Structural Hollow Steel Sections", "category": "Metals & Structural", "reusability_tier": "Directly Reusable", "recyclability": "Infinite", "carbon_factor": 1.85, "waste_factor": 0.012},
    {"name": "Sorted Mixed Demolition Rubble", "category": "Unsorted Rubble", "reusability_tier": "Downcycling Only", "recyclability": "Moderate", "carbon_factor": 0.10, "waste_factor": 1.0}
]

LISTINGS_DATA = [
    {
        "material_name": "Reclaimed Red Bricks", "category": "Masonry",
        "image_url": "https://images.unsplash.com/photo-1590069261209-f8e9b8642343?w=800&auto=format&fit=crop&q=60",
        "ai_confidence": 0.962, "quality_grade": "A", "quality_score": 94.0,
        "quantity": 3500.0, "unit": "Pieces", "age_years": 1.5, "damage_percentage": 4.0,
        "price": 21000.0, "ai_estimated_price": 22500.0, "city": "Bangalore", "state": "Karnataka",
        "original_usage": "Low-rise residential facade", "availability": "Immediate Pickup", "status": "active"
    },
    {
        "material_name": "Fe-500 TMT Steel Rebar", "category": "Metals & Structural",
        "image_url": "https://images.unsplash.com/photo-1535813547-99c456a41d4a?w=800&auto=format&fit=crop&q=60",
        "ai_confidence": 0.948, "quality_grade": "A", "quality_score": 92.5,
        "quantity": 1200.0, "unit": "Kg", "age_years": 0.8, "damage_percentage": 2.0,
        "price": 48000.0, "ai_estimated_price": 49200.0, "city": "Mumbai", "state": "Maharashtra",
        "original_usage": "Metro viaduct surplus cutoffs", "availability": "Site Delivery Available", "status": "active"
    },
    {
        "material_name": "Recycled Coarse Concrete Aggregates", "category": "Aggregates & Masonry",
        "image_url": "https://images.unsplash.com/photo-1578885136359-16c8bd4d3a8e?w=800&auto=format&fit=crop&q=60",
        "ai_confidence": 0.915, "quality_grade": "B", "quality_score": 83.0,
        "quantity": 25.0, "unit": "Tonnes", "age_years": 2.0, "damage_percentage": 10.0,
        "price": 35000.0, "ai_estimated_price": 37500.0, "city": "Bangalore", "state": "Karnataka",
        "original_usage": "Demolished airport runway concrete", "availability": "Immediate Pickup", "status": "active"
    },
    {
        "material_name": "Reclaimed Teak Wood Doors & Panels", "category": "Joinery & Fixtures",
        "image_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&auto=format&fit=crop&q=60",
        "ai_confidence": 0.932, "quality_grade": "A", "quality_score": 91.0,
        "quantity": 8.0, "unit": "Pieces", "age_years": 4.0, "damage_percentage": 5.0,
        "price": 18500.0, "ai_estimated_price": 19800.0, "city": "Mysore", "state": "Karnataka",
        "original_usage": "Colonial bungalow salvage", "availability": "Immediate Pickup", "status": "active"
    },
    {
        "material_name": "Vitrified Ceramic Floor Tiles", "category": "Finishing & Ceramics",
        "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&auto=format&fit=crop&q=60",
        "ai_confidence": 0.954, "quality_grade": "A", "quality_score": 95.0,
        "quantity": 450.0, "unit": "Sq.Ft", "age_years": 0.5, "damage_percentage": 1.0,
        "price": 12500.0, "ai_estimated_price": 13000.0, "city": "Hyderabad", "state": "Telangana",
        "original_usage": "Commercial IT park surplus crates", "availability": "Immediate Pickup", "status": "active"
    },
    {
        "material_name": "Heavy-Duty Rigid PVC Pipes", "category": "Plumbing & Conduits",
        "image_url": "https://images.unsplash.com/photo-1541888946425-d0fbb186c5f8?w=800&auto=format&fit=crop&q=60",
        "ai_confidence": 0.892, "quality_grade": "B", "quality_score": 85.0,
        "quantity": 180.0, "unit": "Meters", "age_years": 1.2, "damage_percentage": 8.0,
        "price": 11500.0, "ai_estimated_price": 12200.0, "city": "Delhi", "state": "Delhi",
        "original_usage": "Subdivision drainage project surplus", "availability": "Immediate Pickup", "status": "active"
    },
    {
        "material_name": "Black Galaxy Polished Granite Slabs", "category": "Finishing & Flooring",
        "image_url": "https://images.unsplash.com/photo-1590402494682-cd3fb53b1f70?w=800&auto=format&fit=crop&q=60",
        "ai_confidence": 0.965, "quality_grade": "A", "quality_score": 93.0,
        "quantity": 220.0, "unit": "Sq.Ft", "age_years": 1.0, "damage_percentage": 3.0,
        "price": 16000.0, "ai_estimated_price": 16800.0, "city": "Bangalore", "state": "Karnataka",
        "original_usage": "Villa kitchen renovation offcuts", "availability": "Immediate Pickup", "status": "active"
    },
    {
        "material_name": "White Makrana Marble Tiles", "category": "Finishing & Flooring",
        "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&auto=format&fit=crop&q=60",
        "ai_confidence": 0.923, "quality_grade": "B", "quality_score": 82.0,
        "quantity": 300.0, "unit": "Sq.Ft", "age_years": 3.0, "damage_percentage": 8.0,
        "price": 18000.0, "ai_estimated_price": 19500.0, "city": "Pune", "state": "Maharashtra",
        "original_usage": "Hotel lobby renovation", "availability": "Immediate Pickup", "status": "active"
    },
    {
        "material_name": "GI Galvanized Scaffolding Pipes", "category": "Plumbing & Structural",
        "image_url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800&auto=format&fit=crop&q=60",
        "ai_confidence": 0.912, "quality_grade": "B", "quality_score": 84.5,
        "quantity": 120.0, "unit": "Meters", "age_years": 2.5, "damage_percentage": 7.0,
        "price": 24000.0, "ai_estimated_price": 25200.0, "city": "Mumbai", "state": "Maharashtra",
        "original_usage": "High-rise construction staging", "availability": "Immediate Pickup", "status": "active"
    },
    {
        "material_name": "Autoclaved Aerated AAC Concrete Blocks", "category": "Masonry",
        "image_url": "https://images.unsplash.com/photo-1590069261209-f8e9b8642343?w=800&auto=format&fit=crop&q=60",
        "ai_confidence": 0.941, "quality_grade": "A", "quality_score": 92.0,
        "quantity": 600.0, "unit": "Pieces", "age_years": 0.6, "damage_percentage": 4.0,
        "price": 13500.0, "ai_estimated_price": 14400.0, "city": "Hyderabad", "state": "Telangana",
        "original_usage": "Apartment partition surplus", "availability": "Immediate Pickup", "status": "active"
    },
    {
        "material_name": "Tempered Architectural Window Glass", "category": "Glazing & Openings",
        "image_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&auto=format&fit=crop&q=60",
        "ai_confidence": 0.887, "quality_grade": "B", "quality_score": 86.0,
        "quantity": 150.0, "unit": "Sq.Ft", "age_years": 2.0, "damage_percentage": 6.0,
        "price": 7500.0, "ai_estimated_price": 8200.0, "city": "Delhi", "state": "Delhi",
        "original_usage": "Corporate office curtain wall retrofit", "availability": "Immediate Pickup", "status": "active"
    },
    {
        "material_name": "Mangalore Clay Terracotta Roof Tiles", "category": "Exterior & Roofing",
        "image_url": "https://images.unsplash.com/photo-1590069261209-f8e9b8642343?w=800&auto=format&fit=crop&q=60",
        "ai_confidence": 0.938, "quality_grade": "B", "quality_score": 81.0,
        "quantity": 1200.0, "unit": "Pieces", "age_years": 5.0, "damage_percentage": 10.0,
        "price": 11000.0, "ai_estimated_price": 11800.0, "city": "Mysore", "state": "Karnataka",
        "original_usage": "Heritage farmhouse deconstruction", "availability": "Immediate Pickup", "status": "active"
    }
]


def seed_database(db):
    """Populates users, materials, listings, transactions, and environmental impact data."""
    Base.metadata.create_all(bind=engine)
    # 1. Check or create users
    admin_email = os.getenv("ADMIN_EMAIL", "admin@rebuildai.com")
    admin_pass = os.getenv("ADMIN_PASSWORD", "Admin@1234")
    seller_email = os.getenv("SELLER_EMAIL", "seller@demolitioncorp.com")
    seller_pass = os.getenv("SELLER_PASSWORD", "Seller@1234")
    buyer_email = os.getenv("BUYER_EMAIL", "buyer@greenbuild.in")
    buyer_pass = os.getenv("BUYER_PASSWORD", "Buyer@1234")

    admin = db.query(User).filter(User.email == admin_email).first()
    if not admin:
        admin = User(
            name="Admin Coordinator",
            email=admin_email,
            phone="+91 9000000001",
            password_hash=get_password_hash(admin_pass),
            user_type="ADMIN",
            city="Bangalore",
            state="Karnataka",
            pincode="560001"
        )
        db.add(admin)

    seller = db.query(User).filter(User.email == seller_email).first()
    if not seller:
        seller = User(
            name="Apex Demolition & Salvage Corp",
            email=seller_email,
            phone="+91 9880012345",
            password_hash=get_password_hash(seller_pass),
            user_type="SELLER",
            city="Bangalore",
            state="Karnataka",
            pincode="560025"
        )
        db.add(seller)

    buyer = db.query(User).filter(User.email == buyer_email).first()
    if not buyer:
        buyer = User(
            name="GreenBuild Sustainable Contractors",
            email=buyer_email,
            phone="+91 9845098765",
            password_hash=get_password_hash(buyer_pass),
            user_type="BUYER",
            city="Bangalore",
            state="Karnataka",
            pincode="560034"
        )
        db.add(buyer)

    db.commit()
    db.refresh(seller)
    db.refresh(buyer)

    # 2. Materials catalog
    for mat in MATERIAL_SEEDS:
        if not db.query(Material).filter(Material.name == mat["name"]).first():
            db.add(Material(**mat))
    db.commit()

    # 3. Sample Listings
    if db.query(Listing).count() == 0:
        for item in LISTINGS_DATA:
            listing = Listing(
                seller_id=seller.id,
                material_name=item["material_name"],
                category=item["category"],
                image_url=item["image_url"],
                ai_confidence=item["ai_confidence"],
                quality_grade=item["quality_grade"],
                quality_score=item["quality_score"],
                quantity=item["quantity"],
                unit=item["unit"],
                age_years=item["age_years"],
                damage_percentage=item["damage_percentage"],
                price=item["price"],
                ai_estimated_price=item["ai_estimated_price"],
                city=item["city"],
                state=item["state"],
                original_usage=item["original_usage"],
                availability=item["availability"],
                status=item["status"]
            )
            db.add(listing)
        db.commit()

        # 4. Seed completed transactions & verified LCA impact
        sample_listings = db.query(Listing).limit(3).all()
        for idx, listing in enumerate(sample_listings):
            tx = Transaction(
                listing_id=listing.id,
                buyer_id=buyer.id,
                seller_id=seller.id,
                quantity=round(listing.quantity * 0.5, 1),
                price=round(listing.price * 0.5, 0),
                status="completed"
            )
            db.add(tx)
            db.flush()

            # Environmental Impact
            from backend.app.ml.environmental_calculator import calculate_environmental_impact
            calc = calculate_environmental_impact(listing.material_name, tx.quantity, listing.unit)
            impact = EnvironmentalImpact(
                transaction_id=tx.id,
                material_type=listing.material_name,
                quantity=tx.quantity,
                estimated_weight_tonnes=calc["estimated_weight_tonnes"],
                estimated_co2_saving_kg=calc["estimated_co2_saving_kg"],
                virgin_material_preserved_kg=calc["virgin_material_preserved_kg"],
                trees_equivalent=calc["trees_equivalent"]
            )
            db.add(impact)

        db.commit()
        logger.info("Seeded initial database successfully.")


def seed_if_empty(db):
    """Runs seeding only if database is uninitialized."""
    if db.query(User).count() == 0:
        seed_database(db)


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_database(db)
        print("Database seed completed successfully.")
    finally:
        db.close()
