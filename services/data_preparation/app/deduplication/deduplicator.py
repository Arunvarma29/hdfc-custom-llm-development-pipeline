import hashlib
import json
from typing import Any


def record_fingerprint(
    record: dict[str, Any],
) -> str:
    """
    Generate a deterministic fingerprint for a record.

    For document chunks, fingerprint the actual content
    instead of metadata such as chunk_id.
    """

    if "content" in record:
        canonical_value = str(
            record["content"]
        ).strip()
    else:
        canonical_value = json.dumps(
            record,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )

    return hashlib.sha256(
        canonical_value.encode("utf-8")
    ).hexdigest()


def deduplicate_records(
    records: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    """
    Remove exact duplicate records.

    Returns:
        unique_records
        duplicate_count
    """

    seen: set[str] = set()
    unique_records: list[dict[str, Any]] = []
    duplicate_count = 0

    for record in records:
        fingerprint = record_fingerprint(record)

        if fingerprint in seen:
            duplicate_count += 1
            continue

        seen.add(fingerprint)
        unique_records.append(record)

    return unique_records, duplicate_count