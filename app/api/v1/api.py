from fastapi import APIRouter

from app.api.v1.routes import auth, order, dashboard

api_router = APIRouter()


@api_router.get("/health", tags=["system"])
async def health_check():
    return {"status": "ok"}


api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(
    dashboard.router, prefix="/dashboard", tags=["dashboard"]
)
api_router.include_router(order.router, prefix="/orders", tags=["orders"])
