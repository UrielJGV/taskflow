\# Práctica 1.5 — Modelos SQLAlchemy y conexión a base de datos



\## Objetivo



Añadir persistencia real a TaskFlow mediante SQLAlchemy y SQLite.



Los proyectos y las tareas se guardan en `taskflow.db` y permanecen disponibles después de detener y volver a iniciar la API.



Esta práctica continúa el trabajo de routers, validación con Pydantic y middleware de las actividades anteriores.



\## Tecnologías



\- Python.

\- FastAPI.

\- SQLAlchemy 2.1.8.

\- SQLite.

\- Pydantic.

\- Uvicorn.



Las versiones de las dependencias están declaradas en `requirements.txt`.



\## Archivos principales



| Archivo | Responsabilidad |

| --- | --- |

| `app/database.py` | Configura el motor, las sesiones y la dependencia `get\_db`. |

| `app/models.py` | Define las tablas y relaciones de SQLAlchemy. |

| `app/schemas.py` | Define los contratos de entrada y salida de tareas y proyectos. |

| `app/dependencies.py` | Implementa la dependencia anidada `get\_current\_user`. |

| `app/main.py` | Configura FastAPI, registra routers y prepara las tablas al arrancar. |

| `app/routers/projects.py` | Crea y consulta proyectos en SQLite. |

| `app/routers/tasks.py` | Crea y consulta tareas en SQLite. |

| `app/routers/users.py` | Define los esquemas y las rutas de usuarios de prueba. |

| `app/routers/status.py` | Conserva las rutas de estado de la aplicación. |

| `app/middleware.py` | Añade tiempo de procesamiento y trazabilidad. |

| `app/errors.py` | Gestiona las excepciones no controladas. |



\## Decisiones de diseño



El enunciado solicita los modelos Task, Project, User y Category.



Al no disponer de una especificación detallada adicional, se conservan los campos de tareas y proyectos de las prácticas anteriores y se proponen las siguientes relaciones:



\- Cada tarea pertenece obligatoriamente a un proyecto.

\- Un proyecto puede tener varias tareas.

\- Una tarea puede tener un usuario asignado o ninguno.

\- Una tarea puede tener una categoría o ninguna.

\- Un usuario puede tener varias tareas asignadas.

\- Una categoría puede agrupar varias tareas.

\- Los proyectos son compartidos: no se aplica un filtro de propietario.



Las asociaciones opcionales con usuarios y categorías están definidas en la base de datos. La API de tareas de esta entrega todavía no permite asignarlas mediante sus esquemas de entrada.



\## Diagrama de la base de datos



```mermaid

erDiagram

&#x20;   PROJECT ||--o{ TASK : contiene

&#x20;   USER o|--o{ TASK : tiene\_asignadas

&#x20;   CATEGORY o|--o{ TASK : clasifica



&#x20;   PROJECT {

&#x20;       int id PK

&#x20;       string name

&#x20;       string description

&#x20;       datetime created\_at

&#x20;   }



&#x20;   TASK {

&#x20;       int id PK

&#x20;       string title

&#x20;       string description "Opcional"

&#x20;       boolean completed

&#x20;       datetime created\_at

&#x20;       int project\_id FK

&#x20;       int assignee\_id FK "Opcional"

&#x20;       int category\_id FK "Opcional"

&#x20;   }



&#x20;   USER {

&#x20;       int id PK

&#x20;       string username UK

&#x20;       string email UK

&#x20;   }



&#x20;   CATEGORY {

&#x20;       int id PK

&#x20;       string name UK

&#x20;   }

```



\## Modelos y relaciones



Los modelos heredan de `Base`, definida mediante `DeclarativeBase`.



Cada clase representa una tabla. Sus atributos, declarados con `Mapped` y `mapped\_column`, representan las columnas.



Las claves primarias identifican cada registro y las claves foráneas conectan las tablas.



`relationship` permite trabajar con los objetos relacionados desde Python. `back\_populates` conecta ambos extremos de cada relación; por ejemplo, `project.tasks` y `task.project`.



\### Comportamiento al eliminar registros



\- Eliminar un proyecto elimina sus tareas mediante `ON DELETE CASCADE`.

\- La relación `Project.tasks` utiliza `cascade="all, delete-orphan"`. También permite eliminar una tarea cuando se retira de la colección del proyecto mediante el ORM.

\- Eliminar un usuario conserva sus tareas y deja `assignee\_id` a NULL.

\- Eliminar una categoría conserva sus tareas y deja `category\_id` a NULL.



Estos comportamientos están definidos en los modelos. Esta entrega no incorpora endpoints DELETE.



Las fechas se generan en UTC y se almacenan sin información de zona horaria, siguiendo una convención común para todas las tablas de esta práctica.



\## Configuración de SQLite



`app/database.py` define el motor `engine`.



Por defecto, el archivo `taskflow.db` se guarda en la raíz de esta práctica. La ruta se calcula a partir de la ubicación de `database.py`, evitando depender de la carpeta desde la que se lance el proceso.



La configuración incluye:



\- `check\_same\_thread=False`: permite utilizar conexiones SQLite desde los diferentes hilos que pueden intervenir al atender peticiones. No convierte una sesión en un objeto seguro para compartir entre peticiones.

\- `timeout`: establece cuánto espera SQLite cuando la base de datos está bloqueada.

\- `pool\_pre\_ping=True`: comprueba la disponibilidad de una conexión al obtenerla del pool.

\- `PRAGMA foreign\_keys=ON`: activa la comprobación de claves foráneas en cada nueva conexión.



\### Variables de entorno



| Variable | Valor por defecto | Finalidad |

| --- | --- | --- |

| `DATABASE\_URL` | URL SQLite del archivo local `taskflow.db` | Seleccionar la base de datos SQLite. |

| `SQLITE\_TIMEOUT` | `10` | Espera ante bloqueos, en segundos. |

| `CORS\_ORIGINS` | `http://localhost:5173` | Orígenes permitidos, separados por comas. |

| `ENABLE\_DEBUG\_ROUTES` | `false` | Activar las rutas de prueba de errores. |



La configuración de esta práctica admite URLs SQLite. Para cambiar de gestor habría que adaptar también las opciones específicas de SQLite.



\## Sesiones y pooling



El motor administra las conexiones a la base de datos. El pool permite reutilizarlas en lugar de abrir una conexión nueva para cada operación.



Una sesión de SQLAlchemy representa una unidad de trabajo; no equivale a una conexión permanentemente reservada.



`SessionLocal` crea las sesiones con:



\- `autoflush=False`: evita el vaciado automático antes de determinadas consultas. `commit()` sigue enviando los cambios pendientes.

\- `expire\_on\_commit=False`: mantiene los atributos cargados tras confirmar una transacción.



\### Dependencia get\_db



Cada petición que necesita la base de datos obtiene una sesión mediante `Depends(get\_db)`.



La dependencia:



1\. Crea la sesión.

2\. La entrega mediante `yield`.

3\. Ejecuta `rollback()` si se propaga una excepción.

4\. Ejecuta `close()` en el bloque `finally`.



Cerrar la sesión libera los recursos y devuelve al pool las conexiones utilizadas.



Las rutas de proyectos, tareas y usuarios utilizan esta dependencia directa o indirectamente. Las rutas de estado y las de depuración que no consultan datos no necesitan una sesión.



\## Inicio y cierre de la aplicación



Se utiliza `lifespan` en FastAPI.



Al iniciar:



\- Se importan los modelos para registrarlos.

\- Se ejecuta `Base.metadata.create\_all(bind=engine)`.



Al cerrar:



\- Se ejecuta `engine.dispose()` para liberar las conexiones del pool.



`create\_all()` crea las tablas que faltan. No borra los datos existentes ni realiza migraciones de tablas ya creadas. Para evolucionar una base de datos existente sería necesario un sistema de migraciones, como Alembic.



\## Pydantic y SQLAlchemy



SQLAlchemy define cómo se almacenan los datos.



Pydantic define qué datos acepta y devuelve la API.



Los esquemas utilizan `from\_attributes=True`, lo que permite construir respuestas a partir de los atributos de los objetos ORM.



La validación de longitudes de los campos de entrada se realiza en Pydantic. En SQLite, declarar `String(100)` no impone por sí solo un límite de 100 caracteres.



\## Endpoints implementados



| Método | Ruta | Función |

| --- | --- | --- |

| POST | `/projects` | Crear un proyecto. |

| GET | `/projects` | Listar proyectos con paginación. |

| GET | `/projects/{project\_id}` | Consultar un proyecto. |

| POST | `/tasks` | Crear una tarea para un proyecto existente. |

| GET | `/tasks` | Listar tareas, con paginación y filtro opcional por proyecto. |

| GET | `/tasks/{task\_id}` | Consultar una tarea. |

| POST | `/users` | Crear un usuario de prueba. |

| GET | `/users/me` | Consultar el usuario indicado mediante `X-User-ID`. |



Se conservan también las rutas de estado de las prácticas anteriores.



\## Dependencias anidadas



La ruta `GET /users/me` utiliza `get\_current\_user`.



A su vez, `get\_current\_user` utiliza `get\_db` para consultar el usuario en SQLite.



La cabecera `X-User-ID` debe contener un identificador positivo de un usuario existente.



Esta funcionalidad demuestra dependencias anidadas. No constituye autenticación: el cliente puede indicar otro identificador. No hay contraseñas ni verificación de identidad en esta entrega.



\## Instalación y ejecución en Windows



Desde la raíz del repositorio:



```powershell

cd .\\practicas\\desarrollo\\1.5-sqlalchemy

```



Crear el entorno virtual si todavía no existe:



```powershell

py -m venv .venv

```



Instalar las dependencias:



```powershell

.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt

```



Arrancar la aplicación:



```powershell

.\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --reload --port 8003

```



Abrir Swagger:



http://127.0.0.1:8003/docs



Para detener el servidor, pulsar Ctrl + C.



El archivo SQLite y las tablas se crean automáticamente al arrancar.



\## Comprobaciones funcionales



Las capturas de las pruebas se recogen en el documento de evidencias de la práctica.



\### 1. Crear un proyecto



Realizar POST a `/projects`:



```json

{

&#x20; "name": "Práctica 1.5 SQLAlchemy",

&#x20; "description": "Proyecto para comprobar la persistencia de tareas en SQLite."

}

```



Resultado esperado: HTTP 201, identificador generado y fecha de creación.



\### 2. Crear una tarea



Realizar POST a `/tasks`, sustituyendo `project\_id` por el identificador obtenido:



```json

{

&#x20; "title": "Comprobar la persistencia",

&#x20; "description": "Verificar que la tarea permanece después del reinicio.",

&#x20; "project\_id": 1

}

```



Resultado esperado: HTTP 201, identificador generado y `completed` igual a `false`.



\### 3. Comprobar la persistencia



Detener Uvicorn y volver a iniciarlo.



Consultar GET `/projects` y GET `/tasks`.



Resultado esperado: HTTP 200 y los registros creados antes del reinicio.



\### 4. Proyecto inexistente



Intentar crear una tarea con un identificador de proyecto que no exista.



Resultado esperado: HTTP 404 con el mensaje:



```json

{

&#x20; "detail": "El proyecto indicado no existe."

}

```



Comprobar después que la tarea no aparece en GET `/tasks`.



\### 5. Dependencias anidadas



Crear un usuario mediante POST `/users`:



```json

{

&#x20; "username": "uriel",

&#x20; "email": "uriel@example.com"

}

```



Consultar GET `/users/me`, indicando su identificador en `X-User-ID`.



Resultado esperado: HTTP 200 con los datos del usuario.



El correo es un dato de ejemplo; la aplicación no envía mensajes.



\## ORM frente a SQL directo



Un ORM permite representar registros como objetos y expresar consultas mediante código Python.



En esta práctica, `db.get(Project, project\_id)` consulta un proyecto por su clave primaria y devuelve una instancia de `Project`.



Ventajas del ORM:



\- Organiza las tablas mediante clases.

\- Facilita el trabajo con relaciones.

\- Integra consultas y transacciones en la aplicación.

\- Reduce el SQL repetitivo.



El ORM no elimina la necesidad de comprender SQL, índices, transacciones y costes de las consultas.



El SQL directo puede ser apropiado para consultas especializadas, informes complejos u optimizaciones concretas. Debe utilizar parámetros enlazados, evitando concatenar valores proporcionados por el usuario.



Ambos enfoques pueden coexistir. En esta práctica se utiliza el ORM para las operaciones de negocio y SQL directo para comprobar o configurar aspectos de SQLite, como `PRAGMA foreign\_keys`.



\## Control de versiones



Se versionan el código, las dependencias y la documentación.



Se excluyen:



\- El entorno virtual.

\- Los archivos de caché de Python.

\- La base de datos local `taskflow.db`.

\- Los archivos auxiliares de SQLite.



Así, cualquier persona puede instalar las dependencias y generar una base de datos nueva al arrancar la aplicación.



\## Alcance



Esta entrega incorpora persistencia de proyectos, tareas y usuarios de prueba.



Las categorías y las relaciones opcionales están preparadas en los modelos para su desarrollo posterior.



Las decisiones propuestas sobre usuarios y categorías quedan documentadas y podrán adaptarse si se facilita una especificación adicional del proyecto.

