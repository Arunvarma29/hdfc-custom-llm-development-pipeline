from pydantic import BaseModel, ConfigDict


class TaskRecord(BaseModel):
    instruction: str | None = None
    context: str | None = None
    response: str | None = None
    label: str | None = None
    refusal: bool = False
    escalation: bool = False

    model_config = ConfigDict(
        extra="allow",
    )