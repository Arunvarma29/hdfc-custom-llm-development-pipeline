from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.dataset_registry.app.api.v1.router import api_router
from services.database.app.config import settings
from services.dataset_registry.app.storage.minio_client import create_bucket_if_not_exists
from services.dataset_registry.app.exceptions import register_exception_handlers

from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create MinIO bucket if it doesn't exist
    create_bucket_if_not_exists()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


register_exception_handlers(app)

app.include_router(api_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "HDFC Bank Custom LLM Development Pipeline",
        "service": "Dataset Registry",
        "status": "running",
        "environment": settings.app_env,
    }