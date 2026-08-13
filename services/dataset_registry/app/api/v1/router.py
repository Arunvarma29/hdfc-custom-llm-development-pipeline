
from fastapi import APIRouter


from services.dataset_registry.app.api.v1.routes import datasets, health

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(datasets.router,prefix="/api/v1")