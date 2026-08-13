from io import BytesIO
from uuid import UUID

from sqlalchemy.orm import Session

from services.dataset_registry.app.models.dataset import Dataset
from services.dataset_registry.app.storage.minio_client import get_file


class PreparationService:

    def __init__(self):
        pass

    def load_source(
        self,
        db: Session,
        dataset_id: UUID,
    ) -> tuple[Dataset, BytesIO]:

        dataset = db.get(
            Dataset,
            dataset_id,
        )

        if dataset is None:
            raise ValueError("Dataset not found")

        if dataset.is_deleted:
            raise ValueError("Dataset not found")

        source_file = get_file(
            dataset.object_key
        )

        return dataset, source_file