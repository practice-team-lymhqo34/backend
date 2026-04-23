from fastapi import APIRouter

from app.api.v1.routes import auth, sender

api_router = APIRouter()


@api_router.get("/health", tags=["system"])
async def health_check():
    return {"status": "ok"}


api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(sender.router, prefix="/sender", tags=["sender"])
