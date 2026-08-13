import hashlib
import re
from typing import Any


SENSITIVE_FIELDS = {
    "card_number": "CARD",
    "customer_id": "CUSTOMER",
    "customer_name": "CUSTOMER_NAME",
    "customer_contact": "CUSTOMER_CONTACT",
}


PHONE_PATTERN = re.compile(
    r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"
)

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+"
    r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)


def deterministic_token(
    value: Any,
    prefix: str,
) -> str:

    if value is None:
        return None

    raw_value = str(value).encode("utf-8")

    digest = hashlib.sha256(
        raw_value
    ).hexdigest()[:16]

    return f"{prefix}_{digest}"


def deidentify_text(
    text: str,
) -> str:

    if not text:
        return text

    def replace_phone(match):
        return deterministic_token(
            match.group(),
            "PHONE",
        )

    def replace_email(match):
        return deterministic_token(
            match.group(),
            "EMAIL",
        )

    text = PHONE_PATTERN.sub(
        replace_phone,
        text,
    )

    text = EMAIL_PATTERN.sub(
        replace_email,
        text,
    )

    return text


def deidentify_record(
    record: dict[str, Any],
) -> dict[str, Any]:

    result = record.copy()

    for field_name, prefix in SENSITIVE_FIELDS.items():

        if field_name not in result:
            continue

        value = result[field_name]

        if value is None:
            continue

        result[field_name] = deterministic_token(
            value=value,
            prefix=prefix,
        )

    # Document/text datasets
    if "content" in result:
        result["content"] = deidentify_text(
            str(result["content"])
        )

    return result


def deidentify_records(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:

    return [
        deidentify_record(record)
        for record in records
    ]