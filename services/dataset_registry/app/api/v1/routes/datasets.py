from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from services.dataset_registry.app.api.dependencies import get_db
from services.dataset_registry.app.services.dataset_service import DatasetService
from fastapi import Query
from services.dataset_registry.app.schemas.common import DatasetListResponse, DatasetQueryParams
from fastapi.responses import StreamingResponse

from services.data_preparation.app.schemas.preparation import (
    PreparationJobResponse,
)

from services.data_preparation.app.schemas.governance import (
    DatasetGovernanceResponse,
)

from services.dataset_registry.app.schemas.dataset import (
    DatasetCreate,
    DatasetResponse,
    DatasetReviewRequest,
)



router = APIRouter(prefix="/datasets", tags=["Datasets"])

service = DatasetService()


@router.post("", response_model=DatasetResponse, status_code=201)
def create_dataset(
    name: str = Form(...),
    description: str = Form(...),
    dataset_type: str = Form(...),
    domain: str = Form(...),
    version: str = Form("1.0.0"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    payload = DatasetCreate(
        name=name,
        description=description,
        dataset_type=dataset_type,
        domain=domain,
        version=version,
    )

    return service.create_dataset(
        db=db,
        dataset=payload,
        file=file,
    )




@router.get(
    "",
    response_model=DatasetListResponse,
)
def list_datasets(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = None,
    dataset_type: str | None = None,
    status: str | None = None,
    domain: str | None = None,
    sort_by: str = "created_at",
    order: str = "desc",
    db: Session = Depends(get_db),
):

    params = DatasetQueryParams(
        page=page,
        limit=limit,
        search=search,
        dataset_type=dataset_type,
        status=status,
        domain=domain,
        sort_by=sort_by,
        order=order,
    )

    return service.list_datasets(
        db,
        params,
    )





@router.post("/{dataset_id}/prepare")
def prepare_dataset(
    dataset_id: UUID,
    db: Session = Depends(get_db),
):
    return service.prepare_dataset(
        db=db,
        dataset_id=dataset_id,
    )



@router.post(
    "/{dataset_id}/approve",
    response_model=DatasetResponse,
)
def approve_dataset(
    dataset_id: UUID,
    review: DatasetReviewRequest,
    db: Session = Depends(get_db),
):
    return service.approve_dataset(
        db=db,
        dataset_id=dataset_id,
        reviewer_name=review.reviewer_name,
        review_comment=review.comment,
    )

@router.post(
    "/{dataset_id}/reject",
    response_model=DatasetResponse,
)
def reject_dataset(
    dataset_id: UUID,
    review: DatasetReviewRequest,
    db: Session = Depends(get_db),
):
    return service.reject_dataset(
        db=db,
        dataset_id=dataset_id,
        reviewer_name=review.reviewer_name,
        review_comment=review.comment,
    )


@router.get(
    "/{dataset_id}/preparation",
    response_model=PreparationJobResponse,
)
def get_preparation(
    dataset_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_preparation(
        db=db,
        dataset_id=dataset_id,
    )





@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(
    dataset_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_dataset(
        db,
        dataset_id,
    )



@router.delete("/{dataset_id}", status_code=204)
def delete_dataset(
    dataset_id: UUID,
    db: Session = Depends(get_db),
):
    service.delete_dataset(
        db,
        dataset_id,
    )



@router.get("/{dataset_id}/download")
def download_dataset(
    dataset_id: UUID,
    db: Session = Depends(get_db),
):
    file_stream, dataset = service.download_dataset(
        db=db,
        dataset_id=dataset_id,
    )

    return StreamingResponse(
        file_stream,
        media_type=dataset.content_type,
        headers={
            "Content-Disposition": f'inline; filename="{dataset.file_name}"'
        },
    )




@router.get(
    "/{dataset_id}/governance",
    response_model=DatasetGovernanceResponse,
)
def get_dataset_governance(
    dataset_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_governance_data(
        db=db,
        dataset_id=dataset_id,
    )



@router.get("/{dataset_id}/quality")
def get_quality_report(
    dataset_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_quality_report(
        db=db,
        dataset_id=dataset_id,
    )



@router.get("/{dataset_id}/artifact")
def get_prepared_artifact(
    dataset_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_prepared_artifact(
        db=db,
        dataset_id=dataset_id,
    )



@router.post("/{dataset_id}/preparation/run")
def run_preparation(
    dataset_id: UUID,
    db: Session = Depends(get_db),
):
    return service.run_preparation(
        db=db,
        dataset_id=dataset_id,
    )


@router.post("/{dataset_id}/quality/run")
def run_quality_check(
    dataset_id: UUID,
    db: Session = Depends(get_db),
):
    return service.run_quality_check(
        db=db,
        dataset_id=dataset_id,
    )



