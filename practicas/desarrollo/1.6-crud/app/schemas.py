"""Esquemas de entrada y salida para el CRUD de TaskFlow."""

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


class SchemaBase(BaseModel):
    """Configuración compartida por los esquemas."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
        from_attributes=True,
    )


# TAREAS

class TaskCreate(SchemaBase):
    """Datos necesarios para crear una tarea."""

    title: str = Field(
        min_length=1,
        max_length=100,
        examples=["Preparar las pruebas del CRUD"],
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        examples=["Probar las operaciones desde Postman."],
    )
    project_id: int = Field(
        gt=0,
        description="Identificador del proyecto al que pertenece.",
        examples=[1],
    )
    category_id: int | None = Field(
        default=None,
        gt=0,
        description="Categoría opcional de la tarea.",
    )
    assignee_id: int | None = Field(
        default=None,
        gt=0,
        description="Usuario asignado opcional.",
    )


class TaskUpdate(TaskCreate):
    """Datos para sustituir los campos editables mediante PUT."""

    completed: bool = Field(
        description="Indica si la tarea está completada.",
        examples=[True],
    )


class TaskRead(TaskCreate):
    """Datos devueltos al consultar una tarea."""

    id: int = Field(gt=0)
    completed: bool
    created_at: datetime = Field(
        description="Fecha y hora de creación en UTC.",
    )


# PROYECTOS

class ProjectCreate(SchemaBase):
    """Datos necesarios para crear un proyecto."""

    name: str = Field(
        min_length=1,
        max_length=100,
        examples=["TaskFlow CRUD"],
    )
    description: str = Field(
        min_length=1,
        max_length=1000,
        examples=["Proyecto para probar tareas y categorías."],
    )


class ProjectUpdate(ProjectCreate):
    """Datos para sustituir los campos editables de un proyecto."""

    pass


class ProjectRead(ProjectCreate):
    """Datos básicos de un proyecto."""

    id: int = Field(gt=0)
    created_at: datetime = Field(
        description="Fecha y hora de creación en UTC.",
    )


class ProjectDetail(ProjectRead):
    """Detalle de un proyecto con sus tareas asociadas."""

    tasks: list[TaskRead] = Field(default_factory=list)


class ProjectSummary(ProjectRead):
    """Resumen de un proyecto con contadores de tareas."""

    total_tasks: int = Field(ge=0)
    completed_tasks: int = Field(ge=0)
    pending_tasks: int = Field(ge=0)


# CATEGORÍAS

class CategoryCreate(SchemaBase):
    """Datos necesarios para crear una categoría."""

    name: str = Field(
        min_length=1,
        max_length=100,
        examples=["Estudios"],
    )


class CategoryUpdate(CategoryCreate):
    """Datos para sustituir los campos editables de una categoría."""

    pass


class CategoryRead(CategoryCreate):
    """Datos básicos de una categoría."""

    id: int = Field(gt=0)


class CategoryDetail(CategoryRead):
    """Detalle de una categoría con sus tareas asociadas."""

    tasks: list[TaskRead] = Field(default_factory=list)


class CategorySummary(CategoryRead):
    """Resumen de una categoría con contadores de tareas."""

    total_tasks: int = Field(ge=0)
    completed_tasks: int = Field(ge=0)
    pending_tasks: int = Field(ge=0)


# PAGINACIÓN

ItemType = TypeVar("ItemType")


class PaginatedResponse(SchemaBase, Generic[ItemType]):
    """Página de resultados acompañada de sus metadatos."""

    items: list[ItemType]
    total: int = Field(
        ge=0,
        description="Total de registros que cumplen los filtros.",
    )
    skip: int = Field(
        ge=0,
        description="Número de registros omitidos.",
    )
    limit: int = Field(
        ge=1,
        le=100,
        description="Número máximo de registros solicitados.",
    )