# Root entrypoint for BuildBack cloud deployment (Render, Railway, Docker, Vercel Serverless)
import os
import uvicorn
from backend.app.main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
