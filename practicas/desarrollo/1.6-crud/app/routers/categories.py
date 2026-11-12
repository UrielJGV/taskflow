"""CRUD de categorías, tareas asociadas y contadores."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response
from sqlalchemy import case, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Category, Task
from app.schemas import (
    CategoryCreate,
    CategoryDetail,
    CategoryRead,
    CategorySummary,
    CategoryUpdate,
    PaginatedResponse,
)


router = APIRouter(prefix="/categories", tags=["categories"])

DatabaseSession = Annotated[Session, Depends(get_db)]
PositiveId = Annotated[int, Path(gt=0)]


def find_category(db: Session, category_id: int) -> Category:
    """Busca una categoría o devuelve un error 404."""

    category = db.get(Category, category_id)

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada.",
        )

    return category


def validate_name(
    db: Session,
    name: str,
    exclude_id: int | None = None,
) -> None:
    """Comprueba que otra categoría no utiliza el mismo nombre."""

    statement = select(Category.id).where(Category.name == name)

    if exclude_id is not None:
        statement = statement.where(Category.id != exclude_id)

    if db.scalar(statement.limit(1)) is not None:
        raise HTTPException(
            status_code=409,
            detail="Ya existe una categoría con ese nombre.",
        )


def commit_changes(db: Session) -> None:
    """Confirma los cambios y gestiona conflictos de integridad."""

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=(
                "Conflicto de integridad. Comprueba el nombre "
                "de la categoría y sus tareas asociadas."
            ),
        ) from None


@router.get(
    "",
    response_model=PaginatedResponse[CategoryRead],
    summary="Listar categorías",
)
def list_categories(
    db: DatabaseSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    sort_by: Literal["id", "name"] = "id",
    order: Literal["asc", "desc"] = "asc",
):
    """Devuelve una página de categorías con el total de registros."""

    total = db.scalar(
        select(func.count()).select_from(Category)
    )

    sort_columns = {
        "id": Category.id,
        "name": Category.name,
    }
    sort_column = sort_columns[sort_by]
    ordering = (
        sort_column.desc()
        if order == "desc"
        else sort_column.asc()
    )

    statement = select(Category).order_by(ordering)

    if sort_by != "id":
        statement = statement.order_by(Category.id.asc())

    statement = statement.offset(skip).limit(limit)

    return {
        "items": db.scalars(statement).all(),
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get(
    "/{category_id}/summary",
    response_model=CategorySummary,
    summary="Consultar contadores de una categoría",
)
def get_category_summary(
    category_id: PositiveId,
    db: DatabaseSession,
):
    """Calcula los contadores en SQL sin cargar todas las tareas."""

    category = find_category(db, category_id)

    statement = (
        select(
            func.count(Task.id),
            func.coalesce(
                func.sum(
                    case(
                        (Task.completed.is_(True), 1),
                        else_=0,
                    )
                ),
                0,
            ),
        )
        .where(Task.category_id == category_id)
    )

    total_tasks, completed_tasks = db.execute(statement).one()

    return {
        **CategoryRead.model_validate(category).model_dump(),
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": total_tasks - completed_tasks,
    }


@router.get(
    "/{category_id}",
    response_model=CategoryDetail,
    summary="Consultar una categoría con sus tareas",
)
def get_category(
    category_id: PositiveId,
    db: DatabaseSession,
):
    statement = (
        select(Category)
        .where(Category.id == category_id)
        .options(selectinload(Category.tasks))
    )

    category = db.scalar(statement)

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada.",
        )

    return category


@router.post(
    "",
    response_model=CategoryRead,
    status_code=201,
    summary="Crear una categoría",
)
def create_category(
    data: CategoryCreate,
    db: DatabaseSession,
):
    validate_name(db, data.name)

    category = Category(**data.model_dump())

    db.add(category)
    commit_changes(db)
    db.refresh(category)

    return category


@router.put(
    "/{category_id}",
    response_model=CategoryRead,
    summary="Modificar una categoría",
)
def update_category(
    category_id: PositiveId,
    data: CategoryUpdate,
    db: DatabaseSession,
):
    category = find_category(db, category_id)
    validate_name(db, data.name, exclude_id=category_id)

    category.name = data.name

    commit_changes(db)
    db.refresh(category)

    return category


@router.delete(
    "/{category_id}",
    status_code=204,
    response_class=Response,
    summary="Eliminar una categoría sin tareas",
)
def delete_category(
    category_id: PositiveId,
    db: DatabaseSession,
):
    category = find_category(db, category_id)

    associated_task = db.scalar(
        select(Task.id)
        .where(Task.category_id == category_id)
        .limit(1)
    )

    if associated_task is not None:
        raise HTTPException(
            status_code=409,
            detail=(
                "No se puede eliminar una categoría con tareas. "
                "Reasigna o elimina sus tareas primero."
            ),
        )

    db.delete(category)
    commit_changes(db)

    return Response(status_code=204)