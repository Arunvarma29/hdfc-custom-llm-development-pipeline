from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from services.dataset_registry.app.models.dataset import (
    Dataset,
    DatasetStatus,
)
from services.data_preparation.app.models.prepared_artifact import (
    PreparedArtifact,
)

from services.run_orchestrator.app.repositories.training_run_repository import (
    TrainingRunRepository,
)

from services.run_orchestrator.app.workers.training_worker import (
            TrainingWorker,
)



class RunService:

    def __init__(self):
        self.repository = TrainingRunRepository()

    def create_run(
        self,
        db: Session,
        *,
        dataset_id: UUID,
        prepared_artifact_id: UUID,
        dataset_version: str,
        base_model: str,
        adaptation: dict,
        training: dict,
        compute: dict,
        evaluation_plan: dict,
    ):
        dataset = (
            db.query(Dataset)
            .filter(
                Dataset.id == dataset_id
            )
            .first()
        )

        if dataset is None:
            raise HTTPException(
                status_code=404,
                detail="Dataset not found.",
            )

        if dataset.status != DatasetStatus.APPROVED.value:
            raise HTTPException(
                status_code=409,
                detail=(
                    "Training is allowed only for "
                    f"APPROVED datasets. Current status: "
                    f"{dataset.status}."
                ),
            )

        if not dataset.is_frozen:
            raise HTTPException(
                status_code=409,
                detail=(
                    "Dataset must be frozen before "
                    "model development."
                ),
            )

        if dataset.version != dataset_version:
            raise HTTPException(
                status_code=409,
                detail=(
                    "Requested dataset version does not "
                    "match the approved dataset version."
                ),
            )

        if artifact.dataset_version != dataset.version:
            raise HTTPException(
            status_code=409,
            detail="Prepared artifact version does not match the approved dataset version.",
        )

        artifact = (
            db.query(PreparedArtifact)
            .filter(
                PreparedArtifact.id
                == prepared_artifact_id
            )
            .first()
        )

        if artifact is None:
            raise HTTPException(
                status_code=404,
                detail="Prepared artifact not found.",
            )

        if artifact.dataset_id != dataset.id:
            raise HTTPException(
                status_code=409,
                detail=(
                    "Prepared artifact does not belong "
                    "to the selected dataset."
                ),
            )

        method = adaptation["method"].lower()

        if method not in {"lora", "qlora"}:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Adaptation method must be "
                    "LoRA or QLoRA."
                ),
            )

        config = {
            "dataset_version": dataset_version,
            "adaptation": adaptation,
            "training": training,
            "compute": compute,
            "evaluation_plan": evaluation_plan,
        }

        return self.repository.create(
            db=db,
            dataset_id=dataset.id,
            prepared_artifact_id=artifact.id,
            base_model=base_model,
            adaptation_type=method,
            config=config,
        )

    def get_run(
        self,
        db: Session,
        run_id: UUID,
    ):
        run = self.repository.get_by_id(
            db=db,
            run_id=run_id,
        )

        if run is None:
            raise HTTPException(
                status_code=404,
                detail="Training run not found.",
            )

        return run

    def list_runs(
        self,
        db: Session,
    ):
        return self.repository.get_runs(
            db=db
        )

    def start_run(
        self,
        db: Session,
        run_id: UUID,
    ):
        run = self.repository.get_by_id(
            db=db,
            run_id=run_id,
        )

        if run is None:
            raise HTTPException(
                status_code=404,
                detail="Training run not found.",
            )

        if run.status != "QUEUED":
            raise HTTPException(
                status_code=409,
                detail=(
                    f"Run cannot be started from "
                    f"{run.status} state."
                ),
            )

        return TrainingWorker().run_once(
            db=db,
            run_id=run.id,
        )

    def cancel_run(
        self,
        db: Session,
        run_id: UUID,
    ):
        run = self.repository.get_by_id(
            db=db,
            run_id=run_id,
        )

        if run is None:
            raise HTTPException(
                status_code=404,
                detail="Training run not found.",
            )

        if run.status not in {
            "QUEUED",
            "RUNNING",
        }:
            raise HTTPException(
                status_code=409,
                detail=(
                    f"Run cannot be cancelled from "
                    f"{run.status} state."
                ),
            )

        return self.repository.mark_cancelled(
            db=db,
            run=run,
        )

    def resume_run(
        self,
        db: Session,
        run_id: UUID,
    ):
        run = self.repository.get_by_id(
            db=db,
            run_id=run_id,
        )

        if run is None:
            raise HTTPException(
                status_code=404,
                detail="Training run not found.",
            )

        if run.status != "FAILED":
            raise HTTPException(
                status_code=409,
                detail=(
                    "Only FAILED training runs "
                    "can be resumed."
                ),
            )

        run.status = "QUEUED"
        run.error_message = None

        db.commit()
        db.refresh(run)

        return run