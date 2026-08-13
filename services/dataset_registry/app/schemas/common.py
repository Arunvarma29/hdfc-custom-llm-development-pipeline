from typing import Literal

from pydantic import BaseModel, Field

from pydantic import BaseModel

from services.dataset_registry.app.schemas.dataset import DatasetResponse


class DatasetQueryParams(BaseModel):
    page: int = Field(default=1, ge=1)

    limit: int = Field(default=10, ge=1, le=100)

    search: str | None = None

    dataset_type: str | None = None

    status: str | None = None

    domain: str | None = None

    sort_by: Literal[
        "created_at",
        "name",
        "version",
    ] = "created_at"

    order: Literal[
        "asc",
        "desc",
    ] = "desc"



class PaginationMetadata(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool


class DatasetListResponse(BaseModel):
    items: list[DatasetResponse]
    pagination: PaginationMetadata