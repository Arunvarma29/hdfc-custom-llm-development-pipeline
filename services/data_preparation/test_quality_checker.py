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


DATASET_ID = "7b57728a-419f-4ccb-b60c-37eca2a71a97"

REQUIRED_FIELDS = {
    "card_number",
    "customer_id",
    "debit_card_type",
    "card_network",
    "card_status",
}

SENSITIVE_FIELDS = {
    "card_number",
    "customer_id",
}


db = SessionLocal()

try:
    dataset = db.get(Dataset, DATASET_ID)

    if dataset is None:
        raise ValueError("Dataset not found")

    file_stream = get_file(dataset.object_key)

    raw_records = parse_xlsx(file_stream)

    normalized_records = normalize_records(
        raw_records
    )

    deidentified_records = deidentify_records(
        normalized_records
    )

    unique_records, duplicate_count = (
        deduplicate_records(
            deidentified_records
        )
    )

    train_records, validation_records, test_records = (
        split_dataset(
            unique_records,
            seed=42,
        )
    )

    result = run_quality_checks(
        records=unique_records,
        train_records=train_records,
        validation_records=validation_records,
        test_records=test_records,
        required_fields=REQUIRED_FIELDS,
        sensitive_fields=SENSITIVE_FIELDS,
        duplicate_count=duplicate_count,
    )

    print("Quality Gate:", result["status"])

    print("\nChecks:")

    for check in result["checks"]:
        print(
            f"- {check['name']}: "
            f"{check['status']}"
        )

    if result["failed_checks"]:
        print("\nFailed checks:")

        for check in result["failed_checks"]:
            print(check)

        raise ValueError(
            "Data quality gate failed"
        )

    print("\nData quality checks successful")

finally:
    db.close()