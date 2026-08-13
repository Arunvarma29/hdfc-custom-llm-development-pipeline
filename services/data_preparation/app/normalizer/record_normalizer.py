from typing import Any


def normalize_value(value: Any) -> Any:
    """
    Normalize an individual field value.
    """

    if isinstance(value, str):
        value = value.strip()

        if value == "":
            return None

        return value

    return value


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    """
    Normalize one dataset record.

    - Removes whitespace from column names.
    - Normalizes string values.
    - Converts empty strings to None.
    """

    normalized: dict[str, Any] = {}

    for key, value in record.items():

        normalized_key = key.strip()

        if not normalized_key:
            continue

        normalized[normalized_key] = normalize_value(value)

    return normalized


def normalize_records(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Normalize all dataset records.
    """

    return [
        normalize_record(record)
        for record in records
    ]