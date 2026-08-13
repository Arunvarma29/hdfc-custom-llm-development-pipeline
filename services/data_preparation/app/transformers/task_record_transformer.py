from typing import Any

from services.data_preparation.app.schemas.task_record import TaskRecord


def transform_record(
    record: dict[str, Any],
) -> dict[str, Any]:
    """
    Convert a prepared record into a typed task-record structure.
    Existing fields are preserved.
    """

    instruction = (
        record.get("instruction")
        or record.get("question")
        or record.get("complaint_text")
        or record.get("issue_type")
    )

    context = (
        record.get("context")
        or record.get("content")
    )

    response = (
        record.get("response")
        or record.get("answer")
    )

    label = (
        record.get("label")
        or record.get("status")
        or record.get("transaction_status")
    )

    transformed = {
        **record,
        "instruction": (
            str(instruction).strip()
            if instruction is not None
            else None
        ),
        "context": (
            str(context).strip()
            if context is not None
            else None
        ),
        "response": (
            str(response).strip()
            if response is not None
            else None
        ),
        "label": (
            str(label).strip()
            if label is not None
            else None
        ),
        "refusal": bool(
            record.get("refusal", False)
        ),
        "escalation": bool(
            record.get("escalation", False)
        ),
    }

    TaskRecord.model_validate(transformed)

    return transformed


def transform_records(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        transform_record(record)
        for record in records
    ]