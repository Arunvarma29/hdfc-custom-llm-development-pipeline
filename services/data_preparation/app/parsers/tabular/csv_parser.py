from io import BytesIO
from typing import Any
import csv
import io


def parse_csv(
    file_stream: BytesIO,
) -> list[dict[str, Any]]:
    """
    Parse CSV into a list of records.
    """

    file_stream.seek(0)

    text_stream = io.TextIOWrapper(
        file_stream,
        encoding="utf-8-sig",
        newline="",
    )

    try:
        reader = csv.DictReader(text_stream)

        records: list[dict[str, Any]] = []

        for row in reader:
            records.append(dict(row))

        return records

    finally:
        text_stream.detach()