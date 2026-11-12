"""Rutas de usuarios y demostración de dependencias anidadas."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import SchemaBase


class UserCreate(SchemaBase):
    """Datos necesarios para registrar un usuario de prueba."""

    username: str = Field(
        min_length=1,
        max_length=100,
        examples=["uriel"],
    )
    email: str = Field(
        min_length=3,
        max_length=254,
        examples=["uriel@example.com"],
    )


class UserRead(UserCreate):
    """Datos públicos del usuario."""

    id: int = Field(gt=0)


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un usuario de prueba",
)
def create_user(
    user: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    """Guarda un usuario con nombre y correo únicos."""

    new_user = User(
        username=user.username,
        email=user.email,
    )

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese nombre o correo.",
        ) from None

    db.refresh(new_user)

    return new_user


@router.get(
    "/me",
    response_model=UserRead,
    summary="Consultar el usuario indicado en X-User-ID",
    description=(
        "Demuestra dependencias anidadas: la ruta utiliza "
        "get_current_user, que utiliza get_db. "
        "La cabecera X-User-ID no constituye autenticación."
    ),
)
def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Devuelve el usuario obtenido por la dependencia."""

    return current_user