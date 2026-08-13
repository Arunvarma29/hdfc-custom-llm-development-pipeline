from datetime import datetime
from enum import Enum
from uuid import UUID
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class DatasetType(str, Enum):
    FAQ = "faq"
    TRANSACTIONS = "transactions"
    COMPLAINTS = "complaints"
    DOCUMENTS = "documents"
    LOGS = "logs"


class DatasetDomain(str, Enum):
    RETAIL_BANKING = "retail_banking"
    CORPORATE_BANKING = "corporate_banking"
    PAYMENTS = "payments"
    CARDS = "cards"
    LOANS = "loans"
    INSURANCE = "insurance"
    NET_BANKING = "net_banking"
    UPI = "upi"
    KYC = "kyc"
    FRAUD = "fraud"



class DatasetCreate(BaseModel):

    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=100,
        ),
    ]

    description: Annotated[
        str,
        Field(
            min_length=10,
            max_length=1000,
        ),
    ]

    dataset_type: DatasetType

    domain: DatasetDomain

    version: str = "1.0.0"

    @field_validator(
        "name",
        "description",
    )
    @classmethod
    def strip_values(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError(
                "Field cannot be empty."
            )

        return value

    @field_validator(
        "dataset_type",
        mode="before",
    )
    @classmethod
    def normalize_dataset_type(cls, value):

        if isinstance(value, str):

            value = value.strip().lower()

            aliases = {
                "faq": "faq",

                "transaction": "transactions",
                "transactions": "transactions",

                "complaint": "complaints",
                "complaints": "complaints",

                "document": "documents",
                "documents": "documents",

                "log": "logs",
                "logs": "logs",
            }

            return aliases.get(
                value,
                value,
            )

        return value

    @field_validator(
        "domain",
        mode="before",
    )
    @classmethod
    def normalize_domain(cls, value):

        if isinstance(value, str):

            return (
                value
                .strip()
                .lower()
                .replace(" ", "_")
            )

        return value

class DatasetResponse(BaseModel):
    id: UUID
    name: str
    description: str
    dataset_type: str
    domain: str
    version: str
    file_name: str
    object_key: str
    file_size: int
    content_type: str
    status: str
    created_at: datetime
    updated_at: datetime
    reviewer_name: str | None = None
    review_comment: str | None = None
    reviewed_at: datetime | None = None

    is_frozen: bool
    frozen_at: datetime | None = None
    
    model_config = ConfigDict(
        from_attributes=True
    )



class DatasetReviewRequest(BaseModel):
    reviewer_name: Annotated[
        str,
        Field(min_length=2, max_length=255),
    ]

    comment: Annotated[
        str | None,
        Field(default=None, max_length=2000),
    ]

    @field_validator("reviewer_name")
    @classmethod
    def strip_reviewer_name(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError(
                "Reviewer name cannot be empty."
            )

        return value

    @field_validator("comment")
    @classmethod
    def strip_comment(cls, value):
        if value is None:
            return None

        value = value.strip()

        return value or None