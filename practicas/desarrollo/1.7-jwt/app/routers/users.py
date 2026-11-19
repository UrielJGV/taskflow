"""Consulta del usuario autenticado mediante JWT."""

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict

from app.dependencies import get_current_user
from app.models import User


class UserRead(BaseModel):
    """Datos públicos del usuario, sin contraseña ni hash."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/me",
    response_model=UserRead,
    summary="Consultar el usuario autenticado",
    description=(
        "Valida el token JWT y devuelve los datos públicos del usuario. "
        "Utiliza dependencias anidadas: get_current_user depende de get_db."
    ),
)
def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user