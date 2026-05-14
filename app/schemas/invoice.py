from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class InvoiceBase(BaseModel):
    owner_id: Optional[int] = None
    billing_month: datetime
    total_shipment: int = 0
    total_weight: float = 0.0
    total_volume: float = 0.0
    total_distance: float = 0.0


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(BaseModel):
    owner_id: Optional[int] = None
    billing_month: Optional[datetime] = None
    total_shipment: Optional[int] = None
    total_weight: Optional[float] = None
    total_volume: Optional[float] = None
    total_distance: Optional[float] = None


class InvoiceOut(InvoiceBase):
    id: int
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)
