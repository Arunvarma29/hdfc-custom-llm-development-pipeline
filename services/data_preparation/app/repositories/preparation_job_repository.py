from uuid import UUID

from sqlalchemy.orm import Session

from services.data_preparation.app.models.preparation_job import (
    PreparationJob,
    PreparationJobStatus,
)


class PreparationJobRepository:

    def create(
        self,
        db: Session,
        dataset_id: UUID,
    ) -> PreparationJob:
        job = PreparationJob(
            dataset_id=dataset_id,
            status=PreparationJobStatus.QUEUED.value,
            attempts=0,
        )

        db.add(job)
        db.flush()

        return job

    def get_by_id(
        self,
        db: Session,
        job_id: UUID,
    ) -> PreparationJob | None:
        return db.get(
            PreparationJob,
            job_id,
        )

    def get_latest_for_dataset(
        self,
        db: Session,
        dataset_id: UUID,
    ) -> PreparationJob | None:
        return (
            db.query(PreparationJob)
            .filter(
                PreparationJob.dataset_id == dataset_id
            )
            .order_by(
                PreparationJob.created_at.desc()
            )
            .first()
        )

    def update_status(
        self,
        db: Session,
        job: PreparationJob,
        status: PreparationJobStatus,
    ) -> PreparationJob:
        job.status = status.value

        db.flush()

        return job

    def get_next_queued_job(
        self,
        db: Session,
    ) -> PreparationJob | None:
        return (
            db.query(PreparationJob)
            .filter(
                PreparationJob.status
                == PreparationJobStatus.QUEUED.value
            )
            .order_by(
                PreparationJob.created_at.asc()
            )
            .first()
        )