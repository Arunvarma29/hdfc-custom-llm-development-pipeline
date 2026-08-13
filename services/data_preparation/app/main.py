from fastapi import FastAPI

# Register all models used by this service
from services.dataset_registry.app.models import Dataset
from services.data_preparation.app.models.preparation_job import (
    PreparationJob,
    PreparationJobStatus
)

from services.data_preparation.app.api.routes import preparations


app = FastAPI()

app.include_router(
    preparations.router
)