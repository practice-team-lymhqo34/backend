from datetime import datetime
from typing import TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import route_status as crud_route_status
from app.enums import RouteStatusEnum
from app.schemas.route import RouteUpdate
from app.schemas.route_status import RouteStatusCreate

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

        # Update route timestamps based on status
        from app.services.route_service import route_service  # noqa: PLC0415

        route_update = None
        if status_in.status == RouteStatusEnum.IN_TRANSIT:
            route_update = RouteUpdate(started_at=datetime.now())
        elif status_in.status == RouteStatusEnum.DELIVERED:
            route_update = RouteUpdate(completed_at=datetime.now())

        if route_update:
            await route_service.update_route(db, route_id, route_update)

        return new_status


route_status_service = RouteStatusService()
