from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.enums import OrderStatus


class OrderCreate(BaseModel):
    recipient_id: Optional[int] = None
    name: str
    origin_address: str
    destination_address: str
    distance: Decimal
    is_template: bool = False


class OrderUpdate(BaseModel):
    name: Optional[str] = None
    origin_address: Optional[str] = None
    destination_address: Optional[str] = None
    status: Optional[OrderStatus] = None


class OrderOut(BaseModel):
    id: int
    sender_id: Optional[int]
    recipient_id: Optional[int]
    name: str
    origin_address: str
    destination_address: str
    distance: Decimal
    is_template: bool
    title: str = Field(
        ..., min_length=3, max_length=100, example="Доставка будматеріалів"
    )
    description: Optional[str] = Field(
        None, example="Привезти 10 мішків цементу"
    )
    weight: float = Field(..., gt=0, example=50.5)
