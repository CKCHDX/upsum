from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from search import router as search_router
from pathlib import Path

app = FastAPI(
    title="Upsum Backend", 
    description="API for Upsum — Project Nexus", 
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"]
)
app.include_router(search_router)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return JSONResponse({"status": "ok", "message": "Upsum backend is running."})

@app.get("/")
def serve_frontend():
    """Serve the frontend HTML file."""
    frontend_path = Path(__file__).parent.parent / "frontend" / "frontend.html"
    return FileResponse(frontend_path)
