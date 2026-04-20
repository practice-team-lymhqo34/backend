import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserLogin, UserOut

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(
    user_in: UserCreate, db: AsyncSession = Depends(deps.get_db)
):
    user = await crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    return await crud_user.create_user(db, user_in)


@router.post("/login", response_model=UserOut)
async def login(
    response: Response,
    user_in: UserLogin,
    db: AsyncSession = Depends(deps.get_db),
):
    user = None
    if user_in.email:
        user = await crud_user.get_user_by_email(db, email=user_in.email)
    elif user_in.phone_number:
        user = await crud_user.get_user_by_phone(
            db, phone=user_in.phone_number
        )

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Incorrect email, phone or password"
        )

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    refresh_token = create_refresh_token(data={"sub": user.email})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=settings.COOKIE_SECURE,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        samesite="lax",
        secure=settings.COOKIE_SECURE,
        path="/api/v1/auth/refresh",
    )

    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=settings.COOKIE_SECURE,
    )
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        samesite="lax",
        secure=settings.COOKIE_SECURE,
        path="/api/v1/auth/refresh",
    )
    return {"status": "ok", "message": "Logged out successfully"}


@router.post("/refresh")
async def refresh_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(deps.get_db),
):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        email = payload.get("sub")
        user = await crud_user.get_user_by_email(db, email=email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        new_access_token = create_access_token(
            data={"sub": user.email, "role": user.role}
        )

        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            samesite="lax",
            secure=settings.COOKIE_SECURE,
        )
        return {"status": "ok", "message": "Token refreshed"}

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
