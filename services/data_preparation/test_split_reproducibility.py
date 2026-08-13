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

    unique_records, _ = deduplicate_records(
        deidentified_records
    )

    # First split
    train_1, validation_1, test_1 = split_dataset(
        unique_records,
        seed=42,
    )

    # Second split using the same input and seed
    train_2, validation_2, test_2 = split_dataset(
        unique_records,
        seed=42,
    )

    if train_1 != train_2:
        raise ValueError(
            "Training split is not reproducible"
        )

    if validation_1 != validation_2:
        raise ValueError(
            "Validation split is not reproducible"
        )

    if test_1 != test_2:
        raise ValueError(
            "Test split is not reproducible"
        )

    print("Training split: reproducible")
    print("Validation split: reproducible")
    print("Test split: reproducible")
    print("Seed: 42")
    print("Dataset split reproducibility successful")

finally:
    db.close()