from fastapi import status

from services.dataset_registry.app.exceptions.base import AppException


class DatasetNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message="Dataset not found.",
            error_code="DATASET_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class DatasetAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(
            message="A dataset with the same name and version already exists.",
            error_code="DATASET_ALREADY_EXISTS",
            status_code=status.HTTP_409_CONFLICT,
        )


class InvalidDatasetException(AppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="INVALID_DATASET",
            status_code=status.HTTP_400_BAD_REQUEST,
        )