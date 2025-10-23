from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from contextlib import asynccontextmanager
from app.core.db.database import initialize_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database()
    yield

app = FastAPI(
    title="Taller Challenge API",
    description="A clean API for managing projects and tasks",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_router)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Taller Challenge API is running!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}
