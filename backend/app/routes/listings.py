import os
import json
import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from backend.app.database import get_db
from backend.app.models import Listing, User, Favorite
from backend.app.schemas import ListingCreate, ListingUpdate, ListingResponse
from backend.app.utils.security import get_current_user, get_optional_current_user, require_seller
from backend.app.ml.material_classifier import material_classifier

router = APIRouter(prefix="/api/listings", tags=["Marketplace Listings"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _serialize_listing(listing: Listing, current_user_id: Optional[int] = None) -> dict:
    """Helper to serialize Listing model into ListingResponse dictionary."""
    is_fav = False
    if current_user_id and listing.favorites:
        is_fav = any(f.user_id == current_user_id for f in listing.favorites)

    seller_name = listing.seller.name if listing.seller else "Unknown Seller"
    seller_phone = listing.seller.phone if listing.seller else None

    return {
        "id": listing.id,
        "seller_id": listing.seller_id,
        "material_name": listing.material_name,
        "category": listing.category,
        "image_url": listing.image_url,
        "ai_confidence": listing.ai_confidence,
        "quality_grade": listing.quality_grade,
        "quality_score": listing.quality_score,
        "quantity": listing.quantity,
        "unit": listing.unit,
        "age_years": listing.age_years,
        "damage_percentage": listing.damage_percentage,
        "price": listing.price,
        "ai_estimated_price": listing.ai_estimated_price,
        "city": listing.city,
        "state": listing.state,
        "original_usage": listing.original_usage,
        "availability": listing.availability,
        "status": listing.status,
        "created_at": listing.created_at,
        "seller_name": seller_name,
        "seller_phone": seller_phone,
        "is_favorited": is_fav
    }


@router.get("", response_model=List[ListingResponse])
def get_listings(
    material: Optional[str] = None,
    category: Optional[str] = None,
    quality_grade: Optional[str] = None,
    city: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "newest",
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve filtered and sorted marketplace listings."""
    query = db.query(Listing).filter(Listing.status == "active")

    if material:
        query = query.filter(Listing.material_name.ilike(f"%{material}%"))
    if category:
        query = query.filter(Listing.category.ilike(f"%{category}%"))
    if quality_grade:
        query = query.filter(Listing.quality_grade == quality_grade.upper())
    if city:
        query = query.filter(Listing.city.ilike(f"%{city}%"))
    if min_price is not None:
        query = query.filter(Listing.price >= min_price)
    if max_price is not None:
        query = query.filter(Listing.price <= max_price)
    if search:
        query = query.filter(
            or_(
                Listing.material_name.ilike(f"%{search}%"),
                Listing.category.ilike(f"%{search}%"),
                Listing.city.ilike(f"%{search}%"),
                Listing.original_usage.ilike(f"%{search}%")
            )
        )

    # Sorting
    if sort_by == "price_asc":
        query = query.order_by(Listing.price.asc())
    elif sort_by == "price_desc":
        query = query.order_by(Listing.price.desc())
    elif sort_by == "quality":
        query = query.order_by(Listing.quality_score.desc())
    else:
        query = query.order_by(Listing.created_at.desc())

    listings = query.all()
    user_id = current_user.id if current_user else None
    return [_serialize_listing(item, user_id) for item in listings]


@router.post("", response_model=ListingResponse, status_code=status.HTTP_201_CREATED)
def create_listing(
    payload: ListingCreate,
    current_user: User = Depends(require_seller),
    db: Session = Depends(get_db)
):
    """Create a new construction material listing with seller parameters and AI metadata."""
    img_url = payload.image_url or "/static/images/placeholder_material.jpg"

    new_listing = Listing(
        seller_id=current_user.id,
        material_name=payload.material_name,
        category=payload.category,
        image_url=img_url,
        ai_confidence=payload.ai_confidence,
        quality_grade=payload.quality_grade.upper(),
        quality_score=payload.quality_score,
        quantity=payload.quantity,
        unit=payload.unit,
        age_years=payload.age_years,
        damage_percentage=payload.damage_percentage,
        price=payload.price,
        ai_estimated_price=payload.ai_estimated_price or payload.price,
        city=payload.city or current_user.city,
        state=payload.state or current_user.state,
        original_usage=payload.original_usage,
        availability=payload.availability,
        status="active"
    )
    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)

    return _serialize_listing(new_listing, current_user.id)


@router.get("/my-listings", response_model=List[ListingResponse])
def get_my_listings(
    current_user: User = Depends(require_seller),
    db: Session = Depends(get_db)
):
    """Retrieve all listings created by the logged-in seller."""
    listings = db.query(Listing).filter(Listing.seller_id == current_user.id).order_by(Listing.created_at.desc()).all()
    return [_serialize_listing(item, current_user.id) for item in listings]


@router.get("/my-favorites", response_model=List[ListingResponse])
def get_my_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve listings favorited by current user."""
    favs = db.query(Favorite).filter(Favorite.user_id == current_user.id).all()
    listing_ids = [f.listing_id for f in favs]
    listings = db.query(Listing).filter(Listing.id.in_(listing_ids)).all()
    return [_serialize_listing(item, current_user.id) for item in listings]


@router.get("/{listing_id}", response_model=ListingResponse)
def get_listing_detail(
    listing_id: int,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve full details of a specific material listing."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found.")
    user_id = current_user.id if current_user else None
    return _serialize_listing(listing, user_id)


@router.put("/{listing_id}", response_model=ListingResponse)
def update_listing(
    listing_id: int,
    payload: ListingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update price, quantity, availability or status of a listing."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found.")

    if listing.seller_id != current_user.id and current_user.user_type != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to edit this listing.")

    if payload.price is not None:
        listing.price = payload.price
    if payload.quantity is not None:
        listing.quantity = payload.quantity
    if payload.availability is not None:
        listing.availability = payload.availability
    if payload.status is not None:
        listing.status = payload.status

    db.commit()
    db.refresh(listing)
    return _serialize_listing(listing, current_user.id)


@router.delete("/{listing_id}")
def delete_listing(
    listing_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete or archive a listing."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found.")

    if listing.seller_id != current_user.id and current_user.user_type != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this listing.")

    db.delete(listing)
    db.commit()
    return {"message": "Listing deleted successfully."}


@router.post("/{listing_id}/favorite")
def toggle_favorite(
    listing_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle a listing in user's saved/favorite list."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found.")

    existing_fav = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.listing_id == listing_id
    ).first()

    if existing_fav:
        db.delete(existing_fav)
        db.commit()
        return {"favorited": False, "message": "Removed from saved materials."}
    else:
        new_fav = Favorite(user_id=current_user.id, listing_id=listing_id)
        db.add(new_fav)
        db.commit()
        return {"favorited": True, "message": "Saved to favorite materials."}
