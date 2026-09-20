import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from backend.app.main import app
from backend.app.database import SessionLocal, Base, engine
from backend.app.models import User, Listing, Transaction, EnvironmentalImpact
from scripts.seed_database import seed_database

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Ensure database tables and initial test records exist."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    db.close()


def test_health_endpoint():
    """Test backend health check."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_auth_login_success():
    """Test login with seeded admin credentials."""
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@rebuildai.com", "password": "Admin@1234"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "admin@rebuildai.com"
    assert data["user"]["user_type"] == "ADMIN"


def test_auth_login_invalid_password():
    """Test login failure on bad password."""
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@rebuildai.com", "password": "WrongPassword999"}
    )
    assert response.status_code == 401


def test_auth_register_new_user():
    """Test registering a new buyer/seller account."""
    payload = {
        "name": "Eco Builder",
        "email": "ecobuilder_test@example.com",
        "phone": "+91 9988776655",
        "password": "StrongPassword123",
        "user_type": "BUYER",
        "city": "Bangalore",
        "state": "Karnataka",
        "pincode": "560001"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert response.json()["user"]["email"] == "ecobuilder_test@example.com"


def test_material_classification_with_image():
    """Test ML material classification endpoint with a synthetic RGB image."""
    img = Image.new("RGB", (224, 224), color=(180, 50, 40))  # Brick-red tone
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)

    files = {"file": ("test_brick.jpg", img_byte_arr, "image/jpeg")}
    response = client.post("/api/ml/predict-material", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_material" in data
    assert "confidence" in data
    assert data["confidence"] > 0.0
    assert len(data["top_predictions"]) > 0
    assert "recommended_applications" in data
    assert "recyclability_tier" in data


def test_quality_assessment():
    """Test multimodal quality grading (Grade A-E, 0-100 score)."""
    payload = {
        "material_name": "Bricks",
        "age_years": 1.5,
        "damage_percentage": 5.0,
        "original_usage": "Residential Partition",
        "surface_wear": "Light"
    }
    response = client.post("/api/ml/assess-quality", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["quality_grade"] in ["A", "B", "C", "D", "E"]
    assert 0.0 <= data["quality_score"] <= 100.0
    assert "recommended_reuse" in data
    assert "disclaimer" in data


def test_price_prediction_regression():
    """Test Gradient Boosting price regression."""
    payload = {
        "material_name": "Bricks",
        "quantity": 2500.0,
        "unit": "Pieces",
        "quality_score": 85.0,
        "age_years": 1.0,
        "damage_percentage": 5.0,
        "city": "Bangalore"
    }
    response = client.post("/api/ml/predict-price", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["estimated_price"] > 0.0
    assert data["price_range_min"] < data["price_range_max"]
    assert data["savings_percentage"] >= 0.0
    assert data["model_r2_benchmark"] >= 0.90


def test_listings_get_and_filter():
    """Test retrieving marketplace listings with category and search filters."""
    response = client.get("/api/listings")
    assert response.status_code == 200
    listings = response.json()
    assert len(listings) > 0

    # Filter by category
    resp_masonry = client.get("/api/listings?category=Masonry")
    assert resp_masonry.status_code == 200
    assert all("Masonry" in item["category"] for item in resp_masonry.json())


def test_environmental_impact_summary():
    """Test cumulative environmental summary endpoint."""
    response = client.get("/api/environmental/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_landfill_diverted_tonnes" in data
    assert "total_co2_saved_kg" in data
    assert "material_breakdown" in data
    assert data["total_transactions"] >= 0


def test_environmental_calculate_get_and_post():
    """Test both GET and POST environmental LCA calculation endpoints."""
    # GET test
    resp_get = client.get("/api/environmental/calculate?material_name=Bricks&quantity=1200&unit=Pieces")
    assert resp_get.status_code == 200
    d_get = resp_get.json()
    assert d_get["estimated_weight_tonnes"] > 0
    assert d_get["estimated_co2_saving_kg"] > 0

    # POST test
    resp_post = client.post("/api/environmental/calculate", json={
        "material_name": "Concrete",
        "quantity": 5000,
        "unit": "Kg"
    })
    assert resp_post.status_code == 200
    d_post = resp_post.json()
    assert d_post["estimated_weight_tonnes"] > 0
    assert d_post["estimated_co2_saving_kg"] > 0



def test_admin_monitoring():
    """Test admin AI monitoring endpoint with valid admin token."""
    # Login as admin
    login_resp = client.post(
        "/api/auth/login",
        json={"email": "admin@rebuildai.com", "password": "Admin@1234"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/admin/ai-monitoring", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "average_confidence" in data
    assert data["model_r2_score"] >= 0.90
    assert data["classification_accuracy"] >= 0.90
