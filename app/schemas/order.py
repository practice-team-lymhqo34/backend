from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.enums import OrderStatus


class OrderBase(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        json_schema_extra={"example": "Доставка будматеріалів"},
    )
    description: Optional[str] = Field(
        None, json_schema_extra={"example": "Привезти 10 мішків цементу"}
    )
    origin_address: Optional[str] = Field(
        None, json_schema_extra={"example": "Київ, вул. Хрещатик, 1"}
    )
    destination_address: Optional[str] = Field(
        None, json_schema_extra={"example": "Львів, вул. Зелена, 10"}
    )
    weight: float = Field(..., gt=0, json_schema_extra={"example": 50.5})
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

    model_config = ConfigDict(from_attributes=True)
