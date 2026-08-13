from dataclasses import replace

from services.data_preparation.app.config.preparation_profiles import (
    PreparationProfile,
    get_preparation_profile,
)


DOCUMENT_CONTENT_TYPES = {
    "text/plain",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def get_profile(
    dataset_type: str,
    content_type: str,
) -> PreparationProfile:

    profile = get_preparation_profile(
        dataset_type
    )

    # Unstructured document input
    if content_type in DOCUMENT_CONTENT_TYPES:

        return replace(
            profile,
            required_fields={
                "content",
            },
        )

    return profile