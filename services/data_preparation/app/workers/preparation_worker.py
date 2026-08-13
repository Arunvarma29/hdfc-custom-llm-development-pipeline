from datetime import UTC, datetime

from services.database.app.session import SessionLocal

from services.dataset_registry.app.models.dataset import (
    Dataset,
    DatasetStatus,
)
from services.dataset_registry.app.storage.minio_client import get_file

from services.data_preparation.app.artifacts.prepared_artifact import (
    create_prepared_artifact,
)
from services.data_preparation.app.config.profile_selector import (
    get_profile,
)
from services.data_preparation.app.models.preparation_job import (
    PreparationJobStatus,
)
from services.data_preparation.app.parsers.parser_selector import (
    get_parser,
)
from services.data_preparation.app.quality.quality_checker import (
    run_quality_checks,
)
from services.data_preparation.app.normalizer.record_normalizer import (
    normalize_records,
)
from services.data_preparation.app.deidentification.deidentifier import (
    deidentify_records,
)
from services.data_preparation.app.deduplication.deduplicator import (
    deduplicate_records,
)
from services.data_preparation.app.repositories.preparation_job_repository import (
    PreparationJobRepository,
)
from services.data_preparation.app.splitters.dataset_splitter import (
    split_dataset,
)
from services.data_preparation.app.chunking.text_chunker import (
    chunk_document_records,
)

from services.data_preparation.app.models.prepared_artifact import (
    PreparedArtifact,
)

from services.data_preparation.app.models.preparation_quality_report import (
    PreparationQualityReport,
)

from services.data_preparation.app.transformers.task_record_transformer import (
    transform_records,
)





DOCUMENT_CONTENT_TYPES = {
    "text/plain",
    "application/pdf",
    "application/json",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


class PreparationWorker:

    def __init__(self):
        self.repository = PreparationJobRepository()

    def run_once(self, job_id=None) -> bool:
        db = SessionLocal()
        job = None
        dataset = None

        try:
            # 1. Get queued job
            if job_id:
                from uuid import UUID

                job = self.repository.get_by_id(
                    db,
                    UUID(str(job_id)),
                )

                if job is not None and job.status != PreparationJobStatus.QUEUED.value:
                    job = None
            else:
                job = self.repository.get_next_queued_job(db)

                

            if job is None:
                return False

            # 2. Mark RUNNING
            job.status = PreparationJobStatus.RUNNING.value
            job.started_at = datetime.now(UTC)
            job.attempts += 1

            db.commit()

            print(f"Processing preparation job: {job.id}")

            # 3. Load dataset
            dataset = db.get(
                Dataset,
                job.dataset_id,
            )

            if dataset is None:
                raise ValueError(
                    f"Dataset not found: {job.dataset_id}"
                )

            if dataset.is_deleted:
                raise ValueError("Dataset has been deleted")

            print(f"Loading dataset: {dataset.id}")

            

            # 4. Load source from MinIO
            file_stream = get_file(
                dataset.object_key
            )

            # 5. Select parser
            parser = get_parser(
                dataset.content_type
            )

            # 6. Parse
            if dataset.content_type in DOCUMENT_CONTENT_TYPES:
                raw_records = parser(
                    file_stream,
                    document_id=str(dataset.id),
                )
            else:
                raw_records = parser(
                    file_stream
                )

            print(
                f"Parsed records: {len(raw_records)}"
            )

            # 7. Normalize
            normalized_records = normalize_records(
                raw_records
            )

            print(
                f"Normalized records: "
                f"{len(normalized_records)}"
            )

            # 8. De-identify
            deidentified_records = deidentify_records(
                normalized_records
            )

            print(
                f"De-identified records: "
                f"{len(deidentified_records)}"
            )

            # 9. Chunk documents
            if any(
                "content" in record
                for record in deidentified_records
            ):
                deidentified_records = (
                    chunk_document_records(
                        deidentified_records,
                        chunk_size=1000,
                        chunk_overlap=100,
                    )
                )

                print(
                    f"Chunked records: "
                    f"{len(deidentified_records)}"
                )

            # 10. Deduplicate
            (
                unique_records,
                duplicate_count,
            ) = deduplicate_records(
                deidentified_records
            )

            print(
                f"Unique records: {len(unique_records)}"
            )
            print(
                f"Duplicate records: {duplicate_count}"
            )


            unique_records = transform_records(
                    unique_records
                )

            # 11. Get preparation profile

            profile = get_profile(
                            dataset_type=dataset.dataset_type,
                            content_type=dataset.content_type,
                        )

            # 12. Split
            (
                train_records,
                validation_records,
                test_records,
            ) = split_dataset(
                unique_records,
                seed=42,
                entity_field=profile.entity_field,
                time_field=profile.time_field,
            )

            print("Dataset split:")
            print(
                f"Training: {len(train_records)}"
            )
            print(
                f"Validation: {len(validation_records)}"
            )
            print(
                f"Test: {len(test_records)}"
            )

            
           
            print(
                f"Preparation profile: "
                f"{dataset.dataset_type}"
            )

            # 13. Quality gate
            quality_result = run_quality_checks(
                records=unique_records,
                train_records=train_records,
                validation_records=validation_records,
                test_records=test_records,
                required_fields=profile.required_fields,
                sensitive_fields=profile.sensitive_fields,
                duplicate_count=duplicate_count,
            )

            quality_report = PreparationQualityReport(
                preparation_job_id=job.id,
                status=quality_result["status"],
                checks=quality_result["checks"],
                failed_checks=quality_result["failed_checks"],
            )

            db.add(quality_report)
            db.flush()

            print(
                f"Quality Gate: "
                f"{quality_result['status']}"
            )

            if quality_result["failed_checks"]:
                for check in quality_result["failed_checks"]:
                    print(check)

                raise ValueError(
                    "Dataset quality gate failed: "
                    + ", ".join(
                        check["name"]
                        for check in quality_result[
                            "failed_checks"
                        ]
                    )
                )

            # 14. Create prepared artifacts
            manifest = create_prepared_artifact(
                dataset_id=str(dataset.id),
                dataset_version=dataset.version,
                train_records=train_records,
                validation_records=validation_records,
                test_records=test_records,
                source_object_key=dataset.object_key,
                duplicate_count=duplicate_count,
                split_seed=42,
                preparation_job_id=str(job.id),
            )

            print(
                "Prepared artifact created:"
            )

            artifact = PreparedArtifact(
                dataset_id=dataset.id,
                preparation_job_id=job.id,
                dataset_version=dataset.version,
                artifact_id=manifest["artifact_id"],
                train_object_key=manifest["artifacts"]["train"],
                validation_object_key=manifest["artifacts"]["validation"],
                test_object_key=manifest["artifacts"]["test"],
                manifest_object_key=manifest["artifacts"]["manifest"],
                train_record_count=manifest["record_counts"]["train"],
                validation_record_count=manifest["record_counts"]["validation"],
                test_record_count=manifest["record_counts"]["test"],
                duplicate_count=manifest["duplicate_count"],
            )

            db.add(artifact)
            db.flush()

            quality_report.prepared_artifact_id = artifact.id
            print(manifest["artifact_id"])

            # 15. Mark dataset READY
            dataset.status = DatasetStatus.READY.value

            # 16. Mark job COMPLETED
            job.status = (
                PreparationJobStatus.COMPLETED.value
            )
            job.completed_at = datetime.now(UTC)
            job.error_message = None

            db.commit()

            print(
                f"Preparation job completed: "
                f"{job.id}"
            )

            return True

        except Exception as exc:
            db.rollback()

            print(
                f"Preparation job failed: {exc}"
            )

            if dataset is not None:
                try:
                    dataset.status = DatasetStatus.UPLOADED.value
                    db.commit()
                except Exception:
                    db.rollback()

            if job is not None:
                try:
                    job.status = (
                        PreparationJobStatus.FAILED.value
                    )
                    job.error_message = str(exc)

                    db.commit()

                except Exception:
                    db.rollback()

            return False

        finally:
            db.close()