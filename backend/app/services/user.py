from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user import UserCreate
from ..core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return (
        db.query(User)
          .filter(User.email == email)
          .first()
    )


def create_user(db: Session, user: UserCreate):
    hashed = get_password_hash(user.password)

    record = User(
        email= user.email,
        hashed_password = hashed,
        name= user.name
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record
