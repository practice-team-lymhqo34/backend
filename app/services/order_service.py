from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import order as crud_order
from app.enums import OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate


class OrderService:
    async def get_order_or_404(self, db: AsyncSession, order_id: int):
        order = await crud_order.get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    async def get_orders(self, db: AsyncSession, **filters):
        return await crud_order.get_orders(db, **filters)

    async def create_order(
        self, db: AsyncSession, order_in: OrderCreate, sender_id: int
    ):
        return await crud_order.create_order(db, order_in, sender_id)

    async def update_order(
        self, db: AsyncSession, order_id: int, order_in: OrderUpdate, sender_id: int
    ):
        order = await self.get_order_or_404(db, order_id)
        if order.sender_id != sender_id:
            raise HTTPException(status_code=403, detail="Access denied")
        if order.status == OrderStatus.IN_PROGRESS:
            raise HTTPException(status_code=409, detail="Order is already in progress")
        return await crud_order.update_order(db, order, order_in)

    async def delete_order(
        self, db: AsyncSession, order_id: int, sender_id: int
    ):
        order = await self.get_order_or_404(db, order_id)
        if order.sender_id != sender_id:
            raise HTTPException(status_code=403, detail="Access denied")
        if order.status != OrderStatus.PENDING:
            raise HTTPException(
                status_code=409, detail="Only pending orders can be deleted"
            )
        await crud_order.delete_order(db, order)


order_service = OrderService()
