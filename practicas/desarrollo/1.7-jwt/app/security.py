"""Hash de contraseñas y creación de tokens JWT."""

import os
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")

if len(SECRET_KEY.encode("utf-8")) < 32:
    raise RuntimeError(
        "Configura JWT_SECRET_KEY con una clave aleatoria "
        "de al menos 32 bytes antes de arrancar la API."
    )


password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__truncate_error=True,
)


def hash_password(password: str) -> str:
    """Genera un hash bcrypt con una sal aleatoria."""
    password_bytes = password.encode("utf-8")

    if len(password) < 12:
        raise ValueError(
            "La contraseña debe tener al menos 12 caracteres."
        )

    if len(password_bytes) > 72:
        raise ValueError(
            "La contraseña no puede superar 72 bytes en UTF-8."
        )

    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Comprueba una contraseña sin truncarla."""
    if len(password.encode("utf-8")) > 72:
        return False

    return password_context.verify(password, hashed_password)


def create_access_token(user_id: int) -> str:
    """Crea un token firmado con una duración de 30 minutos."""
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )