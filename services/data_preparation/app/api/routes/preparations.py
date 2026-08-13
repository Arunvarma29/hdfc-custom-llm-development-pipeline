from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services.data_preparation.app.api.dependencies import get_db
from services.data_preparation.app.schemas.preparation import (
    PreparationRequest,
)
from services.data_preparation.app.services.preparation_job_service import (
    PreparationJobService,
)


router = APIRouter(
    prefix="/api/v1/preparations",
    tags=["Data Preparation"],
)


job_service = PreparationJobService()


@router.post("")
def create_preparation(
    request: PreparationRequest,
    db: Session = Depends(get_db),
):
    job = job_service.create_job(
        db=db,
        dataset_id=request.dataset_id,
    )

    return {
        "dataset_id": str(job.dataset_id),
        "job_id": str(job.id),
        "status": "PREPARING",
        "job_status": job.status,
        "message": "Dataset preparation job queued",
    }