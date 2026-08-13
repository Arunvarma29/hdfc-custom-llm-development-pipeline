from uuid import UUID

from pydantic import BaseModel


class DatasetGovernanceResponse(BaseModel):
    dataset_id: UUID
    dataset_name: str
    dataset_version: str
    dataset_status: str

    preparation_job_id: UUID | None
    preparation_status: str | None

    file_name: str
    dataset_type: str
    domain: str