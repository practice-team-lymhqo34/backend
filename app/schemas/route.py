from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RouteCreate(BaseModel):
    order_id: int
    driver_id: Optional[int] = None
    eta: datetime


class RouteUpdate(BaseModel):
    driver_id: Optional[int] = None
    eta: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class RouteOut(BaseModel):
    id: int
    order_id: int
    driver_id: Optional[int]
    started_at: Optional[datetime]
    eta: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True
