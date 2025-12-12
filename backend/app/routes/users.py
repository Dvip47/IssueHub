from fastapi import (
    APIRouter, Depends, HTTPException, status
)
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from ..db import get_db
from ..schemas.user import UserOut
from ..models.user import User

from ..core.security import settings, jwt, JWTError



router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = "/api/auth/login"
)



def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_error = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = { "WWW-Authenticate": "Bearer" }
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms = [settings.ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_error

    except JWTError:
        raise credentials_error


    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        raise credentials_error

    return user



@router.get("", response_model = UserOut)
def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user