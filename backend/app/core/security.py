from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings



pwd_context = CryptContext(
    schemes = ["bcrypt"],
    deprecated = "auto"
)



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



def get_password_hash(password):
    return pwd_context.hash(password)



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    payload = data.copy()

    if expires_delta:
        expire_at = datetime.utcnow() + expires_delta
    else:
        expire_at = datetime.utcnow() + timedelta(
            minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload.update({ "exp": expire_at })

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm = settings.ALGORITHM
    )

    return token