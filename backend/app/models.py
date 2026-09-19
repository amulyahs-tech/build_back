import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from backend.app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(180), unique=True, index=True, nullable=False)
    phone = Column(String(30), nullable=True)
    password_hash = Column(String(255), nullable=False)
    user_type = Column(String(30), default="BOTH")  # SELLER, BUYER, BOTH, ADMIN
    city = Column(String(100), default="Bangalore")
    state = Column(String(100), default="Karnataka")
    pincode = Column(String(20), default="560001")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    listings = relationship("Listing", back_populates="seller", foreign_keys="Listing.seller_id")
    purchase_requests = relationship("PurchaseRequest", back_populates="buyer")
    favorites = relationship("Favorite", back_populates="user")
    feedbacks = relationship("ModelFeedback", back_populates="user")


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(80), nullable=False)
    description = Column(Text, nullable=True)
    reusability_tier = Column(String(50), default="Directly Reusable")  # Directly Reusable, Reusable After Processing, Recyclable, Downcycling Only
    recyclability = Column(String(50), default="High")
    carbon_factor = Column(Float, default=0.25)  # kg CO2e per kg of material
    waste_factor = Column(Float, default=1.0)  # conversion factor to metric tonnes
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    material_name = Column(String(120), index=True, nullable=False)
    category = Column(String(80), index=True, nullable=False)
    image_url = Column(String(500), nullable=False)
    ai_confidence = Column(Float, default=0.0)
    quality_grade = Column(String(5), default="B")  # A, B, C, D, E
    quality_score = Column(Float, default=80.0)  # 0 to 100
    quantity = Column(Float, nullable=False)
    unit = Column(String(30), default="Pieces")  # Pieces, Tonnes, Sq.Ft, Meters, Kg
    age_years = Column(Float, default=1.0)
    damage_percentage = Column(Float, default=10.0)
    price = Column(Float, nullable=False)  # Seller's listed price in INR
    ai_estimated_price = Column(Float, nullable=True)
    city = Column(String(100), index=True, default="Bangalore")
    state = Column(String(100), default="Karnataka")
    original_usage = Column(String(200), default="Residential Construction")
    availability = Column(String(50), default="Immediate Pickup")
    status = Column(String(30), default="active")  # active, pending_review, sold, flagged
    embedding_json = Column(Text, nullable=True)  # JSON-encoded 1280-dim feature vector
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    seller = relationship("User", back_populates="listings", foreign_keys=[seller_id])
    purchase_requests = relationship("PurchaseRequest", back_populates="listing", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="listing", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="listing")


class PurchaseRequest(Base):
    __tablename__ = "purchase_requests"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    proposed_price = Column(Float, nullable=False)
    message = Column(Text, nullable=True)
    preferred_pickup_date = Column(String(50), nullable=True)
    status = Column(String(30), default="pending")  # pending, accepted, rejected, completed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    listing = relationship("Listing", back_populates="purchase_requests")
    buyer = relationship("User", back_populates="purchase_requests")


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="favorites")
    listing = relationship("Listing", back_populates="favorites")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String(30), default="completed")  # completed, refunded, cancelled
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    listing = relationship("Listing", back_populates="transactions")
    impact = relationship("EnvironmentalImpact", back_populates="transaction", uselist=False)


class EnvironmentalImpact(Base):
    __tablename__ = "environmental_impact"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    material_type = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False)
    estimated_weight_tonnes = Column(Float, nullable=False)
    estimated_co2_saving_kg = Column(Float, nullable=False)
    virgin_material_preserved_kg = Column(Float, default=0.0)
    trees_equivalent = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    transaction = relationship("Transaction", back_populates="impact")


class ModelFeedback(Base):
    __tablename__ = "model_feedback"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    predicted_material = Column(String(100), nullable=False)
    corrected_material = Column(String(100), nullable=True)
    predicted_quality = Column(String(10), nullable=True)
    corrected_quality = Column(String(10), nullable=True)
    predicted_price = Column(Float, nullable=True)
    final_price = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    feedback_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="feedbacks")


class SearchLog(Base):
    __tablename__ = "search_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    query = Column(String(200), nullable=True)
    filters_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ListingReport(Base):
    __tablename__ = "listing_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(30), default="pending")  # pending, resolved, dismissed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
