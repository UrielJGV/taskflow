# TaskFlow — Prácticas de desarrollo y despliegue

Proyecto educativo de una API de tareas y proyectos con FastAPI.

El repositorio reúne las prácticas de desarrollo y despliegue, organizadas en carpetas independientes. Cada carpeta contiene el código o la documentación correspondiente a esa entrega.

Las primeras versiones se recuperaron del historial de Git para conservar la evolución del proyecto. Las siguientes prácticas continúan esa evolución dentro de su propia carpeta.

## Índice de prácticas

### Desarrollo de aplicaciones web usando frameworks

| Práctica | Contenido | Origen |
| --- | --- | --- |
| [1.1 — Primeros endpoints](practicas/desarrollo/1.1-primeros-endpoints/) | Estructura inicial y endpoints de salud, versión y conectividad. | Commit `418d284` |
| [1.2 — Modelado con Pydantic](practicas/desarrollo/1.2-pydantic/) | Esquemas, validación y creación simulada de tareas. | Commit `5484701` |
| [1.3 — Organización con APIRouter](practicas/desarrollo/1.3-apirouter/) | Rutas separadas por recurso y documentación Swagger agrupada. | Commit `ebbc322` |
| [1.4 — Middleware](practicas/desarrollo/1.4-middleware/) | CORS, tiempo de procesamiento, trazabilidad y manejo global de errores. | Evolución de la práctica 1.3 |
| [1.5 — SQLAlchemy y base de datos](practicas/desarrollo/1.5-sqlalchemy/) | Modelos relacionados, persistencia en SQLite, sesiones por petición y dependencias anidadas. | Evolución de la práctica 1.4 |

### Despliegue de aplicaciones web

| Práctica | Contenido | Origen |
| --- | --- | --- |
| [1.1 — Preparar el servidor base](practicas/despliegue/1.1-servidor-base/) | Ubuntu Server, máquina virtual y acceso SSH. | Repositorio original de Despliegue |
| [1.2 — Instalación básica de Apache](practicas/despliegue/1.2-apache/) | Servidor web Apache y comprobación del puerto 80. | Repositorio original de Despliegue |
| [1.3 — Instalación de Gunicorn](practicas/despliegue/1.3-gunicorn/) | Ejecución del backend en Ubuntu Server. | Commit `e7ada53` |
| [1.4 — Docker y primer contenedor](practicas/despliegue/1.4-docker/) | Imagen Docker, contenedor y comparación de arquitecturas. | Commit `17c5cd6` |

La numeración se repite porque las prácticas pertenecen a módulos distintos.

## Cómo consultar el repositorio

1. Seleccionar el módulo y la práctica en las tablas anteriores.
2. Leer su README y la documentación asociada.
3. Consultar el código de esa entrega, cuando corresponda.
4. Instalar las dependencias de su propio `requirements.txt`.
5. Ejecutar los comandos desde la carpeta de esa práctica.

Las prácticas de desarrollo contienen copias independientes de su código. No necesitan importar archivos de otras carpetas de prácticas.

Los entornos virtuales no se incluyen en Git: deben crearse en el equipo donde se vaya a ejecutar cada ejercicio.

Las primeras prácticas de despliegue contienen documentación y evidencias de la configuración del servidor.

## Práctica más reciente: SQLAlchemy

La [práctica 1.5 de desarrollo](practicas/desarrollo/1.5-sqlalchemy/) incorpora:

- Modelos `Task`, `Project`, `User` y `Category`.
- Relaciones mediante claves foráneas y `back_populates`.
- Comportamientos de eliminación definidos en los modelos.
- Persistencia de proyectos, tareas y usuarios de prueba en SQLite.
- Una sesión por petición mediante `get_db`.
- Consultas con paginación y filtro de tareas por proyecto.
- Dependencias anidadas mediante `get_current_user` y `get_db`.
- Creación de las tablas al arrancar la aplicación.
- Documentación del modelo de datos y de las comprobaciones funcionales.

Las relaciones opcionales con usuarios y categorías están definidas en los modelos. La API de tareas todavía no permite asignarlas mediante sus esquemas de entrada.

La cabecera `X-User-ID` se utiliza para demostrar dependencias anidadas; no constituye un sistema de autenticación.

### Ejecución en Windows

Desde la raíz del repositorio:

```powershell
cd .\practicas\desarrollo\1.5-sqlalchemy
```

Crear el entorno virtual si todavía no existe:

```powershell
py -m venv .venv
```

Instalar las dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Arrancar la API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8003
```

Abrir la documentación interactiva:

http://127.0.0.1:8003/docs

El archivo `taskflow.db` y las tablas se crean al arrancar. La base de datos local está excluida de Git.

## Documentación disponible

- [Servidor base](practicas/despliegue/1.1-servidor-base/README.md)
- [Instalación de Apache](practicas/despliegue/1.2-apache/docs/apache.md)
- [Organización con APIRouter](practicas/desarrollo/1.3-apirouter/docs/routers.md)
- [Middleware](practicas/desarrollo/1.4-middleware/README.md)
- [SQLAlchemy y conexión a base de datos](practicas/desarrollo/1.5-sqlalchemy/README.md)
- [Instalación de Gunicorn](practicas/despliegue/1.3-gunicorn/docs/gunicorn.md)
- [Docker y comparación de arquitecturas](practicas/despliegue/1.4-docker/docs/arquitectura.md)

Algunos documentos describen el proceso original y pueden mencionar las ubicaciones de trabajo utilizadas durante las prácticas.

Para ejecutar las copias organizadas, hay que situarse en la carpeta concreta del ejercicio.

## Evidencias

Las capturas de las pruebas se recogen en los documentos de entrega correspondientes.

Las evidencias incorporadas al repositorio para las primeras prácticas de despliegue están disponibles aquí:

- [Evidencias del servidor base](practicas/despliegue/1.1-servidor-base/evidencias-servidor-base.pdf)
- [Evidencias de Apache](practicas/despliegue/1.2-apache/docs/evidencias-apache.pdf)

Las capturas de otras prácticas pueden estar en los documentos entregados por Classroom. Recuperar una versión del código desde Git no incorpora automáticamente esas capturas.

## Estado del proyecto original

La carpeta `app/` situada en la raíz conserva la versión de trabajo utilizada antes de organizar las prácticas.

También se mantienen los archivos de despliegue y la documentación originales.

Las entregas separadas y sus instrucciones se consultan desde `practicas/`. Para ejecutar la versión con persistencia, debe utilizarse la carpeta `practicas/desarrollo/1.5-sqlalchemy/`.

## Evolución y alcance

Las primeras versiones utilizan operaciones simuladas de creación de tareas y proyectos.

La práctica 1.5 añade persistencia real en SQLite. Este cambio pertenece a su carpeta y no modifica las versiones anteriores.

La reorganización conserva el código de cada entrega; no implica que todas las versiones históricas hayan vuelto a ejecutarse después de exportarlas.

Las decisiones de diseño y las limitaciones de cada práctica están documentadas en su propio README.