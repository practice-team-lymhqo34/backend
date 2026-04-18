import enum

from sqlalchemy import Column, Enum, Integer, String

from app.db.base_class import Base


class UserRole(str, enum.Enum):
    SENDER = "sender"
    DRIVER = "driver"
    RECEIVER = "receiver"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    full_name = Column(String)
