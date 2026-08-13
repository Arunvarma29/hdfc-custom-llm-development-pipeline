from io import BytesIO
from typing import Any


def parse_txt(
    file_stream: BytesIO,
    document_id: str = "document",
) -> list[dict[str, Any]]:
    """
    Parse a TXT file into one document record.
    """

    file_stream.seek(0)

    content = file_stream.read().decode(
        "utf-8",
        errors="replace",
    ).strip()

    if not content:
        return []

    return [
        {
            "document_id": document_id,
            "title": "Text Document",
            "content": content,
        }
    ]