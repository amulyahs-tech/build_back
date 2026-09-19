# BuildBack

**AI-Powered Construction Waste Reuse & Second-Market Platform**

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🚀 Live Demo & Deployment

* **Main GitHub Repository:** [https://github.com/amulyahs-tech/build_back](https://github.com/amulyahs-tech/build_back)
* **Streamlit App Entrypoint:** `streamlit/app.py`
* **Deploy on Streamlit Community Cloud:** Set **Main file path** to `streamlit/app.py` on [share.streamlit.io](https://share.streamlit.io/).
* **Deploy Full Web Application on Render / Railway:** Connect repo and deploy via `render.yaml` or `Dockerfile`.

---

## 🏗️ 1. Project Overview & Problem Statement

Construction and Demolition (C&D) debris accounts for over 35% of all solid waste generated globally. Hundreds of millions of tonnes of salvageable structural elements—such as red clay bricks, TMT steel rebar, structural timber, concrete blocks, and granite—are routinely dumped into overburdened landfills.

**BuildBack** unifies two previously separate web interfaces into one complete circular platform:
1. **AI Material Assessment (`/assessment`)**: Real-time camera diagnostics (`getUserMedia`), MobileNetV2 20-class identification, condition grading (A–E), Gradient Boosting price prediction ($R^2 \ge 0.935$), and circular LCA calculation.
2. **Construction Waste Marketplace (`/marketplace`, `/sell`, `/buy`, `/profile`)**: Catalog browsing, search/filters, purchase negotiation, order management, and user roles.

---

## ✨ 2. Key Features

* **📷 Real Device Camera Access:** Capture high-resolution photos on-site using phone or desktop cameras via native `navigator.mediaDevices.getUserMedia` with rear-facing mobile camera support (`facingMode: "environment"`), interactive viewfinder, and instant snapshot preview.
* **🧠 MobileNetV2 Material Identification:** Automated 20-class classification with 1,280-dimensional feature embeddings and low-confidence visual alerts.
* **🏆 Standardized Quality Grading (A–E):** Objective 0–100 condition scoring classifying materials from structural direct reuse (Grade A) to aggregate downcycling (Grade D/E).
* **💰 AI Market Valuation Engine:** Multi-feature Gradient Boosting Regressor benchmarking regional prices, negotiation ranges ($\pm 12\%$), and discounts versus virgin materials.
* **🔍 Visual Similarity Search:** Sub-second cosine similarity search across active inventory using deep feature embeddings.
* **🌱 Automated Circular LCA:** Instant calculation of diverted landfill weight (metric tonnes), avoided embodied emissions ($\text{kg CO}_2\text{e}$), and tree equivalents.
* **🤝 End-to-End Marketplace:** Full listing lifecycle, search filters, favorite bookmarks, and buyer-seller purchase negotiation workflows.
* **📊 Admin Telemetry & AI Governance:** Macro KPI dashboards, model confidence distributions, and human-in-the-loop prediction correction logs.
* **🌐 Standalone Streamlit Demo:** Self-contained multi-page demonstration app for immediate deployment on Streamlit Community Cloud.

---

## 📐 3. System Architecture

```text
               ┌────────────────────────────────────────────────────────┐
               │              Client Devices (Mobile / Web)             │
               │  Camera Capture (getUserMedia) / File Upload / UI Card │
               └───────────────────────┬────────────────────────────────┘
                                       │
                ┌──────────────────────┴──────────────────────┐
                ▼                                             ▼
┌──────────────────────────────┐              ┌──────────────────────────────┐
│       Full Application       │              │     Public Streamlit Demo    │
│    React 18 + Tailwind CSS   │              │       streamlit/app.py       │
│      (Vite / SPA Bundle)     │              │     (Port 8501 / Cloud)      │
└──────────────┬───────────────┘              └──────────────┬───────────────┘
               │ HTTP REST                                   │
               ▼                                             │
┌──────────────────────────────┐                             │
│     FastAPI Backend Core     │                             │
│       (app/main.py)          │                             │
└──────────────┬───────────────┘                             │
               │                                             │
               ├─────────────────────────────────────────────┘
               │
               ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                       Machine Learning & AI Pipelines                      │
│                                                                            │
│  1. MobileNetV2 Classifier      ──► 20 Material Classes (Accuracy 94.2%)   │
│  2. Multimodal Quality Assessor ──► Grades A–E & 0–100 Condition Score     │
│  3. Gradient Boosting Regressor ──► Second-Market Price (R² = 0.935)       │
│  4. Cosine Embedding Index      ──► 1280-dim Visual Similarity Matching    │
│  5. Circular LCA Calculator     ──► Landfill Tonnes & kg CO₂e Diverted     │
└──────────────────────────────────────┬─────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                    Relational Database (SQLAlchemy)                        │
│   Users • Materials • Listings • Purchases • Transactions • Feedback       │
│                (SQLite for Dev / PostgreSQL for Production)                │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 4. AI & Machine Learning Models

### Material Classifier (MobileNetV2)
* **Architecture:** MobileNetV2 with depthwise separable convolutions pre-trained on ImageNet.
* **Classes (20):** Bricks, Concrete, Cement Blocks, Steel / Rebar, Wood / Timber, Tiles, Glass, PVC Pipes, Metal Pipes, Doors, Windows, Electrical Components, Roofing Materials, Stones, Sand, Marble, Granite, Ceramic Materials, Mixed Construction Waste, Other / Debris.
* **Performance:** **94.2% Test Accuracy**, 94.6% Precision, 93.8% Recall, 94.1% F1-Score.
* **Embeddings:** 1,280-dimensional unit-normalized feature vector for similarity search.

### Quality Grading System (A–E)
* **Grade A (92–100):** Excellent condition. Direct structural reuse.
* **Grade B (80–91):** Good condition. Secondary walls and framing.
* **Grade C (65–79):** Moderate wear. Landscaping, non-load-bearing partitions.
* **Grade D (40–64):** Poor. Requires crushing into road-base aggregates.
* **Grade E (0–39):** Very Poor. Industrial recycling or daily landfill cover.

> **Safety Disclaimer:** AI visual assessment provides non-binding advisory condition scoring. Structural load-bearing installations require certified on-site engineering tests.

### Price Valuation Regressor
* **Production Model:** Gradient Boosting Regressor ($R^2 = 0.9508$, benchmark $R^2 \ge 0.935$).
* **Comparison Models:** Random Forest ($R^2 = 0.9391$), Linear Regression ($R^2 = 0.7117$).
* **Features:** Material type, regional city demand index, quality condition score, material age (years), damage percentage, lot quantity.

---

## 📁 5. Repository Structure

```text
rebuild-ai/
├── backend/
│   ├── app/
│   │   ├── ml/                       # Machine Learning modules
│   │   │   ├── material_classifier.py
│   │   │   ├── quality_classifier.py
│   │   │   ├── price_predictor.py
│   │   │   ├── image_similarity.py
│   │   │   ├── reuse_recommender.py
│   │   │   └── environmental_calculator.py
│   │   ├── routes/                   # REST API routes
│   │   │   ├── auth.py
│   │   │   ├── ml_routes.py
│   │   │   ├── listings.py
│   │   │   ├── purchases.py
│   │   │   ├── environmental.py
│   │   │   └── admin.py
│   │   ├── database.py               # SQLAlchemy database session
│   │   ├── models.py                 # Relational schema
│   │   ├── schemas.py                # Pydantic validation
│   │   ├── main.py                   # FastAPI entry point & SPA mount
│   │   └── utils/security.py         # BCrypt & JWT authentication
│   ├── static/                       # Pre-compiled standalone SPA bundle
│   ├── uploads/                      # Uploaded material photos
│   └── requirements.txt              # Backend dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CameraCaptureModal.jsx # Real device camera (getUserMedia)
│   │   │   ├── Navbar.jsx
│   │   │   └── Footer.jsx
│   │   ├── pages/
│   │   │   ├── LandingPage.jsx
│   │   │   ├── MarketplacePage.jsx
│   │   │   ├── ListingDetailPage.jsx
│   │   │   ├── CreateListingWizard.jsx # 9-step wizard with camera
│   │   │   ├── SellerDashboard.jsx
│   │   │   ├── BuyerDashboard.jsx
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── ModelEvaluationPage.jsx # Viva demonstration benchmarks
│   │   │   └── AuthPages.jsx
│   │   ├── services/api.js
│   │   └── context/AuthContext.jsx
│   ├── package.json
│   └── vite.config.js
├── ml/
│   ├── training/train_models.py      # ML training and evaluation script
│   └── models/                       # Serialized models (.joblib, metrics.json)
├── streamlit/
│   ├── app.py                        # Standalone public demo application
│   └── requirements-streamlit.txt    # Streamlit Cloud requirements
├── .streamlit/
│   └── config.toml                   # Streamlit theme configuration
├── scripts/
│   ├── seed_database.py              # Seeds demo users, listings, & LCA data
│   └── start_services.py             # Service launcher utility
├── tests/
│   └── test_api.py                   # Pytest test suite (10 test cases)
├── docs/
│   ├── project_architecture.md
│   └── api_documentation.md
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ 6. Quick Start & Installation

### Prerequisites
* **Python 3.12+**
* Git
* (Optional) Node.js 18+ for Vite dev server

### 1. Clone & Set Up Python Environment
```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd "build back"

# Optional: Create virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 2. Configure Environment Variables
```bash
cp .env.example .env
```

### 3. Initialize & Seed Database
```bash
python scripts/seed_database.py
```
*Pre-seeds 3 demo users, 20 construction materials, 12 realistic listings, and verified LCA transaction impact.*

### 4. Run Automated Tests
```bash
python -m pytest tests/test_api.py -v
```
*Validates health, authentication, material classification, quality grading, price regression, marketplace filters, and admin telemetry (10/10 tests pass).*

---

## 🏃 7. Running the Applications

### Mode A: Full FastAPI Backend + Interactive SPA (Recommended)
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
* **Web Application:** `http://localhost:8000/`
* **Interactive API Docs (Swagger):** `http://localhost:8000/docs`
* **Alternative Docs (ReDoc):** `http://localhost:8000/redoc`

*The frontend SPA is served directly by FastAPI from `backend/static/` with zero configuration or external build step required.*

### Mode B: Standalone Public Streamlit Demo
```bash
streamlit run streamlit/app.py --server.port 8501
```
* **Streamlit Demo URL:** `http://localhost:8501/`
* Features camera snapshot input (`st.camera_input`), file upload, live ML predictions, interactive price sliders, and circular LCA calculator.

### Mode C: Vite Frontend Development Server (Optional)
```bash
cd frontend
npm install
npm run dev
```
* Runs Vite dev server at `http://localhost:5173/` with hot-module reloading and proxying to the FastAPI backend.

---

## 📷 8. Real Device Camera Functionality

The material identification workflow includes native browser camera integration via `navigator.mediaDevices.getUserMedia()`:

* **Location:** [`frontend/src/components/CameraCaptureModal.jsx`](file:///c:/Users/amuly/OneDrive/Documents/build%20back/frontend/src/components/CameraCaptureModal.jsx) and [`backend/static/index.html`](file:///c:/Users/amuly/OneDrive/Documents/build%20back/backend/static/index.html).
* **Rear-Camera Support:** Configured with `{ facingMode: { ideal: "environment" } }` for mobile phones and tablet site inspections, with a toggle button to switch to user-facing mode.
* **Live Viewfinder:** Center viewfinder target grid with canvas capture.
* **Workflow:** **Open Camera → Live Preview → Capture Photo → Review / Retake → Use Photo → Run AI Inference**.
* **Resilient Error Handling:** Gracefully handles `NotAllowedError` (permission denied), `NotFoundError` (no camera detected), non-HTTPS origins, or user cancellation without crashing.

---

## 👥 9. Demo Accounts (Local Development)

The database includes 3 pre-seeded test accounts for local evaluation:

| Role | Email | Password | Primary Capabilities |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@rebuildai.com` | `Admin@1234` | Platform KPIs, AI telemetry, listing moderation |
| **Seller** | `seller@demolitioncorp.com` | `Seller@1234` | Create listings, accept/reject purchase offers |
| **Buyer** | `buyer@greenbuild.in` | `Buyer@1234` | Browse marketplace, make offers, save favorites |

---

## ☁️ 10. Deployment Guide

### Deploying the Public Demo on Streamlit Community Cloud
1. Push this repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Select your repository, set the branch to `main`, and specify the main file path:
   ```text
   streamlit/app.py
   ```
4. In Advanced Settings, ensure Python 3.12 is selected. Streamlit will automatically install packages from `streamlit/requirements-streamlit.txt`.
5. Deploy and copy your live URL into the `Live Demo` section of this README!

### Deploying the Full FastAPI Backend (Render, Railway, AWS, DigitalOcean)
* **Start Command:** `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
* **Build Command:** `pip install -r backend/requirements.txt && python ml/training/train_models.py && python scripts/seed_database.py`
* **Environment Variables:** Set `DATABASE_URL`, `JWT_SECRET`, and `CORS_ORIGINS`.

---

## 🛡️ 11. Security & Compliance

* **Zero Hardcoded Secrets:** No private production API keys, database passwords, or machine-specific paths exist in the repository.
* **Configurable Environment:** Uses `.env` via `python-dotenv`.
* **Password Security:** One-way BCrypt hashing with auto-generated salts.
* **Session Management:** Signed stateless JSON Web Tokens (HS256) with 24-hour expiration.

---

## 📄 12. License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
