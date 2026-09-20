import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.database import engine, Base, SessionLocal
from backend.app.routes import auth, ml_routes, listings, purchases, environmental, admin
from scripts.seed_database import seed_if_empty

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="REBUILD AI API",
    description="AI-Powered Construction Waste Reuse & Second-Market Platform REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration: permits local development and all Vercel preview/production deployments
raw_origins = os.getenv("CORS_ORIGINS", "*")
origins = [o.strip() for o in raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_origin_regex=r"^https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router)
app.include_router(ml_routes.router)
app.include_router(listings.router)
app.include_router(purchases.router)
app.include_router(environmental.router)
app.include_router(admin.router)

# Mount Uploads directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.on_event("startup")
def startup_event():
    """Seed initial demo materials and accounts on launch if database is clean."""
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "REBUILD AI Backend", "version": "1.0.0"}


# Serve Single Page Application (SPA) fallback
@app.get("/{full_path:path}")
async def serve_spa(request: Request, full_path: str):
    """Serves compiled frontend SPA for non-API routes."""
    # Don't intercept API or uploaded file routes
    if full_path.startswith("api/") or full_path.startswith("uploads/") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
        return {"detail": "Not found"}

    file_path = os.path.join(STATIC_DIR, full_path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)

    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)

    return {
        "platform": "REBUILD AI",
        "description": "AI-Powered Construction Waste Reuse & Second-Market Platform",
        "api_docs": "/docs",
        "health": "/api/health"
    }
