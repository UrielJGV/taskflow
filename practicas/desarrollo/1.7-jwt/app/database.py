"""Conexión SQLite y gestión de sesiones por petición."""

import os
from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


# Sitúa la base de datos en la carpeta de esta práctica.
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{(BASE_DIR / 'taskflow.db').as_posix()}",
)

SQLITE_TIMEOUT = float(os.getenv("SQLITE_TIMEOUT", "10"))


class Base(DeclarativeBase):
    """Clase base de los modelos que se convertirán en tablas."""

    pass


# Esta práctica utiliza SQLite mediante el controlador sqlite3.
if not DATABASE_URL.startswith(("sqlite:///", "sqlite+pysqlite:///")):
    raise ValueError("Esta práctica requiere una URL de SQLite.")


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": SQLITE_TIMEOUT,
    },
    pool_pre_ping=True,
)


@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    """Activa la comprobación de claves foráneas en cada conexión."""

    # PRAGMA debe ejecutarse fuera de una transacción.
    has_autocommit = hasattr(dbapi_connection, "autocommit")
    if has_autocommit:
        previous_autocommit = dbapi_connection.autocommit
        dbapi_connection.autocommit = True

    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys=ON")
    finally:
        cursor.close()
        if has_autocommit:
            dbapi_connection.autocommit = previous_autocommit


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Proporciona una sesión independiente y garantiza su cierre."""

    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()