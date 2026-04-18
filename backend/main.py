from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.api import router

app = FastAPI(title="CodeAtlas API", version="1.0.0", description="AI-powered Repository Architecture Navigator Backend")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Specify frontend origin for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to CodeAtlas API. Access /docs for Swagger UI documentation."}

if __name__ == "__main__":
    import uvicorn
    # Typically run as a module: uvicorn backend.main:app
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
