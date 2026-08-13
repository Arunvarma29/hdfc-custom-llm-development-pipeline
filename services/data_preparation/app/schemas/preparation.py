from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PreparationRequest(BaseModel):
    dataset_id: UUID


class PreparationJobResponse(BaseModel):
    id: UUID
    dataset_id: UUID
    status: str
    attempts: int
    started_at: datetime | None
    completed_at: datetime | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )