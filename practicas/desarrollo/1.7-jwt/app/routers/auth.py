"""Registro de usuarios e inicio de sesión con JWT."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, ConfigDict, Field, SecretStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    hash_password,
    verify_password,
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


class RegisterRequest(BaseModel):
    """Datos de registro; la contraseña conserva sus espacios."""

    model_config = ConfigDict(extra="forbid")

    username: str = Field(
        min_length=3,
        max_length=100,
        pattern=r"^[a-zA-Z0-9_.-]+$",
        examples=["uriel"],
    )
    email: str = Field(
        min_length=3,
        max_length=254,
        pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
        examples=["uriel@example.com"],
    )
    password: SecretStr = Field(
        min_length=12,
        max_length=72,
    )


class UserResponse(BaseModel):
    """Datos públicos: nunca devuelve contraseñas ni hashes."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# Permite comprobar un hash incluso si el usuario no existe.
# Reduce las diferencias de tiempo entre ambos casos.
DUMMY_HASH = hash_password("Clave-ficticia-para-verificacion-123!")


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un usuario",
)
def register(
    data: RegisterRequest,
    db: Annotated[Session, Depends(get_db)],
):
    password = data.password.get_secret_value()

    try:
        hashed_password = hash_password(password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from None

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hashed_password,
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo completar el registro con esos datos.",
        ) from None

    db.refresh(user)
    return user


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión y obtener un token",
)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = db.scalar(
        select(User).where(User.username == form.username)
    )

    stored_hash = (
        user.hashed_password
        if user is not None
        else DUMMY_HASH
    )

    password_is_valid = verify_password(
        form.password,
        stored_hash,
    )

    if user is None or not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(
        access_token=create_access_token(user.id),
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )