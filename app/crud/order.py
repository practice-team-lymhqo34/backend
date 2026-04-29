from typing import Any, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import OrderStatus
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate


async def get_order_by_id(db: AsyncSession, order_id: int) -> Optional[Order]:
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalars().first()


async def get_orders(
    db: AsyncSession,
    sender_id: Optional[int] = None,
    recipient_id: Optional[int] = None,
    status: Optional[OrderStatus] = None,
    is_template: Optional[bool] = None,
) -> Sequence[Any]:
    query = select(Order)
    if sender_id is not None:
        query = query.where(Order.sender_id == sender_id)
    if recipient_id is not None:
        query = query.where(Order.recipient_id == recipient_id)
    if status is not None:
        query = query.where(Order.status == status)
    if is_template is not None:
        query = query.where(Order.is_template == is_template)
    result = await db.execute(query)
    return result.scalars().all()


async def create_order(
    db: AsyncSession, order_in: OrderCreate, sender_id: int
) -> Order:
    db_order = Order(
        sender_id=sender_id,
        recipient_id=order_in.recipient_id,
        name=order_in.name,
        origin_address=order_in.origin_address,
        destination_address=order_in.destination_address,
        distance=order_in.distance,
        is_template=order_in.is_template,
        status=OrderStatus.PENDING,
    )
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order


async def update_order(
    db: AsyncSession, order: Order, order_in: OrderUpdate
) -> Order:
    update_data = order_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def delete_order(db: AsyncSession, order: Order) -> None:
    await db.delete(order)
    await db.commit()
