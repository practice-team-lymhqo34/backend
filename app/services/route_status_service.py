from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import route_status as crud_route_status
from app.enums import RouteStatusEnum
from app.schemas.route_status import RouteStatusCreate

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
    ):
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

        return await crud_route_status.create_route_status(
            db, route_id, status_in
        )


route_status_service = RouteStatusService()
