from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services.dataset_registry.app.api.dependencies import get_db

from services.run_orchestrator.app.schemas.training_run import (
    TrainingRunCreate,
    TrainingRunResponse,
)

from services.run_orchestrator.app.services.run_service import (
    RunService,
)


router = APIRouter(
    prefix="/runs",
    tags=["Runs"],
)

service = RunService()


@router.post(
    "",
    response_model=TrainingRunResponse,
    status_code=201,
)
def create_run(
    payload: TrainingRunCreate,
    db: Session = Depends(get_db),
):
    return service.create_run(
        db=db,
        dataset_id=payload.dataset_id,
        prepared_artifact_id=payload.prepared_artifact_id,
        dataset_version=payload.dataset_version,
        base_model=payload.base_model,
        adaptation=payload.adaptation.model_dump(),
        training=payload.training.model_dump(),
        compute=payload.compute.model_dump(),
        evaluation_plan=payload.evaluation_plan.model_dump(),
    )


@router.get(
    "",
    response_model=list[TrainingRunResponse],
)
def list_runs(
    db: Session = Depends(get_db),
):
    return service.list_runs(
        db=db
    )



@router.get(
    "/{run_id}",
    response_model=TrainingRunResponse,
)
def get_run(
    run_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_run(
        db=db,
        run_id=run_id,
    )



@router.post(
    "/{run_id}/start",
    response_model=TrainingRunResponse,
)
def start_run(
    run_id: UUID,
    db: Session = Depends(get_db),
):
    return service.start_run(
        db=db,
        run_id=run_id,
    )



@router.post(
    "/{run_id}/cancel",
    response_model=TrainingRunResponse,
)
def cancel_run(
    run_id: UUID,
    db: Session = Depends(get_db),
):
    return service.cancel_run(
        db=db,
        run_id=run_id,
    )



@router.post(
    "/{run_id}/resume",
    response_model=TrainingRunResponse,
)
def resume_run(
    run_id: UUID,
    db: Session = Depends(get_db),
):
    return service.resume_run(
        db=db,
        run_id=run_id,
    )