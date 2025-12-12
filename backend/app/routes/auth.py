from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from datetime import timedelta

from ..db import get_db
from ..schemas.user import UserCreate, Token
from ..services.user import create_user, get_user_by_email
from ..core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/signup", response_model = Token)
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    print(user)

    existing = get_user_by_email(db, user.email)
    print(existing)

    if existing:
        raise HTTPException(
            status_code = 400,
            detail = "Email already registered"
        )

    create_user(db, user)
    token = create_access_token(data = { "sub": user.email })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/login", response_model = Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = { "WWW-Authenticate": "Bearer" }
        )

    token = create_access_token(data = { "sub": user.email })

    return {
        "access_token": token,
        "token_type": "bearer"
    }