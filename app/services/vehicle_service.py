from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import vehicle as crud_vehicle
from app.models.user import User
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


class VehicleService:
    async def get_driver_vehicles(self, db: AsyncSession, driver_id: int):
        return await crud_vehicle.get_vehicles_by_driver(db, driver_id)

    async def get_vehicle_or_404(self, db: AsyncSession, vehicle_id: int):
        vehicle = await crud_vehicle.get_vehicle_by_id(db, vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return vehicle

    async def add_vehicle(
        self, db: AsyncSession, vehicle_in: VehicleCreate, current_user: User
    ):
        existing = await crud_vehicle.get_vehicle_by_plate(
            db, vehicle_in.license_plate
        )
        if existing:
            raise HTTPException(
                status_code=409, detail="License plate already registered"
            )
        return await crud_vehicle.create_vehicle(
            db, vehicle_in, current_user.id
        )

    async def update_vehicle(
        self,
        db: AsyncSession,
        vehicle_id: int,
        data: VehicleUpdate,
        current_user: User,
    ):
        vehicle = await self.get_vehicle_or_404(db, vehicle_id)
        self._check_ownership(vehicle, current_user)

        if data.current_mileage is not None:
            if data.current_mileage < vehicle.current_mileage:
                raise HTTPException(
                    status_code=400,
                    detail="New mileage cannot be less than current mileage",
                )

        return await crud_vehicle.update_vehicle(db, vehicle, data)

    async def remove_vehicle(
        self, db: AsyncSession, vehicle_id: int, current_user: User
    ):
        vehicle = await self.get_vehicle_or_404(db, vehicle_id)
        self._check_ownership(vehicle, current_user)
        await crud_vehicle.delete_vehicle(db, vehicle)

    def _check_ownership(self, vehicle, current_user: User):
        if vehicle.driver_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not your vehicle")


vehicle_service = VehicleService()
