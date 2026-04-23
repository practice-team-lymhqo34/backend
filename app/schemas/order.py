from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    title: str = Field(
        ..., min_length=3, max_length=100, example="Доставка будматеріалів"
    )
    description: Optional[str] = Field(
        None, example="Привезти 10 мішків цементу"
    )
    weight: float = Field(..., gt=0, example=50.5)


class OrderOut(OrderCreate):
    id: int
    owner_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
