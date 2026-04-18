from enum import Enum

from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    SENDER = "sender"
    DRIVER = "driver"
    RECEIVER = "receiver"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    full_name: str

    class Config:
        from_attributes = True
