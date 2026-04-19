from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str):
    # Використовуй .first(), як у тебе і було
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_in: UserCreate):
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        full_name=user_in.full_name,
        phone_number=user_in.phone_number,  # Це поле тепер є в моделі та схемі
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
