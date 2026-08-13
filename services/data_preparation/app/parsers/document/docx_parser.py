from io import BytesIO
from typing import Any

from docx import Document


def parse_docx(
    file_stream: BytesIO,
    document_id: str = "document",
) -> list[dict[str, Any]]:
    """
    Parse DOCX paragraphs into one document record.
    """

    file_stream.seek(0)

    document = Document(file_stream)

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    content = "\n".join(paragraphs)

    if not content:
        return []

    return [
        {
            "document_id": document_id,
            "title": "Word Document",
            "content": content,
        }
    ]