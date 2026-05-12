from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.order import OrderCreate, OrderOut
from app.services.order_service import order_service

router = APIRouter()


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(
    *,
    db: AsyncSession = Depends(deps.get_db),
    order_in: OrderCreate,
    current_user: User = Depends(deps.get_current_user),
):
    return await order_service.create_order(
        db, order_in=order_in, owner_id=current_user.id
    )


@router.get("/", response_model=list[OrderOut])
async def get_orders(
    *,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    is_template: Optional[bool] = None,
):
    return await order_service.get_orders(
        db, owner_id=current_user.id, is_template=is_template
    )
