from typing import AsyncGenerator

import jwt
from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import SessionLocal
from app.enums import UserRole
from app.services.user_service import user_service


async def get_db() -> AsyncGenerator:
    async with SessionLocal() as db:
        yield db


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None),
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str | None = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await user_service.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


async def require_sender(user=Depends(get_current_user)):
    if user.role != UserRole.SENDER:
        raise HTTPException(status_code=403, detail="Sender role required")
    return user
