import json
from io import BytesIO

from services.database.app.session import SessionLocal

from services.dataset_registry.app.models.dataset import Dataset
from services.dataset_registry.app.storage.minio_client import get_file

from services.data_preparation.app.parsers.tabular.xlsx_parser import parse_xlsx
from services.data_preparation.app.normalizer.record_normalizer import (
    normalize_records,
)
from services.data_preparation.app.deidentification.deidentifier import (
    deidentify_records,
)
from services.data_preparation.app.deduplication.deduplicator import (
    deduplicate_records,
)
from services.data_preparation.app.splitters.dataset_splitter import (
    split_dataset,
)
from services.data_preparation.app.quality.quality_checker import (
    run_quality_checks,
)
from services.data_preparation.app.artifacts.prepared_artifact import (
    create_prepared_artifact,
    client,
)
from services.database.app.config import settings


DATASET_ID = "7b57728a-419f-4ccb-b60c-37eca2a71a97"


db = SessionLocal()

try:
    dataset = db.get(
        Dataset,
        DATASET_ID,
    )

    if dataset is None:
        raise ValueError(
            "Dataset not found"
        )

    file_stream = get_file(
        dataset.object_key
    )

    raw_records = parse_xlsx(
        file_stream
    )

    normalized_records = normalize_records(
        raw_records
    )

    deidentified_records = (
        deidentify_records(
            normalized_records
        )
    )

    unique_records, duplicate_count = (
        deduplicate_records(
            deidentified_records
        )
    )

    (
        train_records,
        validation_records,
        test_records,
    ) = split_dataset(
        unique_records,
        seed=42,
    )

    quality_result = run_quality_checks(
        records=unique_records,
        train_records=train_records,
        validation_records=validation_records,
        test_records=test_records,
        required_fields={
            "card_number",
            "customer_id",
            "debit_card_type",
            "card_network",
            "card_status",
        },
        sensitive_fields={
            "card_number",
            "customer_id",
        },
        duplicate_count=duplicate_count,
    )

    if quality_result["status"] != "PASS":
        raise ValueError(
            "Quality gate failed"
        )

    manifest = create_prepared_artifact(
        dataset_id=str(dataset.id),
        dataset_version=dataset.version,
        train_records=train_records,
        validation_records=validation_records,
        test_records=test_records,
        source_object_key=dataset.object_key,
        duplicate_count=duplicate_count,
        split_seed=42,
    )

    print(
        "Prepared artifact created successfully"
    )

    print(
        json.dumps(
            manifest,
            indent=2,
        )
    )

finally:
    db.close()