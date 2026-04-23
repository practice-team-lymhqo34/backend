from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, require_sender
from app.enums import OrderStatus
from app.schemas.notification import NotificationOut
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate
from app.schemas.route import RouteCreate, RouteOut, RouteUpdate
from app.schemas.route_status import RouteStatusOut
from app.schemas.shipment import ShipmentOut
from app.services.notification_service import notification_service
from app.services.order_service import order_service
from app.services.route_service import route_service
from app.services.route_status_service import route_status_service
from app.services.shipment_service import shipment_service

router = APIRouter()


@router.get("/orders", response_model=list[OrderOut])
async def get_orders(
    status: Optional[OrderStatus] = None,
    is_template: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    return await order_service.get_orders(
        db,
        sender_id=current_user.id,
        status=status,
        is_template=is_template,
    )


@router.post("/orders", response_model=OrderOut, status_code=201)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    return await order_service.create_order(
        db, order_in, sender_id=current_user.id
    )


@router.get("/orders/{order_id}", response_model=OrderOut)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    order = await order_service.get_order_or_404(db, order_id)
    if order.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return order


@router.patch("/orders/{order_id}", response_model=OrderOut)
async def update_order(
    order_id: int,
    order_in: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    return await order_service.update_order(
        db, order_id, order_in, sender_id=current_user.id
    )


@router.delete("/orders/{order_id}", status_code=204)
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    await order_service.delete_order(db, order_id, sender_id=current_user.id)


@router.get("/orders/{order_id}/shipments", response_model=list[ShipmentOut])
async def get_shipments(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    order = await order_service.get_order_or_404(db, order_id)
    if order.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return await shipment_service.get_shipments_by_order(db, order_id)


@router.get("/routes", response_model=list[RouteOut])
async def get_routes(
    order_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    return await route_service.get_routes(db, order_id=order_id)


@router.post("/routes", response_model=RouteOut, status_code=201)
async def create_route(
    route_in: RouteCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    return await route_service.create_route(db, route_in)


@router.get("/routes/{route_id}", response_model=RouteOut)
async def get_route(
    route_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    return await route_service.get_route_or_404(db, route_id)


@router.patch("/routes/{route_id}", response_model=RouteOut)
async def update_route(
    route_id: int,
    route_in: RouteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    return await route_service.update_route(db, route_id, route_in)


@router.get("/routes/{route_id}/statuses", response_model=list[RouteStatusOut])
async def get_route_statuses(
    route_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    await route_service.get_route_or_404(db, route_id)
    return await route_status_service.get_statuses(db, route_id)


@router.get("/routes/{route_id}/eta")
async def get_route_eta(
    route_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    route = await route_service.get_route_or_404(db, route_id)
    return {"eta": route.eta}


@router.get("/routes/{route_id}/status")
async def get_route_current_status(
    route_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    await route_service.get_route_or_404(db, route_id)
    statuses = await route_status_service.get_statuses(db, route_id)
    if not statuses:
        return {"status": None}
    return {"status": statuses[-1].status}


@router.get("/notifications", response_model=list[NotificationOut])
async def get_notifications(
    is_read: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    return await notification_service.get_notifications(
        db, user_id=current_user.id, is_read=is_read
    )


@router.patch(
    "/notifications/{notification_id}", response_model=NotificationOut
)
async def mark_notification_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    return await notification_service.mark_as_read(
        db, notification_id, user_id=current_user.id
    )


@router.patch("/notifications/all")
async def mark_all_notifications_read(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_sender),
):
    updated = await notification_service.mark_all_as_read(
        db, user_id=current_user.id
    )
    return {"updated": updated}
