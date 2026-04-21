from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.enum import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole
    phone_number: str = Field(..., example="+380991234567")


class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    full_name: str
    phone_number: str
    created_at: datetime

    class Config:
        from_attributes = True
