from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.orm import Session

from services.run_orchestrator.app.models.training_run import (
    TrainingRun,
    TrainingRunStatus,
)


class TrainingRunRepository:

    def create(
        self,
        db: Session,
        *,
        dataset_id: UUID,
        prepared_artifact_id: UUID,
        base_model: str,
        adaptation_type: str,
        config: dict,
    ):
        run = TrainingRun(
            dataset_id=dataset_id,
            prepared_artifact_id=prepared_artifact_id,
            base_model=base_model,
            adaptation_type=adaptation_type,
            config=config,
            status=TrainingRunStatus.QUEUED.value,
        )

        db.add(run)
        db.commit()
        db.refresh(run)

        return run

    def get_by_id(
        self,
        db: Session,
        run_id: UUID,
    ):
        return (
            db.query(TrainingRun)
            .filter(TrainingRun.id == run_id)
            .first()
        )

    def get_runs(
        self,
        db: Session,
        limit: int = 50,
    ):
        return (
            db.query(TrainingRun)
            .order_by(
                TrainingRun.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    def mark_running(
        self,
        db: Session,
        run: TrainingRun,
        total_steps: int,
    ):
        run.status = TrainingRunStatus.RUNNING.value
        run.current_step = 0
        run.total_steps = total_steps
        run.started_at = datetime.now(UTC)

        db.commit()
        db.refresh(run)

        return run

    def update_progress(
        self,
        db: Session,
        run: TrainingRun,
        *,
        current_step: int,
        metrics: dict | None = None,
        checkpoint: str | None = None,
    ):
        run.current_step = current_step

        if metrics is not None:
            run.metrics = metrics

        if checkpoint is not None:
            run.latest_checkpoint = checkpoint

        db.commit()
        db.refresh(run)

        return run

    def mark_completed(
        self,
        db: Session,
        run: TrainingRun,
        *,
        adapter_object_key: str,
        manifest_object_key: str,
        metrics: dict,
    ):
        run.status = TrainingRunStatus.COMPLETED.value
        run.current_step = run.total_steps
        run.adapter_object_key = adapter_object_key
        run.manifest_object_key = manifest_object_key
        run.metrics = metrics
        run.completed_at = datetime.now(UTC)

        db.commit()
        db.refresh(run)

        return run

    def mark_failed(
        self,
        db: Session,
        run: TrainingRun,
        error_message: str,
    ):
        run.status = TrainingRunStatus.FAILED.value
        run.error_message = error_message

        db.commit()
        db.refresh(run)

        return run

    def mark_cancelled(
        self,
        db: Session,
        run: TrainingRun,
    ):
        run.status = TrainingRunStatus.CANCELLED.value

        db.commit()
        db.refresh(run)

        return run