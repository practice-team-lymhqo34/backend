from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.enums import OrderStatus


class OrderBase(BaseModel):
    title: str = Field(
        ..., min_length=3, max_length=100, example="Доставка будматеріалів"
    )
    description: Optional[str] = Field(
        None, example="Привезти 10 мішків цементу"
    )
    weight: float = Field(..., gt=0, example=50.5)
    is_template: bool = Field(default=False)


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    weight: Optional[float] = Field(None, gt=0)
    status: Optional[OrderStatus] = None
    is_template: Optional[bool] = None


class OrderOut(OrderBase):
    id: int
    owner_id: int
    status: OrderStatus
    created_at: datetime

    class Config:
        from_attributes = True
