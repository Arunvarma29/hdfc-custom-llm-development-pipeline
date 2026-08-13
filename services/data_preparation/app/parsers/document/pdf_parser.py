from io import BytesIO
from typing import Any


from pypdf import PdfReader


def parse_pdf(
    file_stream: BytesIO,
    document_id: str = "document",
) -> list[dict[str, Any]]:
    """
    Parse PDF pages into document records.

    All pages belong to the same document.
    Blank pages are ignored.
    """

    file_stream.seek(0)

    reader = PdfReader(file_stream)

    records: list[dict[str, Any]] = []

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):
        content = page.extract_text() or ""

        content = content.strip()

        # Ignore completely empty pages
        if not content:
            continue

        records.append(
            {
                "document_id": document_id,
                "page_number": page_number,
                "title": f"PDF Page {page_number}",
                "content": content,
            }
        )

    return records