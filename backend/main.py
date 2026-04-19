import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()
import backend.routes.api as api

app = FastAPI(title="CodeAtlas API", version="1.0.0", description="AI-powered Repository Architecture Navigator Backend")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Specify frontend origin for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")

# Mount frontend directory for static UI serving at the root URL
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    # Typically run as a module: uvicorn backend.main:app
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
