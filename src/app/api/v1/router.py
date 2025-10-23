"""
API v1 router configuration.
This module centralizes all v1 route registrations.
"""
from fastapi import APIRouter

from app.api.v1.projects import router as projects_router
from app.api.v1.tasks import router as tasks_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(projects_router)
api_v1_router.include_router(tasks_router)
