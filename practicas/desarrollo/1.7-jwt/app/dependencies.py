"""Dependencias para identificar al usuario mediante JWT."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import ALGORITHM, SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    auto_error=False,
)


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> User:
    """Valida la firma, la expiración y el usuario del token."""

    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_error

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={
                "require_exp": True,
                "require_sub": True,
                "verify_exp": True,
            },
        )

        subject = payload.get("sub")

        if not isinstance(subject, str):
            raise credentials_error

        # Los tokens creados por la aplicación usan el ID como texto.
        if (
            not subject.isascii()
            or not subject.isdecimal()
            or len(subject) > 19
        ):
            raise credentials_error

        user_id = int(subject)

        if not 1 <= user_id <= 9223372036854775807:
            raise credentials_error

    except (JWTError, ValueError, TypeError):
        raise credentials_error from None

    user = db.get(User, user_id)

    if user is None:
        raise credentials_error

    return user