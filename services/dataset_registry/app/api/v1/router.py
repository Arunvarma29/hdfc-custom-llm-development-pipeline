from fastapi import APIRouter

from services.dataset_registry.app.api.v1.routes import (
    auth,
    datasets,
    health,
    dashboard,
)


api_router = APIRouter()

api_router.include_router(
    health.router
)

api_router.include_router(
    datasets.router,
    prefix="/api/v1",
)

api_router.include_router(
    auth.router,
    prefix="/api/v1",
)

api_router.include_router(
    dashboard.router,
    prefix="/api/v1",
)