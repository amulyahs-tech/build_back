# BuildBack - AI-Powered Construction Waste Reuse & Second-Market Platform
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY backend/ ./backend/
COPY ml/ ./ml/
COPY scripts/ ./scripts/
COPY streamlit/ ./streamlit/
COPY docs/ ./docs/

EXPOSE 8000

# Run FastAPI serving unified React Single Page Application + REST API
CMD uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}
