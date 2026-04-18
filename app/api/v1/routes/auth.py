from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.api import deps
from app.core.security import create_access_token, verify_password
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserOut

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(deps.get_db)):
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud_user.create_user(db, user_in)


@router.post("/login")
def login(
    response: Response, user_in: UserCreate, db: Session = Depends(deps.get_db)
):
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )

    token = create_access_token(data={"sub": user.email, "role": user.role})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        samesite="lax",
        secure=False,
    )
    return {"message": "Logged in successfully", "role": user.role}
