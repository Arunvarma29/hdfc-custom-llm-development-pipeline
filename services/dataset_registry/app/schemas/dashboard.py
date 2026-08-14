from datetime import datetime

from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_datasets: int
    uploaded: int
    preparing: int
    ready: int
    approved: int
    rejected: int


class RecentDataset(BaseModel):
    id: str
    name: str
    dataset_type: str
    domain: str
    version: str
    status: str
    created_at: datetime


class DashboardSummaryResponse(BaseModel):
    stats: DashboardStats
    recent_datasets: list[RecentDataset]