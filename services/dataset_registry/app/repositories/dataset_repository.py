from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from services.dataset_registry.app.models.dataset import Dataset
from services.dataset_registry.app.schemas.dataset import DatasetCreate
from sqlalchemy import asc, desc, or_
from datetime import datetime,UTC
from services.dataset_registry.app.schemas.common import DatasetQueryParams

class DatasetRepository:

    def create(
        self,
        db: Session,
        dataset: DatasetCreate,
        file_name: str,
        object_key: str,
        file_size: int,
        content_type: str,
    ) -> Dataset :

        db_dataset = Dataset(
            name=dataset.name,
            description=dataset.description,
            dataset_type=dataset.dataset_type,
            domain=dataset.domain,
            version=dataset.version,
            file_name=file_name,
            object_key=object_key,
            file_size=file_size,
            content_type=content_type,
        )

        db.add(db_dataset)
        try:
            db.commit()
            db.refresh(db_dataset)
        except:
            db.rollback()
            raise
        return db_dataset

    

    def get_all(self, db: Session):
        return db.query(Dataset).order_by(Dataset.created_at.desc()).all()





    def get_by_id(
        self,
        db: Session,
        dataset_id: UUID,
    ):
        return (
            db.query(Dataset)
           .filter(
                Dataset.id == dataset_id,
                Dataset.is_deleted == False,
            )
            .first()
        )





    def update_status(
        self,
        db: Session,
        dataset: Dataset,
        status: str,
    ) -> Dataset:
        dataset.status = status

        db.commit()
        db.refresh(dataset)

        return dataset




    def delete(
        self,
        db: Session,
        dataset: Dataset,
    ):
        dataset.is_deleted = True
        dataset.deleted_at = datetime.now(UTC)

        db.commit()
        db.refresh(dataset)





    def exists(
        self,
        db: Session,
        name: str,
        version: str,
    )-> Dataset | None:

        return (
            db.query(Dataset)
           .filter(
                func.lower(Dataset.name) == name.lower(),
                Dataset.version == version,
            Dataset.is_deleted == False,
        )
    .first()
    )




    def get_datasets(
        self,
        db: Session,
        params: DatasetQueryParams,
    ):
        query = (
            db.query(Dataset)
            .filter(Dataset.is_deleted==False)
        )
    # Search
        if params.search:
            search = f"%{params.search}%"

            query = query.filter(
                or_(
                Dataset.name.ilike(search),
                Dataset.description.ilike(search),
                Dataset.dataset_type.ilike(search),
                Dataset.domain.ilike(search),
                )
            )

    # Filter

        if params.dataset_type:
            query = query.filter(
            Dataset.dataset_type == params.dataset_type
        )

        if params.status:
            query = query.filter(
            Dataset.status == params.status
        )

        if params.domain:
            query = query.filter(
            Dataset.domain == params.domain
        )

    # Sorting

        SORT_COLUMNS = {
        "created_at": Dataset.created_at,
        "name": Dataset.name,
        "version": Dataset.version,
        }

        column = SORT_COLUMNS.get(
        params.sort_by,
        Dataset.created_at,
        )
        
        if params.order == "asc":
            query = query.order_by(
            asc(column)
             )
        else:
            query = query.order_by(
            desc(column)
        )

    # Pagination

       # Count AFTER search & filters, BEFORE pagination
            total = query.count()

        # Sorting
            SORT_COLUMNS = {
             "created_at": Dataset.created_at,
             "name": Dataset.name,
             "version": Dataset.version,
        }

        column = SORT_COLUMNS.get(
         params.sort_by,
         Dataset.created_at,
        )

        if params.order == "asc":
         query = query.order_by(asc(column))
        else:
         query = query.order_by(desc(column))

        offset = (params.page - 1) * params.limit

        items = (
             query
            .offset(offset)
            .limit(params.limit)
             .all()
        )

        return items, total




def get_governance_data(
    self,
    db: Session,
    dataset_id: UUID,
):
    return (
        db.query(Dataset)
        .filter(
            Dataset.id == dataset_id,
            Dataset.is_deleted == False,
        )
        .first()
    )