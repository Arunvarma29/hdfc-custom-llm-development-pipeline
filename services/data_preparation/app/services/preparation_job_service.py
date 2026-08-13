from uuid import UUID

from sqlalchemy.orm import Session

from services.data_preparation.app.models.preparation_job import (
    PreparationJob,
)
from services.data_preparation.app.repositories.preparation_job_repository import (
    PreparationJobRepository,
)


class PreparationJobService:

    def __init__(self):
        self.repository = PreparationJobRepository()

    def create_job(
        self,
        db: Session,
        dataset_id: UUID,
    ) -> PreparationJob:

        job = self.repository.create(
            db=db,
            dataset_id=dataset_id,
        )

        db.commit()
        db.refresh(job)

        return job