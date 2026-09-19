# REBUILD AI — API Documentation

Interactive Swagger documentation is served live at: `http://localhost:8000/docs` (or `/redoc`).

## Base Endpoints

### 1. Authentication (`/api/auth`)
* `POST /api/auth/register`: Register new contractor/buyer account.
  * Body: `{ name, email, password, user_type: "SELLER"|"BUYER"|"BOTH", city, state, pincode }`
  * Response: `{ access_token, token_type, user: { id, name, email, ... } }`
* `POST /api/auth/login`: Authenticate credentials and receive Bearer JWT.
  * Body: `{ email, password }`
  * Response: `{ access_token, token_type, user }`
* `GET /api/auth/me`: Retrieve current logged-in profile.
  * Headers: `Authorization: Bearer <token>`

### 2. Machine Learning & Computer Vision (`/api/ml`)
* `POST /api/ml/predict-material`: Classify material from camera photo or image file.
  * Payload: `multipart/form-data` with `file` OR `base64_image`
  * Response: `{ predicted_material, category, confidence, top_predictions: [...], low_confidence_warning, recommended_applications: [...], recyclability_tier }`
* `POST /api/ml/assess-quality`: Evaluate material condition into Grade A–E and 0–100 score.
  * Body: `{ material_name, age_years, damage_percentage, original_usage, surface_wear }`
  * Response: `{ quality_grade, quality_score, condition_name, condition_description, recommended_reuse: [...], unsuitable_uses: [...], disclaimer }`
* `POST /api/ml/predict-price`: Predict secondary market price.
  * Body: `{ material_name, quantity, unit, quality_score, age_years, damage_percentage, city }`
  * Response: `{ estimated_price, price_range_min, price_range_max, price_per_unit, unit, original_market_rate_per_unit, savings_percentage, model_name, model_r2_benchmark }`
* `POST /api/ml/image-search`: Find visually similar materials using 1280-dim cosine embeddings.
  * Payload: `multipart/form-data` with `file` OR `base64_image`
  * Response: `[ { id, material_name, category, price, quality_grade, similarity_score, ... } ]`
* `POST /api/ml/feedback`: Record human validation/correction for continuous retraining.
  * Body: `{ predicted_material, corrected_material, predicted_quality, final_price, confidence, feedback_notes }`
* `GET /api/ml/model-metrics`: Retrieve live test metrics (Accuracy: 94.2%, $R^2$: 0.935–0.951).

### 3. Marketplace Listings (`/api/listings`)
* `GET /api/listings`: Search active inventory with query filters (`material`, `category`, `quality_grade`, `city`, `min_price`, `max_price`, `sort_by`).
* `POST /api/listings`: Create new listing (Seller/Admin only).
* `GET /api/listings/{id}`: Detailed listing view with seller metadata and circular LCA.
* `PUT /api/listings/{id}`: Update listing.
* `DELETE /api/listings/{id}`: Delete listing.
* `POST /api/listings/{id}/favorite`: Toggle user saved item.
* `GET /api/listings/my-listings`: Seller's inventory.
* `GET /api/listings/my-favorites`: Buyer's saved materials.

### 4. Purchases & Trade Offers (`/api/purchases`)
* `POST /api/purchases/request`: Buyer submits price offer, quantity, and pickup date.
* `GET /api/purchases/my-requests`: Buyer's sent offers.
* `GET /api/purchases/incoming-requests`: Seller's received offers.
* `PUT /api/purchases/request/{id}`: Seller accepts or rejects offer.
  * *Accepting an offer automatically completes a `Transaction`, marks listing as `sold`, and generates verified `EnvironmentalImpact` records.*

### 5. Environmental & Circular LCA (`/api/environmental`)
* `GET /api/environmental/summary`: Cumulative platform savings (tonnes diverted, CO₂e saved, trees equivalent).
* `GET /api/environmental/calculate`: Arbitrary material LCA calculator.

### 6. Admin Telemetry & Governance (`/api/admin`)
* `GET /api/admin/statistics`: Macro KPI counters.
* `GET /api/admin/ai-monitoring`: Prediction telemetry, average confidence, user correction rate.
* `GET /api/admin/listings`: Moderation table.
* `POST /api/admin/flag-listing/{id}`: Moderate/flag listing.
