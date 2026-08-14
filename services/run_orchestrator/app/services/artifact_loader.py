import json

import pyarrow.parquet as pq

from services.dataset_registry.app.storage.minio_client import (
    get_file,
)
from services.data_preparation.app.models.prepared_artifact import (
    PreparedArtifact,
)
from sqlalchemy.orm import Session


def load_training_records(
    db: Session,
    prepared_artifact: PreparedArtifact,
):
    if not prepared_artifact.train_object_key:
        raise ValueError(
            "Prepared artifact has no training object key."
        )

    file_stream = get_file(
        prepared_artifact.train_object_key
    )

    table = pq.read_table(file_stream)

    return table.to_pylist()


def load_manifest(
    prepared_artifact: PreparedArtifact,
):
    if not prepared_artifact.manifest_object_key:
        raise ValueError(
            "Prepared artifact has no manifest object key."
        )

    file_stream = get_file(
        prepared_artifact.manifest_object_key
    )

    data = file_stream.read()

    return json.loads(data.decode("utf-8"))