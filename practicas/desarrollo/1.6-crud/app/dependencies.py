"""Dependencias compartidas de TaskFlow."""

from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[
        int,
        Header(
            alias="X-User-ID",
            gt=0,
            description=(
                "Identificador de usuario para demostrar dependencias "
                "anidadas. No constituye autenticación."
            ),
        ),
    ],
) -> User:
    """Busca el usuario indicado utilizando la sesión de get_db."""

    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )

    return user