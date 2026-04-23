from datetime import datetime

from pydantic import BaseModel

from app.enums import RouteStatusEnum


class RouteStatusCreate(BaseModel):
    status: RouteStatusEnum


class RouteStatusOut(BaseModel):
    id: int
    route_id: int
    status: RouteStatusEnum
    created_at: datetime

    class Config:
        from_attributes = True
