from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.enums import RouteStatusEnum


class RouteStatusCreate(BaseModel):
    status: RouteStatusEnum


class RouteStatusOut(BaseModel):
    id: int
    route_id: int
    status: RouteStatusEnum
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
