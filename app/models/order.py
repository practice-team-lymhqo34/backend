from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Column, DateTime, Enum, Field, SQLModel, func

from app.enums import OrderStatus


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)

    sender_id: Optional[int] = Field(default=None, foreign_key="users.id")
    recipient_id: Optional[int] = Field(default=None, foreign_key="users.id")

    name: str = Field(max_length=50, nullable=False)
    is_template: bool = Field(default=False)

    origin_address: str = Field(max_length=150, nullable=False)
    destination_address: str = Field(max_length=150, nullable=False)
    distance: Decimal = Field(max_digits=10, decimal_places=3, nullable=False)

    status: OrderStatus = Field(
        sa_column=Column(Enum(OrderStatus, native_enum=False), nullable=False)
    )

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
