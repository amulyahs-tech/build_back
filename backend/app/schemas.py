from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ------------------ Authentication Schemas ------------------

class UserBase(BaseModel):
    name: str = Field(..., example="Amulya H.S.")
    email: EmailStr = Field(..., example="amulya@greenbuild.in")
    phone: Optional[str] = Field(None, example="+91 9876543210")
    user_type: str = Field("BOTH", example="SELLER")  # SELLER, BUYER, BOTH, ADMIN
    city: str = Field("Bangalore", example="Bangalore")
    state: str = Field("Karnataka", example="Karnataka")
    pincode: str = Field("560001", example="560001")


class UserRegister(UserBase):
    password: str = Field(..., min_length=6, example="SecretPass123")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="admin@rebuildai.com")
    password: str = Field(..., example="Admin@1234")


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    user_type: Optional[str] = None


# ------------------ ML & AI Schemas ------------------

class MaterialPredictionItem(BaseModel):
    material: str
    confidence: float


class MaterialClassificationResponse(BaseModel):
    predicted_material: str
    category: str
    confidence: float
    top_predictions: List[MaterialPredictionItem]
    low_confidence_warning: bool
    recommended_applications: List[str]
    recyclability_tier: str
    is_fallback: bool = False
    embedding_length: int = 1280


class QualityAssessRequest(BaseModel):
    material_name: str = Field(..., example="Red Brick")
    age_years: float = Field(1.0, ge=0.0, example=2.0)
    damage_percentage: float = Field(10.0, ge=0.0, le=100.0, example=15.0)
    original_usage: Optional[str] = Field("Residential Demolition", example="Load-bearing wall")
    surface_wear: Optional[str] = Field("Light", example="Moderate")


class QualityAssessResponse(BaseModel):
    quality_grade: str  # A, B, C, D, E
    quality_score: float  # 0 to 100
    condition_description: str
    recommended_reuse: List[str]
    unsuitable_uses: List[str]
    disclaimer: str


class PricePredictRequest(BaseModel):
    material_name: str = Field(..., example="Red Brick")
    quantity: float = Field(..., gt=0.0, example=2000.0)
    unit: str = Field("Pieces", example="Pieces")
    quality_score: float = Field(80.0, ge=0.0, le=100.0, example=78.0)
    age_years: float = Field(1.0, ge=0.0, example=2.0)
    damage_percentage: float = Field(10.0, ge=0.0, le=100.0, example=15.0)
    city: Optional[str] = Field("Bangalore", example="Bangalore")


class PricePredictResponse(BaseModel):
    estimated_price: float
    price_range_min: float
    price_range_max: float
    price_per_unit: float
    unit: str
    original_market_rate_per_unit: float
    savings_percentage: float
    model_r2_benchmark: float = 0.9349
    model_name: str = "Gradient Boosting Regressor"
    is_fallback: bool = False


class SimilarSearchResponseItem(BaseModel):
    id: int
    material_name: str
    category: str
    image_url: str
    price: float
    quantity: float
    unit: str
    quality_grade: str
    city: str
    similarity_score: float


# ------------------ Listings Schemas ------------------

class ListingCreate(BaseModel):
    material_name: str
    category: str
    quantity: float
    unit: str = "Pieces"
    age_years: float = 1.0
    damage_percentage: float = 10.0
    price: float
    quality_grade: str = "B"
    quality_score: float = 80.0
    ai_confidence: float = 0.90
    ai_estimated_price: Optional[float] = None
    city: str = "Bangalore"
    state: str = "Karnataka"
    original_usage: str = "Residential Construction"
    availability: str = "Immediate Pickup"
    image_url: Optional[str] = None


class ListingUpdate(BaseModel):
    price: Optional[float] = None
    quantity: Optional[float] = None
    availability: Optional[str] = None
    status: Optional[str] = None


class ListingResponse(BaseModel):
    id: int
    seller_id: int
    material_name: str
    category: str
    image_url: str
    ai_confidence: float
    quality_grade: str
    quality_score: float
    quantity: float
    unit: str
    age_years: float
    damage_percentage: float
    price: float
    ai_estimated_price: Optional[float]
    city: str
    state: str
    original_usage: str
    availability: str
    status: str
    created_at: datetime
    seller_name: Optional[str] = None
    seller_phone: Optional[str] = None
    is_favorited: Optional[bool] = False

    class Config:
        from_attributes = True


# ------------------ Purchase Request Schemas ------------------

class PurchaseRequestCreate(BaseModel):
    listing_id: int
    quantity: float
    proposed_price: float
    message: Optional[str] = None
    preferred_pickup_date: Optional[str] = None


class PurchaseRequestResponse(BaseModel):
    id: int
    listing_id: int
    buyer_id: int
    quantity: float
    proposed_price: float
    message: Optional[str]
    preferred_pickup_date: Optional[str]
    status: str
    created_at: datetime
    material_name: Optional[str] = None
    image_url: Optional[str] = None
    buyer_name: Optional[str] = None
    seller_name: Optional[str] = None

    class Config:
        from_attributes = True


class PurchaseRequestAction(BaseModel):
    status: str = Field(..., example="accepted")  # accepted or rejected


# ------------------ Environmental Impact Schemas ------------------

class EnvironmentalImpactResponse(BaseModel):
    material_type: str
    quantity: float
    unit: str
    estimated_weight_tonnes: float
    estimated_co2_saving_kg: float
    virgin_material_preserved_kg: float
    trees_equivalent: float
    disclaimer: str


class EnvironmentalSummaryResponse(BaseModel):
    total_landfill_diverted_tonnes: float
    total_co2_saved_kg: float
    total_virgin_material_saved_kg: float
    total_trees_equivalent: float
    total_transactions: int
    material_breakdown: Dict[str, float]


# ------------------ Feedback & Telemetry Schemas ------------------

class ModelFeedbackCreate(BaseModel):
    listing_id: Optional[int] = None
    predicted_material: str
    corrected_material: Optional[str] = None
    predicted_quality: Optional[str] = None
    corrected_quality: Optional[str] = None
    predicted_price: Optional[float] = None
    final_price: Optional[float] = None
    confidence: Optional[float] = None
    feedback_notes: Optional[str] = None


class ModelFeedbackResponse(BaseModel):
    id: int
    message: str = "Feedback submitted successfully for retraining."


class AdminStatsResponse(BaseModel):
    total_users: int
    total_listings: int
    active_listings: int
    total_transactions: int
    total_diverted_tonnes: float
    total_co2_saved_kg: float
    materials_count: int


class AIMonitoringStats(BaseModel):
    total_predictions: int
    average_confidence: float
    low_confidence_count: int
    feedback_count: int
    user_correction_rate: float
    model_r2_score: float = 0.9349
    classification_accuracy: float = 0.942
