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


DATASET_ID = "7b57728a-419f-4ccb-b60c-37eca2a71a97"


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
        split_dataset(unique_records)
    )

    print("Raw records:", len(raw_records))
    print(
        "Normalized records:",
        len(normalized_records),
    )
    print(
        "De-identified records:",
        len(deidentified_records),
    )
    print(
        "Unique records:",
        len(unique_records),
    )
    print(
        "Duplicate records:",
        duplicate_count,
    )

    print("\nDataset split:")
    print("Training:", len(train_records))
    print("Validation:", len(validation_records))
    print("Test:", len(test_records))

    total_split_records = (
        len(train_records)
        + len(validation_records)
        + len(test_records)
    )

    if total_split_records != len(unique_records):
        raise ValueError(
            "Split record count does not match "
            "unique record count"
        )

    print(
        "\nTotal split records:",
        total_split_records,
    )

    print("Dataset splitting successful")

finally:
    db.close()