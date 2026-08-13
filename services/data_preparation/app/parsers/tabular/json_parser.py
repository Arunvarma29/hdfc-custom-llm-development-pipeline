import json
from io import BytesIO
from typing import Any


def parse_json(
    file_stream: BytesIO,
    document_id: str = "document",
) -> list[dict[str, Any]]:
    """
    Parse JSON into normalized records.

    Supports:
    - Object
    - Array of objects
    - Document-style object containing content
    """

    file_stream.seek(0)

    data = json.load(file_stream)

    # -----------------------------------------
    # Document-style JSON
    # -----------------------------------------

    if isinstance(data, dict) and "content" in data:

        content = data.get("content")

        if content is None:
            return []

        return [
            {
                "document_id": data.get(
                    "document_id",
                    document_id,
                ),
                "title": data.get(
                    "title",
                    "JSON Document",
                ),
                "content": str(content).strip(),
            }
        ]

    # -----------------------------------------
    # Single structured record
    # -----------------------------------------

    if isinstance(data, dict):
        return [data]

    # -----------------------------------------
    # Structured records
    # -----------------------------------------

    if isinstance(data, list):

        records = []

        for item in data:

            if not isinstance(item, dict):
                raise ValueError(
                    "JSON array must contain objects."
                )

            records.append(item)

        return records

    raise ValueError(
        "JSON must contain an object "
        "or an array of objects."
    )