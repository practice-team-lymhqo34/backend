import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import order as crud_order
from app.enums import OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate

logger = logging.getLogger(__name__)


class OrderService:
    async def get_order_or_404(self, db: AsyncSession, order_id: int):

        order = await crud_order.get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    async def get_orders(self, db: AsyncSession, **filters):

        return await crud_order.get_orders(db, **filters)

    async def create_order(
        self, db: AsyncSession, order_in: OrderCreate, owner_id: int
    ):

        return await crud_order.create_order(db, order_in, owner_id)

    async def update_order(
        self,
        db: AsyncSession,
        order_id: int,
        order_in: OrderUpdate,
        owner_id: int,
    ):

        order = await self.get_order_or_404(db, order_id)
        if order.owner_id != owner_id:
            raise HTTPException(status_code=403, detail="Access denied")
        if order.status == OrderStatus.IN_PROGRESS:
            raise HTTPException(
                status_code=409, detail="Order is already in progress"
            )
        return await crud_order.update_order(db, order, order_in)

    async def delete_order(
        self, db: AsyncSession, order_id: int, owner_id: int
    ):

        order = await self.get_order_or_404(db, order_id)
        if order.owner_id != owner_id:
            raise HTTPException(status_code=403, detail="Access denied")
        if order.status != OrderStatus.PENDING:
            raise HTTPException(
                status_code=409, detail="Only pending orders can be deleted"
            )
        await crud_order.delete_order(db, order)

    async def confirm_receipt(
        self, db: AsyncSession, order_id: int, owner_id: int
    ):

        order = await self.get_order_or_404(db, order_id)

        if order.owner_id != owner_id:
            logger.warning(
                f"Unauthorized confirmation attempt: user {owner_id} "
                f"on order {order_id}"
            )
            raise HTTPException(status_code=403, detail="Access denied")

        if order.status == OrderStatus.COMPLETED:
            raise HTTPException(
                status_code=409, detail="Order is already completed"
            )

        if order.status == OrderStatus.CANCELED:
            raise HTTPException(
                status_code=409, detail="Cannot confirm a canceled order"
            )

        if order.status == OrderStatus.PENDING:
            raise HTTPException(
                status_code=409,
                detail="Order must be in progress to confirm receipt",
            )

        updated_order = await crud_order.confirm_order_receipt(db, order)

        logger.info(f"Order {order_id} receipt confirmed by user {owner_id}")
        return updated_order


order_service = OrderService()
