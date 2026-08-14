from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AdaptationConfig(BaseModel):
    method: str = Field(
        min_length=1,
        max_length=20,
    )

    rank: int = Field(
        default=16,
        ge=1,
    )

    alpha: int = Field(
        default=32,
        ge=1,
    )

    dropout: float = Field(
        default=0.05,
        ge=0.0,
        le=1.0,
    )


class TrainingConfig(BaseModel):
    learning_rate: float = Field(
        default=0.0002,
        gt=0,
    )

    epochs: int = Field(
        default=3,
        ge=1,
    )

    batch_size: int = Field(
        default=4,
        ge=1,
    )

    seed: int = Field(
        default=42,
    )


class ComputeConfig(BaseModel):
    profile: str = Field(
        min_length=1,
        max_length=100,
    )


class EvaluationPlan(BaseModel):
    suite: str = Field(
        min_length=1,
        max_length=100,
    )


class TrainingRunCreate(BaseModel):
    dataset_id: UUID
    prepared_artifact_id: UUID
    dataset_version: str = Field(
        min_length=1,
        max_length=50,
    )

    base_model: str = Field(
        min_length=1,
        max_length=255,
    )

    adaptation: AdaptationConfig
    training: TrainingConfig
    compute: ComputeConfig
    evaluation_plan: EvaluationPlan


class TrainingRunResponse(BaseModel):
    id: UUID

    dataset_id: UUID
    prepared_artifact_id: UUID
    base_model: str
    adaptation_type: str
    status: str

    config: dict

    current_step: int
    total_steps: int

    latest_checkpoint: str | None
    adapter_object_key: str | None
    manifest_object_key: str | None

    metrics: dict | None
    error_message: str | None

    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    dataset_version: str | None = None

    model_config = ConfigDict(
        from_attributes=True
    )