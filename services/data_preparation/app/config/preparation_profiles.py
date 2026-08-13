from dataclasses import dataclass


@dataclass(frozen=True)
class PreparationProfile:
    required_fields: set[str]
    sensitive_fields: set[str]
    entity_field: str | None = None
    time_field: str | None = None

PREPARATION_PROFILES: dict[str, PreparationProfile] = {
        "logs": PreparationProfile(
                required_fields={
            "customer_id",
            "app_version",
            "device_model",
            "platform",
            "login_frequency_per_month",
            "last_login",
            "fingerprint_enabled",
            "face_id_enabled",
            "push_notifications",
            "app_crash",
    },
    sensitive_fields={
        "customer_id",
    },
    entity_field="customer_id",
    time_field="last_login",
),

    "transactions": PreparationProfile(
        required_fields={
            "transaction_id",
            "customer_id",
            "transaction_type",
            "amount",
            "transaction_status",
            "transaction_date",
        },
        sensitive_fields={
            "customer_id",
            "account_number",
        },
    ),

    "complaints": PreparationProfile(
        required_fields={
            "case_id",
            "complaint_text",
            "issue_type",
            "priority",
            "status",
        },
        sensitive_fields={
            "customer_name",
            "customer_contact",
        },
    ),

    "faq": PreparationProfile(
        required_fields={
            "question",
            "answer",
        },
        sensitive_fields=set(),
    ),

    "documents": PreparationProfile(
        required_fields={
            "document_id",
            "title",
            "content",
        },
        sensitive_fields=set(),
    ),

    "debit_cards": PreparationProfile(
        required_fields={
            "card_number",
            "customer_id",
            "debit_card_type",
            "card_network",
            "card_status",
        },
        sensitive_fields={
            "card_number",
            "customer_id",
        },
    ),
}


DATASET_TYPE_ALIASES: dict[str, str] = {
    "logs": "logs",
    "log": "logs",

    "transactions": "transactions",
    "transaction": "transactions",

    "complaints": "complaints",
    "complaint": "complaints",

    "faq": "faq",

    "documents": "documents",
    "document": "documents",

    "debit_cards": "debit_cards",
    "debit card": "debit_cards",
}


def get_preparation_profile(
    dataset_type: str,
) -> PreparationProfile:

    normalized_type = dataset_type.strip().lower()

    profile_key = DATASET_TYPE_ALIASES.get(
        normalized_type
    )

    if profile_key is None:
        raise ValueError(
            f"No preparation profile configured "
            f"for dataset type: {dataset_type}"
        )

    return PREPARATION_PROFILES[profile_key]