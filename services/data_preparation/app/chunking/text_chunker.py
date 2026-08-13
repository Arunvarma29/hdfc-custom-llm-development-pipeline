from typing import Any


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
) -> list[str]:
    """
    Split text into overlapping character-based chunks.
    """

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0"
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative"
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    chunks: list[str] = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(
            start + chunk_size,
            text_length,
        )

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - chunk_overlap

    return chunks


def chunk_document_records(
    records: list[dict[str, Any]],
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
) -> list[dict[str, Any]]:

    chunked_records: list[dict[str, Any]] = []

    for record in records:

        content = record.get("content")

        if not content:
            continue

        chunks = chunk_text(
            str(content),
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):
            chunked_records.append(
                {
                    **record,
                    "chunk_id": (
                        f"{record.get('document_id', 'document')}"
                        f"_chunk_{index}"
                    ),
                    "chunk_index": index,
                    "content": chunk,
                }
            )

    return chunked_records