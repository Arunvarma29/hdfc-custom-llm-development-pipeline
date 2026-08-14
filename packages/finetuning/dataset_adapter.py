from typing import Any


def records_to_text(
    records: list[dict[str, Any]],
) -> list[str]:
    texts: list[str] = []

    for record in records:
        parts: list[str] = []

        for key, value in record.items():
            parts.append(
                f"{key}: {value}"
            )

        texts.append(
            "\n".join(parts)
        )

    return texts


def tokenize_texts(
    tokenizer,
    texts: list[str],
    max_length: int = 512,
):
    return tokenizer(
        texts,
        truncation=True,
        padding="max_length",
        max_length=max_length,
    )