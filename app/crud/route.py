from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from app.models.route import Route
from app.schemas.route import RouteCreate, RouteUpdate


async def get_route_by_id(db: AsyncSession, route_id: int) -> Optional[Route]:
    result = await db.execute(select(Route).where(col(Route.id) == route_id))
    return result.scalars().first()


async def get_route_by_order_id(
    db: AsyncSession, order_id: int
) -> Optional[Route]:
    result = await db.execute(
        select(Route).where(col(Route.order_id) == order_id)
    )
    return result.scalars().first()


async def get_routes(
    db: AsyncSession,
    driver_id: Optional[int] = None,
    order_id: Optional[int] = None,
) -> Sequence[Route]:
    query = select(Route)
    if driver_id is not None:
        query = query.where(col(Route.driver_id) == driver_id)
    if order_id is not None:
        query = query.where(col(Route.order_id) == order_id)
    result = await db.execute(query)
    return result.scalars().all()


async def create_route(db: AsyncSession, route_in: RouteCreate) -> Route:
    db_route = Route(
        order_id=route_in.order_id,
        driver_id=route_in.driver_id,
        eta=route_in.eta,
    )
    db.add(db_route)
    await db.commit()
    await db.refresh(db_route)
    return db_route


async def update_route(
    db: AsyncSession, route: Route, route_in: RouteUpdate
) -> Route:
    update_data = route_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(route, field, value)
    db.add(route)
    await db.commit()
    await db.refresh(route)
    return route


async def delete_route(db: AsyncSession, route: Route) -> None:
    await db.delete(route)
    await db.commit()
