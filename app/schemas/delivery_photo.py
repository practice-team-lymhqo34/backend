from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DeliveryPhotoCreate(BaseModel):
    description: Optional[str] = Field(default=None, max_length=255)


class DeliveryPhotoOut(BaseModel):
    id: int
    route_id: int
    key: str
    description: Optional[str]
    taken: datetime

    class Config:
        from_attributes = True


class DeliveryPhotoUploadOut(BaseModel):
    key: str
    url: str
