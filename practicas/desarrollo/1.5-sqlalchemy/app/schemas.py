"""Contratos de entrada y salida de la API TaskFlow."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SchemaBase(BaseModel):
    """Configuración compartida por los esquemas."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
        from_attributes=True,
    )


class TaskCreate(SchemaBase):
    """Datos que envía el cliente para crear una tarea."""

    title: str = Field(
        min_length=1,
        max_length=100,
        description="Título obligatorio, entre 1 y 100 caracteres.",
        examples=["Preparar la práctica de SQLAlchemy"],
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Descripción opcional de la tarea.",
        examples=["Definir los modelos y probarlos en Swagger."],
    )
    project_id: int = Field(
        gt=0,
        description="Identificador positivo del proyecto.",
        examples=[1],
    )


class TaskRead(TaskCreate):
    """Datos que devuelve la API al consultar o crear una tarea."""

    id: int = Field(
        gt=0,
        description="Identificador de la tarea.",
        examples=[1],
    )
    completed: bool = Field(
        description="Indica si la tarea está completada.",
        examples=[False],
    )
    created_at: datetime = Field(
        description="Fecha y hora de creación en UTC.",
        examples=["2026-11-06T08:00:00"],
    )


class ProjectCreate(SchemaBase):
    """Datos que envía el cliente para crear un proyecto."""

    name: str = Field(
        min_length=1,
        max_length=100,
        description="Nombre obligatorio del proyecto.",
        examples=["TaskFlow"],
    )
    description: str = Field(
        min_length=1,
        max_length=1000,
        description="Descripción obligatoria del proyecto.",
        examples=["Aplicación para gestionar proyectos y tareas."],
    )


class ProjectRead(ProjectCreate):
    """Datos que devuelve la API sobre un proyecto."""

    id: int = Field(
        gt=0,
        description="Identificador del proyecto.",
        examples=[1],
    )
    created_at: datetime = Field(
        description="Fecha y hora de creación en UTC.",
        examples=["2026-11-06T08:00:00"],
    )