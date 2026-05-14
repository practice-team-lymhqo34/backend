from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import route as crud_route
from app.models.route import Route
from app.schemas.route import RouteCreate, RouteUpdate


class RouteService:
    async def get_route_or_404(self, db: AsyncSession, route_id: int) -> Route:
        route = await crud_route.get_route_by_id(db, route_id)
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        return route

    async def get_routes(self, db: AsyncSession, **filters):
        return await crud_route.get_routes(db, **filters)

    async def get_today_routes(
        self, db: AsyncSession, driver_id: int
    ) -> Sequence[Route]:
        return await crud_route.get_today_routes_by_driver(db, driver_id)

    async def create_route(
        self, db: AsyncSession, route_in: RouteCreate
    ) -> Route:
        existing = await crud_route.get_route_by_order_id(
            db, route_in.order_id
        )
        if existing:
            raise HTTPException(
                status_code=409, detail="Route already exists for this order"
            )
        return await crud_route.create_route(db, route_in)

    async def update_route(
        self, db: AsyncSession, route_id: int, route_in: RouteUpdate
    ) -> Route:
        route = await self.get_route_or_404(db, route_id)
        if route.completed_at is not None:
            raise HTTPException(
                status_code=409, detail="Route is already completed"
            )
        return await crud_route.update_route(db, route, route_in)

    async def delete_route(self, db: AsyncSession, route_id: int) -> None:
        route = await self.get_route_or_404(db, route_id)
        await crud_route.delete_route(db, route)


route_service = RouteService()
