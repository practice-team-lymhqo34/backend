from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, require_roles
from app.enums import OrderStatus, UserRole
from app.schemas.delivery_photo import DeliveryPhotoOut, DeliveryPhotoUploadOut
from app.schemas.notification import NotificationOut
from app.schemas.order import OrderOut
from app.schemas.route import RouteCreate, RouteOut, RouteUpdate
from app.schemas.route_status import RouteStatusCreate, RouteStatusOut
from app.schemas.shipment import ShipmentOut
from app.schemas.vehicle import VehicleCreate, VehicleOut, VehicleUpdate
from app.services.delivery_photo_service import delivery_photo_service
from app.services.notification_service import notification_service
from app.services.order_service import order_service
from app.services.route_service import route_service
from app.services.route_status_service import route_status_service
from app.services.shipment_service import shipment_service
from app.services.vehicle_service import vehicle_service

router = APIRouter()


@router.get("/orders", response_model=list[OrderOut])
async def get_orders(
    status: Optional[OrderStatus] = None,
    is_template: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.CLIENT)),
):
    return await order_service.get_orders(
        db,
        sender_id=current_user.id,
        status=status,
        is_template=is_template,
    )


@router.get("/orders/{order_id}", response_model=OrderOut)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.CLIENT)),
):
    order = await order_service.get_order_or_404(db, order_id)
    if order.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return order


@router.post("/routes", response_model=RouteOut, status_code=201)
async def create_route(
    route_in: RouteCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_roles(UserRole.CLIENT)),
):
    return await route_service.create_route(db, route_in)


@router.patch("/routes/{route_id}", response_model=RouteOut)
async def update_route(
    route_id: int,
    route_in: RouteUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_roles(UserRole.CLIENT)),
):
    return await route_service.update_route(db, route_id, route_in)


@router.get("/orders/{order_id}/shipments", response_model=list[ShipmentOut])
async def get_shipments(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.CLIENT, UserRole.DRIVER)),
):
    order = await order_service.get_order_or_404(db, order_id)
    if (
        current_user.role == UserRole.CLIENT
        and order.sender_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Access denied")
    return await shipment_service.get_shipments_by_order(db, order_id)


@router.get("/routes", response_model=list[RouteOut])
async def get_routes(
    order_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.CLIENT, UserRole.DRIVER)),
):
    driver_id = (
        current_user.id if current_user.role == UserRole.DRIVER else None
    )
    return await route_service.get_routes(
        db, order_id=order_id, driver_id=driver_id
    )


@router.get("/routes/{route_id}", response_model=RouteOut)
async def get_route(
    route_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.CLIENT, UserRole.DRIVER)),
):
    route = await route_service.get_route_or_404(db, route_id)
    if (
        current_user.role == UserRole.DRIVER
        and route.driver_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Not your route")
    return route


@router.get("/routes/{route_id}/statuses", response_model=list[RouteStatusOut])
async def get_route_statuses(
    route_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_roles(UserRole.CLIENT, UserRole.DRIVER)),
):
    await route_service.get_route_or_404(db, route_id)
    return await route_status_service.get_statuses(db, route_id)


@router.get("/routes/{route_id}/status")
async def get_route_current_status(
    route_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_roles(UserRole.CLIENT, UserRole.DRIVER)),
):
    await route_service.get_route_or_404(db, route_id)
    statuses = await route_status_service.get_statuses(db, route_id)
    if not statuses:
        return {"status": None}
    return {"status": statuses[-1].status}


@router.get("/routes/{route_id}/eta")
async def get_route_eta(
    route_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_roles(UserRole.CLIENT, UserRole.DRIVER)),
):
    route = await route_service.get_route_or_404(db, route_id)
    return {"eta": route.eta}


@router.get("/routes/{route_id}/photos", response_model=list[DeliveryPhotoOut])
async def get_route_photos(
    route_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_roles(UserRole.CLIENT, UserRole.DRIVER)),
):
    await route_service.get_route_or_404(db, route_id)
    return await delivery_photo_service.get_route_photos(db, route_id)


@router.get("/notifications", response_model=list[NotificationOut])
async def get_notifications(
    is_read: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.CLIENT, UserRole.DRIVER)),
):
    return await notification_service.get_notifications(
        db, user_id=current_user.id, is_read=is_read
    )


@router.patch("/notifications/read-all")
async def mark_all_notifications_read(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.CLIENT, UserRole.DRIVER)),
):
    updated = await notification_service.mark_all_as_read(
        db, user_id=current_user.id
    )
    return {"updated": updated}


@router.patch(
    "/notifications/{notification_id}", response_model=NotificationOut
)
async def mark_notification_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.CLIENT, UserRole.DRIVER)),
):
    return await notification_service.mark_as_read(
        db, notification_id, user_id=current_user.id
    )


@router.post(
    "/routes/{route_id}/statuses",
    response_model=RouteStatusOut,
    status_code=201,
)
async def add_route_status(
    route_id: int,
    status_in: RouteStatusCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.DRIVER)),
):
    route = await route_service.get_route_or_404(db, route_id)
    if route.driver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your route")
    return await route_status_service.add_status(db, route_id, status_in)


@router.post(
    "/routes/{route_id}/photos",
    response_model=DeliveryPhotoUploadOut,
    status_code=201,
)
async def upload_route_photo(
    route_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = Form(default=None),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.DRIVER)),
):
    route = await route_service.get_route_or_404(db, route_id)
    if route.driver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your route")
    return await delivery_photo_service.upload_photo(
        db, route_id, file, description, current_user
    )


@router.get("/vehicles", response_model=list[VehicleOut])
async def get_my_vehicles(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.DRIVER)),
):
    return await vehicle_service.get_driver_vehicles(db, current_user.id)


@router.post("/vehicles", response_model=VehicleOut, status_code=201)
async def add_vehicle(
    vehicle_in: VehicleCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.DRIVER)),
):
    return await vehicle_service.add_vehicle(db, vehicle_in, current_user)


@router.get("/vehicles/{vehicle_id}", response_model=VehicleOut)
async def get_vehicle(
    vehicle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.DRIVER)),
):
    vehicle = await vehicle_service.get_vehicle_or_404(db, vehicle_id)
    if vehicle.driver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your vehicle")
    return vehicle


@router.patch("/vehicles/{vehicle_id}", response_model=VehicleOut)
async def update_vehicle(
    vehicle_id: int,
    vehicle_in: VehicleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.DRIVER)),
):
    return await vehicle_service.update_vehicle(
        db, vehicle_id, vehicle_in, current_user
    )


@router.delete("/vehicles/{vehicle_id}", status_code=204)
async def delete_vehicle(
    vehicle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.DRIVER)),
):
    await vehicle_service.remove_vehicle(db, vehicle_id, current_user)
