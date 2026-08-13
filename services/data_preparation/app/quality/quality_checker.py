from typing import Any
import re


def check_record_count(
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    count = len(records)

    return {
        "name": "record_count",
        "status": "PASS" if count > 0 else "FAIL",
        "count": count,
    }


def check_required_fields(
    records: list[dict[str, Any]],
    required_fields: set[str],
) -> dict[str, Any]:
    if not records:
        return {
            "name": "required_fields",
            "status": "FAIL",
            "missing_fields": list(required_fields),
        }

    available_fields = set(records[0].keys())

    missing_fields = sorted(
        required_fields - available_fields
    )

    return {
        "name": "required_fields",
        "status": (
            "PASS"
            if not missing_fields
            else "FAIL"
        ),
        "missing_fields": missing_fields,
    }


def check_schema_consistency(
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    if not records:
        return {
            "name": "schema_consistency",
            "status": "FAIL",
        }

    expected_fields = set(records[0].keys())

    inconsistent_records = 0

    for record in records[1:]:
        if set(record.keys()) != expected_fields:
            inconsistent_records += 1

    return {
        "name": "schema_consistency",
        "status": (
            "PASS"
            if inconsistent_records == 0
            else "FAIL"
        ),
        "inconsistent_records": inconsistent_records,
    }



def check_empty_values(
    records: list[dict[str, Any]],
    required_fields: set[str],
) -> dict[str, Any]:

    empty_counts: dict[str, int] = {}

    for field in required_fields:
        count = sum(
            1
            for record in records
            if record.get(field) is None
            or str(record.get(field)).strip() == ""
        )

        if count > 0:
            empty_counts[field] = count

    return {
        "name": "empty_values",
        "status": (
            "PASS"
            if not empty_counts
            else "FAIL"
        ),
        "empty_counts": empty_counts,
    }




def check_split_integrity(
    total_records: int,
    train_records: list[dict[str, Any]],
    validation_records: list[dict[str, Any]],
    test_records: list[dict[str, Any]],
) -> dict[str, Any]:

    split_total = (
        len(train_records)
        + len(validation_records)
        + len(test_records)
    )

    if split_total != total_records:
        return {
            "name": "split_integrity",
            "status": "FAIL",
            "total_records": total_records,
            "split_total": split_total,
            "document_overlap": [],
        }

    train_documents = {
        str(record["document_id"])
        for record in train_records
        if "document_id" in record
    }

    validation_documents = {
        str(record["document_id"])
        for record in validation_records
        if "document_id" in record
    }

    test_documents = {
        str(record["document_id"])
        for record in test_records
        if "document_id" in record
    }

    overlap = (
        (train_documents & validation_documents)
        | (train_documents & test_documents)
        | (validation_documents & test_documents)
    )

    return {
        "name": "split_integrity",
        "status": (
            "PASS"
            if not overlap
            else "FAIL"
        ),
        "total_records": total_records,
        "split_total": split_total,
        "document_overlap": sorted(overlap),
    }




def check_duplicate_integrity(
    unique_records: list[dict[str, Any]],
    duplicate_count: int,
) -> dict[str, Any]:
    return {
        "name": "duplicate_integrity",
        "status": (
            "PASS"
            if len(unique_records) + duplicate_count
            >= len(unique_records)
            else "FAIL"
        ),
        "unique_records": len(unique_records),
        "duplicate_count": duplicate_count,
    }




PHONE_PATTERN = re.compile(
    r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"
)

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+"
    r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)



def check_sensitive_fields(
    records: list[dict[str, Any]],
    sensitive_fields: set[str],
) -> dict[str, Any]:

    violations: list[str] = []

    prefixes = {
        "card_number": "CARD_",
        "customer_id": "CUSTOMER_",
        "customer_name": "CUSTOMER_NAME_",
        "customer_contact": "CUSTOMER_CONTACT_",
    }

    for field in sensitive_fields:

        expected_prefix = prefixes.get(field)

        if not expected_prefix:
            continue

        for index, record in enumerate(records):

            value = record.get(field)

            if value is None:
                continue

            if not str(value).startswith(
                expected_prefix
            ):
                violations.append(
                    f"{field} at record {index}"
                )

    # Check de-identified document text
    for index, record in enumerate(records):

        content = record.get("content")

        if content is None:
            continue

        content = str(content)

        if PHONE_PATTERN.search(content):
            violations.append(
                f"phone number at record {index}"
            )

        if EMAIL_PATTERN.search(content):
            violations.append(
                f"email address at record {index}"
            )

    return {
        "name": "privacy_check",
        "status": (
            "PASS"
            if not violations
            else "FAIL"
        ),
        "violations": violations,
    }


def check_length_statistics(
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    lengths: list[int] = []

    for record in records:
        for value in record.values():
            if isinstance(value, str) and value.strip():
                lengths.append(len(value))

    if not lengths:
        return {
            "name": "length_statistics",
            "status": "PASS",
            "min_length": 0,
            "max_length": 0,
            "average_length": 0,
        }

    average_length = sum(lengths) / len(lengths)

    return {
        "name": "length_statistics",
        "status": "PASS",
        "min_length": min(lengths),
        "max_length": max(lengths),
        "average_length": round(average_length, 2),
    }


def check_anomalous_records(
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    anomalies: list[int] = []

    for index, record in enumerate(records):
        if not record:
            anomalies.append(index)
            continue

        if all(
            value is None
            or str(value).strip() == ""
            for value in record.values()
        ):
            anomalies.append(index)

    return {
        "name": "anomalous_records",
        "status": (
            "PASS"
            if not anomalies
            else "FAIL"
        ),
        "anomaly_count": len(anomalies),
        "sample_indices": anomalies[:20],
    }


def check_split_contamination(
    train_records: list[dict[str, Any]],
    validation_records: list[dict[str, Any]],
    test_records: list[dict[str, Any]],
) -> dict[str, Any]:

    def fingerprints(records):
        return {
            str(record)
            for record in records
        }

    train = fingerprints(train_records)
    validation = fingerprints(validation_records)
    test = fingerprints(test_records)

    overlap = (
        (train & validation)
        | (train & test)
        | (validation & test)
    )

    return {
        "name": "split_contamination",
        "status": (
            "PASS"
            if not overlap
            else "FAIL"
        ),
        "overlap_count": len(overlap),
    }



def run_quality_checks(
    records: list[dict[str, Any]],
    train_records: list[dict[str, Any]],
    validation_records: list[dict[str, Any]],
    test_records: list[dict[str, Any]],
    required_fields: set[str],
    sensitive_fields: set[str],
    duplicate_count: int,
) -> dict[str, Any]:

    checks = [
        check_record_count(records),
        check_required_fields(
            records,
            required_fields,
        ),
        check_schema_consistency(records),
        check_empty_values(
            records,
            required_fields
            ),
        check_split_integrity(
            total_records=len(records),
            train_records=train_records,
            validation_records=validation_records,
            test_records=test_records,
        ),
        check_duplicate_integrity(
            unique_records=records,
            duplicate_count=duplicate_count,
        ),
        check_sensitive_fields(
            records,
            sensitive_fields,
        ),
        check_length_statistics(records),
        check_anomalous_records(records),
        check_split_contamination(
            train_records,
            validation_records,
            test_records,
        ),
    ]

    failed_checks = [
        check
        for check in checks
        if check["status"] == "FAIL"
    ]

    return {
        "status": (
            "PASS"
            if not failed_checks
            else "FAIL"
        ),
        "checks": checks,
        "failed_checks": failed_checks,
    }