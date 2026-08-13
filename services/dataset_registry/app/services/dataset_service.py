from uuid import UUID
import math
from fastapi import UploadFile
from sqlalchemy.orm import Session
from datetime import UTC, datetime
from fastapi import HTTPException
from packages.observability.logging import setup_logger
from services.dataset_registry.app.exceptions.dataset import (
    DatasetAlreadyExistsException,
    DatasetNotFoundException,
)

from services.dataset_registry.app.models.dataset import DatasetStatus

from services.dataset_registry.app.repositories.dataset_repository import DatasetRepository
from services.dataset_registry.app.schemas.dataset import DatasetCreate
from services.dataset_registry.app.storage.minio_client import (
    delete_file,
    upload_file,
    get_file
)
from services.dataset_registry.app.utils.file_validation import validate_file
from services.dataset_registry.app.schemas.common import DatasetQueryParams
from services.data_preparation.app.repositories.preparation_job_repository import (
    PreparationJobRepository,
)

from services.data_preparation.app.models.preparation_job import (
    PreparationJob,
)
from services.data_preparation.app.models.prepared_artifact import PreparedArtifact
from services.data_preparation.app.models.preparation_quality_report import (
    PreparationQualityReport,
)

from services.data_preparation.app.workers.preparation_worker import (
        PreparationWorker,
    )

from services.data_preparation.app.models.preparation_quality_report import (
    PreparationQualityReport,
)



logger = setup_logger(__name__)


class DatasetService:
    def __init__(self):
        self.repository = DatasetRepository()
        self.preparation_job_repository = PreparationJobRepository()

    def create_dataset(
        self,
        db: Session,
        dataset: DatasetCreate,
        file: UploadFile,
    ):
        # Check duplicate dataset
        existing = self.repository.exists(
            db=db,
            name=dataset.name.strip(),
            version=dataset.version.strip(),
        )

        if existing:
            logger.warning(
                "Duplicate dataset upload attempted: %s (version %s)",
                dataset.name,
                dataset.version,
            )
            raise DatasetAlreadyExistsException()

        # Validate uploaded file
        file_info = validate_file(
            file=file,
            dataset_type=dataset.dataset_type.value,
        )
        # Upload file to MinIO
        object_key, file_size = upload_file(file)

        # Save metadata in PostgreSQL
       
        try:
            db_dataset = self.repository.create(
            db=db,
            dataset=dataset,
            file_name=file.filename,
            object_key=object_key,
            file_size=file_size,
            content_type=file_info["content_type"],
        )

        except Exception as exc:
            logger.exception(
            "Database save failed. Rolling back uploaded object: %s",
                object_key,
            )

            delete_file(object_key)

            raise exc
        logger.info(
            "Dataset uploaded successfully | id=%s | object_key=%s",
            db_dataset.id,
            object_key,
        )

        return db_dataset




    def list_datasets(
        self,
        db: Session,
        params: DatasetQueryParams,
    ):
        items, total = self.repository.get_datasets(
        db=db,
        params=params,
        )

        total_pages = math.ceil(total / params.limit) if total else 1

        return {
            "items": items,
            "pagination": {
            "page": params.page,
            "limit": params.limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": params.page < total_pages,
            "has_previous": params.page > 1,
        },
    }




    def get_dataset(
        self,
        db: Session,
        dataset_id: UUID,
    ):
        dataset = self.repository.get_by_id(
            db=db,
            dataset_id=dataset_id,
        )

        if dataset is None:
            logger.warning(
                "Dataset not found | id=%s",
                dataset_id,
            )
            raise DatasetNotFoundException()

        return dataset




    def prepare_dataset(
            self,
            db: Session,
            dataset_id: UUID,
        ):
            dataset = self.get_dataset(
            db=db,
            dataset_id=dataset_id,
        )

            if dataset.is_frozen:

                raise HTTPException(
                        status_code=409,
                        detail="Frozen dataset versions cannot be prepared again.",
                    )

            if dataset.is_deleted:
                raise DatasetNotFoundException()

            if dataset.status != DatasetStatus.UPLOADED.value:
        
                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"Dataset cannot be prepared. "
                        f"Current status: {dataset.status}"
                    ),
                )

    # Move dataset into preparation state
            dataset.status = DatasetStatus.PREPARING.value

    # Create a preparation job
            job = self.preparation_job_repository.create(
                db=db,
                dataset_id=dataset.id,
        )

    # Commit both changes together
            db.commit()

            db.refresh(dataset)
            db.refresh(job)

            logger.info(
                "Dataset preparation job queued | dataset_id=%s | job_id=%s",
                dataset.id,
                job.id,
        )

            return {
                "dataset_id": str(dataset.id),
                "job_id": str(job.id),
                "status": dataset.status,
                "job_status": job.status,
                "message": "Dataset preparation job queued",
            }




    def get_preparation(
        self,
        db: Session,
        dataset_id: UUID,
    ):
        # Make sure dataset exists
        self.get_dataset(
            db=db,
            dataset_id=dataset_id,
        )

        job = self.preparation_job_repository.get_latest_for_dataset(
            db=db,
            dataset_id=dataset_id,
        )

        if job is None:
            from fastapi import HTTPException

            raise HTTPException(
                status_code=404,
                detail="No preparation job found for this dataset",
            )

        return job




    def approve_dataset(
        self,
        db: Session,
        dataset_id: UUID,
        reviewer_name: str,
        review_comment: str | None = None,
    ):
        dataset = self.get_dataset(
            db=db,
            dataset_id=dataset_id,
        )

        if dataset.is_frozen:
            raise HTTPException(
                    status_code=409,
                    detail="Frozen dataset versions cannot be approved again.",
            )

        if dataset.status != DatasetStatus.READY.value:

            raise HTTPException(
                status_code=409,
                detail=(
                    f"Dataset cannot be approved. "
                    f"Current status: {dataset.status}. "
                    f"Dataset must be READY before approval."
                ),
            )

        dataset = self.repository.update_status(
            db=db,
            dataset=dataset,
            status=DatasetStatus.APPROVED.value,
        )

        dataset.is_frozen = True
        dataset.frozen_at = datetime.now(UTC)

        dataset.reviewer_name = reviewer_name
        dataset.review_comment = review_comment
        dataset.reviewed_at = datetime.now(UTC)

        db.commit()
        db.refresh(dataset)

        logger.info(
            "Dataset approved | id=%s",
            dataset.id,
        )

        return dataset




    def reject_dataset(
            self,
            db: Session,
            dataset_id: UUID,
            reviewer_name: str,
            review_comment: str | None = None,
        ):
            dataset = self.get_dataset(
            db=db,
            dataset_id=dataset_id,
            )

            if dataset.is_frozen:
                raise HTTPException(
                        status_code=409,
                        detail="Frozen dataset versions cannot be rejected.",
                    )

            if dataset.status != DatasetStatus.READY.value:
               
                raise HTTPException(
                    status_code=409,
                    detail=(
                    f"Dataset cannot be rejected. "
                    f"Current status: {dataset.status}"
                ),
            )

            dataset.status = DatasetStatus.REJECTED.value

            dataset.reviewer_name = reviewer_name
            dataset.review_comment = review_comment
            dataset.reviewed_at = datetime.now(UTC)

            dataset.status = DatasetStatus.REJECTED.value

            db.commit()
            db.refresh(dataset)

            logger.info(
            "Dataset rejected | id=%s",
            dataset.id,
        )

            return dataset
    



    def delete_dataset(
        self,
        db: Session,
        dataset_id: UUID,
    ):
        dataset = self.get_dataset(
            db=db,
            dataset_id=dataset_id,
        )

        if dataset.is_frozen:
            raise HTTPException(
                    status_code=409,
                    detail="Frozen dataset versions cannot be deleted.",
            )

        # delete_file(dataset.object_key)

        self.repository.delete(
            db=db,
            dataset=dataset,
        )

        logger.info(
            "Dataset deleted | id=%s | object_key=%s",
            dataset.id,
            dataset.object_key,
        )





    def download_dataset(
        self,
        db: Session,
        dataset_id: UUID,
    ):
        dataset = self.get_dataset(
        db=db,
        dataset_id=dataset_id,
    )

        file_stream = get_file(
            dataset.object_key,
    )

        return file_stream, dataset




    def get_governance_data(
    self,
    db: Session,
    dataset_id: UUID,
):
        dataset = self.get_dataset(
            db=db,
            dataset_id=dataset_id,
    )

        preparation_job = (
        self.preparation_job_repository
        .get_latest_for_dataset(
            db=db,
            dataset_id=dataset.id,
        )
    )

        return {
            "dataset_id": dataset.id,
            "dataset_name": dataset.name,
            "dataset_version": dataset.version,
            "dataset_status": dataset.status,

            "preparation_job_id": (
                preparation_job.id
                if preparation_job
                else None
        ),

            "preparation_status": (
                preparation_job.status
                if preparation_job
                else None
         ),

            "file_name": dataset.file_name,
            "dataset_type": dataset.dataset_type,
            "domain": dataset.domain,
    }



    def get_quality_report(
        self,
        db: Session,
        dataset_id: UUID,
):
        self.get_dataset(
        db=db,
        dataset_id=dataset_id,
    )

        return (
            db.query(PreparationQualityReport)
            .join(
                PreparationJob,
                PreparationQualityReport.preparation_job_id
            == PreparationJob.id,
        )
        .filter(
                PreparationJob.dataset_id == dataset_id
        )
        .order_by(
            PreparationQualityReport.created_at.desc()
        )
        .first()
    )


    def get_prepared_artifact(
        self,
        db: Session,
        dataset_id: UUID,
    ):
        self.get_dataset(db=db, dataset_id=dataset_id)

        return (
            db.query(PreparedArtifact)
            .filter(
            PreparedArtifact.dataset_id == dataset_id
            )
            .order_by(
            PreparedArtifact.created_at.desc()
            )
            .first()
     )



    def run_preparation(
        self,
        db: Session,
        dataset_id: UUID,
    ):
        dataset = self.get_dataset(
        db=db,
        dataset_id=dataset_id,
    )

        if dataset.is_frozen:
            raise HTTPException(
            status_code=409,
            detail="Frozen dataset cannot be prepared.",
        )

        job = (
            self.preparation_job_repository
            .get_latest_for_dataset(
            db=db,
            dataset_id=dataset.id,
        )
    )

        if job is None:
            raise HTTPException(
                status_code=404,
                detail="No preparation job found.",
            )

        if job.status != "QUEUED":
            raise HTTPException(
                status_code=409,
                detail=f"Preparation job is {job.status}.",
            )

   

        return {
            "job_id": str(job.id),
            "status": "STARTING",
            "result": PreparationWorker().run_once(job.id),
        }



    def run_quality_check(
        self,
        db: Session,
        dataset_id: UUID,
    ):
        dataset = self.get_dataset(
            db=db,
            dataset_id=dataset_id,
        )

        job = (
            self.preparation_job_repository
            .get_latest_for_dataset(
            db=db,
            dataset_id=dataset.id,
        )
    )

        if job is None:
            raise HTTPException(
                status_code=404,
                detail="No preparation job found for this dataset.",
            )

        if job.status != "COMPLETED":
            raise HTTPException(
                status_code=409,
                detail=(
                    "Quality check is available only after "
                    f"preparation completes. Current status: {job.status}."
                ),
            )

        report = (
            db.query(PreparationQualityReport)
            .filter(
                PreparationQualityReport.preparation_job_id
                == job.id
            )
            .order_by(
                PreparationQualityReport.created_at.desc()
            )
            .first()
        )

        if report is None:
            raise HTTPException(
                status_code=404,
                detail="No quality report found for the completed preparation job.",
            )

        return {
            "dataset_id": str(dataset.id),
            "job_id": str(job.id),
            "status": report.status,
            "checks": report.checks,
            "failed_checks": report.failed_checks,
            "created_at": report.created_at,
        }