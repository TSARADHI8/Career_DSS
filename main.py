"""
Career Decision Support System — FastAPI Backend
Run with: uvicorn main:app --reload
API docs at: http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from database import engine
import models
from routers import auth_router, predict_router, admin_router

# Create all PostgreSQL tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Career DSS API",
    description="Decision Support System for B.Tech career guidance",
    version="2.0.0",
)

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all route groups
app.include_router(auth_router.router)
app.include_router(predict_router.router)
app.include_router(admin_router.router)

# Serve the frontend HTML
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", include_in_schema=False)
def root():
    return FileResponse("frontend/index.html")

@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}
