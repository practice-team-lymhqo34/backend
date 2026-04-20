import enum
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Enum, Field, SQLModel, func


class UserRole(str, enum.Enum):
    SENDER = "sender"
    DRIVER = "driver"
    RECEIVER = "receiver"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)

    role: UserRole = Field(
        sa_column=Column(Enum(UserRole, native_enum=False), nullable=False)
    )

    full_name: Optional[str] = None
    phone_number: str = Field(unique=True, index=True, nullable=False)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
