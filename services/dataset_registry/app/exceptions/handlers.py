from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from services.dataset_registry.app.exceptions.dataset import (
    DatasetAlreadyExistsException,
    DatasetNotFoundException,AppException
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def dataset_not_found(
        request: Request,
        exc: AppException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error_code": exc.error_code,
                "message": exc.message,
            },
        )

    @app.exception_handler(
        DatasetAlreadyExistsException
    )
    async def dataset_exists(
        request: Request,
        exc: DatasetAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": exc.message,
            },
        )