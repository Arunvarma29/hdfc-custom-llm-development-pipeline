from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from services.dataset_registry.app.api.dependencies import get_db
from services.dataset_registry.app.models.dataset import Dataset
from services.dataset_registry.app.schemas.dashboard import (
    DashboardSummaryResponse,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
):
    base_query = db.query(Dataset).filter(
        Dataset.is_deleted.is_(False)
    )

    total = base_query.count()

    uploaded = (
        base_query
        .filter(Dataset.status == "UPLOADED")
        .count()
    )

    preparing = (
        base_query
        .filter(Dataset.status == "PREPARING")
        .count()
    )

    ready = (
        base_query
        .filter(Dataset.status == "READY")
        .count()
    )

    approved = (
        base_query
        .filter(Dataset.status == "APPROVED")
        .count()
    )

    rejected = (
        base_query
        .filter(Dataset.status == "REJECTED")
        .count()
    )

    recent = (
        base_query
        .order_by(Dataset.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "stats": {
            "total_datasets": total,
            "uploaded": uploaded,
            "preparing": preparing,
            "ready": ready,
            "approved": approved,
            "rejected": rejected,
        },
        "recent_datasets": [
            {
                "id": str(dataset.id),
                "name": dataset.name,
                "dataset_type": dataset.dataset_type,
                "domain": dataset.domain,
                "version": dataset.version,
                "status": dataset.status,
                "created_at": dataset.created_at,
            }
            for dataset in recent
        ],
    }