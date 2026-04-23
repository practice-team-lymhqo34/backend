from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.order import Order
from app.models.user import User
from app.schemas.order import OrderCreate, OrderOut

router = APIRouter()


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(
    *,
    db: AsyncSession = Depends(deps.get_db),
    order_in: OrderCreate,
    current_user: User = Depends(deps.get_current_user),
):
    db_order = Order(
        **order_in.model_dump(), owner_id=current_user.id, status="pending"
    )

    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    return db_order
