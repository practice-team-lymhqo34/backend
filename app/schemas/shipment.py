from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ShipmentCreate(BaseModel):
    weight: Decimal
    volume: Decimal
    quantity: int
    description: Optional[str] = None


class ShipmentUpdate(BaseModel):
    weight: Optional[Decimal] = None
    volume: Optional[Decimal] = None
    quantity: Optional[int] = None
    description: Optional[str] = None


class ShipmentOut(BaseModel):
    id: int
    order_id: int
    weight: Decimal
    volume: Decimal
    quantity: int
    description: Optional[str]

    class Config:
        from_attributes = True
