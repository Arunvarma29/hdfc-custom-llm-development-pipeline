import random
from datetime import datetime
from typing import Any


def _split_groups(
    groups: dict[str, list[dict[str, Any]]],
    train_ratio: float,
    validation_ratio: float,
    test_ratio: float,
    seed: int,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    group_items = list(groups.items())

    random.Random(seed).shuffle(group_items)

    total_groups = len(group_items)

    train_end = int(total_groups * train_ratio)
    validation_count = int(total_groups * validation_ratio)
    test_count = int(total_groups * test_ratio)

    if total_groups >= 3:
        validation_count = max(validation_count, 1)
        test_count = max(test_count, 1)

    if train_end + validation_count + test_count > total_groups:
        train_end = total_groups - validation_count - test_count

    validation_end = train_end + validation_count

    train_groups = group_items[:train_end]
    validation_groups = group_items[
        train_end:validation_end
    ]
    test_groups = group_items[
        validation_end:
    ]

    train_records = [
        record
        for _, group_records in train_groups
        for record in group_records
    ]

    validation_records = [
        record
        for _, group_records in validation_groups
        for record in group_records
    ]

    test_records = [
        record
        for _, group_records in test_groups
        for record in group_records
    ]

    return (
        train_records,
        validation_records,
        test_records,
    )




def _split_entity_by_time(
    records: list[dict[str, Any]],
    entity_field: str,
    time_field: str,
    train_ratio: float,
    validation_ratio: float,
    test_ratio: float,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    entities: dict[str, list[dict[str, Any]]] = {}

    for record in records:
        if entity_field not in record:
            raise ValueError(
                f"Entity field '{entity_field}' "
                "is missing from one or more records."
            )

        if time_field not in record:
            raise ValueError(
                f"Time field '{time_field}' "
                "is missing from one or more records."
            )

        entity_id = str(record[entity_field])

        entities.setdefault(
            entity_id,
            [],
        ).append(record)

    entity_items: list[
        tuple[str, list[dict[str, Any]], datetime]
    ] = []

    for entity_id, entity_records in entities.items():
        latest_time = max(
            datetime.fromisoformat(
                str(record[time_field])
            )
            for record in entity_records
        )

        entity_items.append(
            (
                entity_id,
                entity_records,
                latest_time,
            )
        )

    entity_items.sort(
        key=lambda item: item[2]
    )

    total_entities = len(entity_items)

    train_end = int(
        total_entities * train_ratio
    )

    validation_count = int(
        total_entities * validation_ratio
    )

    test_count = total_entities - train_end - validation_count

    if total_entities >= 3:
        validation_count = max(
            validation_count,
            1,
        )
        test_count = max(
            test_count,
            1,
        )

        train_end = (
            total_entities
            - validation_count
            - test_count
        )

    validation_end = (
        train_end + validation_count
    )

    train_entities = entity_items[:train_end]

    validation_entities = entity_items[
        train_end:validation_end
    ]

    test_entities = entity_items[
        validation_end:
    ]

    train_records = [
        record
        for _, entity_records, _ in train_entities
        for record in entity_records
    ]

    validation_records = [
        record
        for _, entity_records, _ in validation_entities
        for record in entity_records
    ]

    test_records = [
        record
        for _, entity_records, _ in test_entities
        for record in entity_records
    ]

    return (
        train_records,
        validation_records,
        test_records,
    )



def split_dataset(
    records: list[dict[str, Any]],
    train_ratio: float = 0.80,
    validation_ratio: float = 0.10,
    test_ratio: float = 0.10,
    seed: int = 42,
    entity_field: str | None = None,
    time_field: str | None = None,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:

    total_ratio = (
        train_ratio
        + validation_ratio
        + test_ratio
    )

    if abs(total_ratio - 1.0) > 1e-9:
        raise ValueError(
            "Train, validation, and test ratios "
            "must add up to 1.0"
        )

    if not records:
        return [], [], []

    # -----------------------------------------
    # Entity + time-aware split
    # -----------------------------------------

    if entity_field and time_field:
        return _split_entity_by_time(
            records=records,
            entity_field=entity_field,
            time_field=time_field,
            train_ratio=train_ratio,
            validation_ratio=validation_ratio,
            test_ratio=test_ratio,
        )

    # -----------------------------------------
    # Time-aware split
    # -----------------------------------------

    if time_field:
        if not all(
            time_field in record
            for record in records
        ):
            raise ValueError(
                f"Time field '{time_field}' "
                "is missing from one or more records."
            )

        sorted_records = sorted(
            records,
            key=lambda record: (
                datetime.fromisoformat(
                    str(record[time_field])
                )
            ),
        )

        total = len(sorted_records)

        train_end = int(
            total * train_ratio
        )

        validation_end = (
            train_end
            + int(total * validation_ratio)
        )

        return (
            sorted_records[:train_end],
            sorted_records[
            train_end:validation_end
        ],
            sorted_records[
                validation_end:
        ],
    )
    # -----------------------------------------
    # Entity-aware split
    # -----------------------------------------

    if entity_field:
        groups: dict[str, list[dict[str, Any]]] = {}

        for record in records:
            if entity_field not in record:
                raise ValueError(
                    f"Entity field '{entity_field}' "
                    "is missing from one or more records."
                )

            entity_id = str(
                record[entity_field]
            )

            groups.setdefault(
                entity_id,
                [],
            ).append(record)

        return _split_groups(
            groups=groups,
            train_ratio=train_ratio,
            validation_ratio=validation_ratio,
            test_ratio=test_ratio,
            seed=seed,
        )

    # -----------------------------------------
    # Document-aware split
    # -----------------------------------------

    if any(
        "document_id" in record
        for record in records
    ):
        groups: dict[str, list[dict[str, Any]]] = {}

        for record in records:
            document_id = str(
                record.get("document_id")
            )

            groups.setdefault(
                document_id,
                [],
            ).append(record)

        return _split_groups(
            groups=groups,
            train_ratio=train_ratio,
            validation_ratio=validation_ratio,
            test_ratio=test_ratio,
            seed=seed,
        )

    # -----------------------------------------
    # Normal tabular split
    # -----------------------------------------

    shuffled_records = records.copy()

    random.Random(seed).shuffle(
        shuffled_records
    )

    total = len(shuffled_records)

    train_end = int(
        total * train_ratio
    )

    validation_end = (
        train_end
        + int(total * validation_ratio)
    )

    return (
        shuffled_records[:train_end],
        shuffled_records[
            train_end:validation_end
        ],
        shuffled_records[
            validation_end:
        ],
    )