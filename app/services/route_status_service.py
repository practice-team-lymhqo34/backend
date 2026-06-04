from datetime import datetime, timezone
from typing import TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import order as crud_order
from app.crud import route_status as crud_route_status
from app.enums import OrderStatus, RouteStatusEnum
from app.schemas.order import OrderUpdate
from app.schemas.route import RouteUpdate
from app.schemas.route_status import RouteStatusCreate
from app.services.invoice_service import invoice_service
from app.services.route_service import route_service

if TYPE_CHECKING:
    from app.models.route_status import RouteStatus

ALLOWED_TRANSITIONS: dict[RouteStatusEnum | None, RouteStatusEnum] = {
    None: RouteStatusEnum.ASSIGNED,
    RouteStatusEnum.ASSIGNED: RouteStatusEnum.LOADED,
    RouteStatusEnum.LOADED: RouteStatusEnum.IN_TRANSIT,
    RouteStatusEnum.IN_TRANSIT: RouteStatusEnum.DELIVERED,
}


class RouteStatusService:
    async def get_statuses(self, db: AsyncSession, route_id: int):
        return await crud_route_status.get_statuses_by_route_id(db, route_id)

    async def add_status(
        self,
        db: AsyncSession,
        route_id: int,
        status_in: RouteStatusCreate,
    ) -> "RouteStatus":
        latest = await crud_route_status.get_latest_status(db, route_id)
        current = latest.status if latest else None

        if status_in.status == RouteStatusEnum.FAILED:
            if current == RouteStatusEnum.DELIVERED:
                raise HTTPException(
                    status_code=409,
                    detail="Cannot mark delivered route as failed",
                )
            return await crud_route_status.create_route_status(
                db, route_id, status_in
            )

        allowed_next = ALLOWED_TRANSITIONS.get(current)
        if status_in.status != allowed_next:
            raise HTTPException(
                status_code=409,
                detail=f"Invalid status transition: "
                f"{current} → {status_in.status}",
            )

        new_status = await crud_route_status.create_route_status(
            db, route_id, status_in
        )

        route_update = None
        order_update = None

        if status_in.status == RouteStatusEnum.IN_TRANSIT:
            route_update = RouteUpdate(started_at=datetime.now(timezone.utc))
            order_update = OrderUpdate(status=OrderStatus.IN_PROGRESS)
        elif status_in.status == RouteStatusEnum.DELIVERED:
            route_update = RouteUpdate(completed_at=datetime.now(timezone.utc))
            order_update = OrderUpdate(
                status=OrderStatus.COMPLETED,
                received_at=datetime.now(timezone.utc),
            )
            fuel_cost = None
            route = await route_service.get_route_or_404(db, route_id)

            # Use the vehicle assigned by manager
            vehicle = None
            if route.vehicle_id:
                from app.services.vehicle_service import vehicle_service
                vehicle = await vehicle_service.get_vehicle_or_404(db, route.vehicle_id)
            elif route.driver_id:
                # Fallback for old routes without vehicle_id
                from app.services.vehicle_service import vehicle_service
                vehicles = await vehicle_service.get_driver_vehicles(db, route.driver_id)
                if vehicles:
                    vehicle = vehicles[0]

            if vehicle:
                fuel_cost = round(
                    ((route.order.distance * vehicle.fuel_consumption) / 100)
                    * vehicle.fuel_price,
                    2,
                )

            route_update = RouteUpdate(
                completed_at=datetime.now(),
                fuel_cost=fuel_cost,
            )
            order_update = OrderUpdate(status=OrderStatus.COMPLETED)

        if route_update:
            updated_route = await route_service.update_route(
                db, route_id, route_update
            )
            if order_update:
                updated_order = await crud_order.update_order(
                    db, updated_route.order, order_update
                )
                if updated_order.status == OrderStatus.COMPLETED:
                    try:
                        await invoice_service.add_order_to_invoice(
                            db, updated_order
                        )
                    except Exception as e:
                        print(f"Failed to update invoice: {e}")

        return new_status


route_status_service = RouteStatusService()
