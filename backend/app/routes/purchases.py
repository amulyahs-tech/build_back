from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import PurchaseRequest, Listing, Transaction, EnvironmentalImpact, User
from backend.app.schemas import PurchaseRequestCreate, PurchaseRequestResponse, PurchaseRequestAction
from backend.app.utils.security import get_current_user
from backend.app.ml.environmental_calculator import calculate_environmental_impact

router = APIRouter(prefix="/api/purchases", tags=["Purchases & Transactions"])


def _serialize_request(req: PurchaseRequest) -> dict:
    return {
        "id": req.id,
        "listing_id": req.listing_id,
        "buyer_id": req.buyer_id,
        "quantity": req.quantity,
        "proposed_price": req.proposed_price,
        "message": req.message,
        "preferred_pickup_date": req.preferred_pickup_date,
        "status": req.status,
        "created_at": req.created_at,
        "material_name": req.listing.material_name if req.listing else None,
        "image_url": req.listing.image_url if req.listing else None,
        "buyer_name": req.buyer.name if req.buyer else None,
        "seller_name": req.listing.seller.name if (req.listing and req.listing.seller) else None
    }


@router.post("/request", response_model=PurchaseRequestResponse, status_code=status.HTTP_201_CREATED)
def create_purchase_request(
    payload: PurchaseRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Buyer submits a purchase / pickup offer for a listed material."""
    listing = db.query(Listing).filter(Listing.id == payload.listing_id).first()
    if not listing or listing.status != "active":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing is no longer active or not found.")

    if listing.seller_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot make an offer on your own listing.")

    req = PurchaseRequest(
        listing_id=listing.id,
        buyer_id=current_user.id,
        quantity=payload.quantity,
        proposed_price=payload.proposed_price,
        message=payload.message,
        preferred_pickup_date=payload.preferred_pickup_date,
        status="pending"
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return _serialize_request(req)


@router.get("/my-requests", response_model=List[PurchaseRequestResponse])
def get_my_purchase_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve purchase requests sent by the current buyer."""
    requests = db.query(PurchaseRequest).filter(
        PurchaseRequest.buyer_id == current_user.id
    ).order_by(PurchaseRequest.created_at.desc()).all()
    return [_serialize_request(r) for r in requests]


@router.get("/incoming-requests", response_model=List[PurchaseRequestResponse])
def get_incoming_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve offers received by the current seller for their listed materials."""
    requests = db.query(PurchaseRequest).join(Listing).filter(
        Listing.seller_id == current_user.id
    ).order_by(PurchaseRequest.created_at.desc()).all()
    return [_serialize_request(r) for r in requests]


@router.put("/request/{request_id}", response_model=PurchaseRequestResponse)
def update_purchase_request_status(
    request_id: int,
    action: PurchaseRequestAction,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Seller accepts or rejects a purchase request. Acceptance automatically records transaction & LCA metrics."""
    req = db.query(PurchaseRequest).filter(PurchaseRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase request not found.")

    listing = req.listing
    if listing.seller_id != current_user.id and current_user.user_type != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the seller can accept or reject this request.")

    new_status = action.status.lower()
    if new_status not in ["accepted", "rejected", "completed"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status must be 'accepted' or 'rejected'.")

    req.status = new_status

    if new_status == "accepted":
        # 1. Create completed transaction
        tx = Transaction(
            listing_id=listing.id,
            buyer_id=req.buyer_id,
            seller_id=listing.seller_id,
            quantity=req.quantity,
            price=req.proposed_price,
            status="completed"
        )
        db.add(tx)
        db.flush()

        # 2. Automatically compute and store verified Environmental Impact
        impact_calc = calculate_environmental_impact(
            material_name=listing.material_name,
            quantity=req.quantity,
            unit=listing.unit
        )
        env_record = EnvironmentalImpact(
            transaction_id=tx.id,
            material_type=listing.material_name,
            quantity=req.quantity,
            estimated_weight_tonnes=impact_calc["estimated_weight_tonnes"],
            estimated_co2_saving_kg=impact_calc["estimated_co2_saving_kg"],
            virgin_material_preserved_kg=impact_calc["virgin_material_preserved_kg"],
            trees_equivalent=impact_calc["trees_equivalent"]
        )
        db.add(env_record)

        # 3. Mark listing as sold
        listing.status = "sold"

    db.commit()
    db.refresh(req)
    return _serialize_request(req)
