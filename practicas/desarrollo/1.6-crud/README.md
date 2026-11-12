\# Práctica 1.6 — CRUD completo



\## Objetivo



Implementar operaciones reales de creación, listado, consulta, modificación y eliminación sobre tareas, proyectos y categorías.



La práctica continúa la versión 1.5 de TaskFlow y utiliza FastAPI, SQLAlchemy y SQLite.



Cada práctica mantiene su propia carpeta, entorno virtual y base de datos.



\## Funcionalidades



\- CRUD completo de tareas, proyectos y categorías.

\- Filtros combinables de tareas por proyecto, estado, categoría y usuario asignado.

\- Paginación mediante `skip` y `limit`.

\- Ordenación ascendente y descendente.

\- Metadatos de paginación en las respuestas.

\- Detalle de proyectos y categorías con sus tareas asociadas.

\- Resúmenes con contadores de tareas.

\- Borrado de proyectos en cascada.

\- Bloqueo del borrado de categorías con tareas.

\- Validación de datos y respuestas diferenciadas para errores.

\- Colección Postman con 22 peticiones.



\## Organización del código



| Archivo | Función |

| --- | --- |

| `app/database.py` | Motor SQLite, configuración de sesiones y dependencia `get\_db`. |

| `app/models.py` | Tablas, relaciones y reglas de eliminación. |

| `app/schemas.py` | Esquemas de entrada, salida, detalle, resumen y paginación. |

| `app/routers/tasks.py` | CRUD y filtros de tareas. |

| `app/routers/projects.py` | CRUD, detalle y contadores de proyectos. |

| `app/routers/categories.py` | CRUD, detalle y contadores de categorías. |

| `app/routers/users.py` | Usuarios de prueba de la práctica anterior. |

| `app/dependencies.py` | Dependencias compartidas. |

| `app/main.py` | Arranque, registro de routers y middleware. |

| `postman/TaskFlow-1.6-CRUD.postman\_collection.json` | Colección de peticiones para importar en Postman. |



\## Instalación y ejecución



Desde la raíz del repositorio:



```powershell

cd .\\practicas\\desarrollo\\1.6-crud

```



Crear el entorno virtual si todavía no existe:



```powershell

py -m venv .venv

```



Instalar las dependencias:



```powershell

.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt

```



Comprobar las dependencias:



```powershell

.\\.venv\\Scripts\\python.exe -m pip check

```



Arrancar la API:



```powershell

.\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --reload --port 8004

```



Documentación interactiva:



http://127.0.0.1:8004/docs



Para detener el servidor, pulsar Ctrl + C.



\## Base de datos



Se utiliza SQLite con un archivo local `taskflow.db`.



Al arrancar la aplicación, `Base.metadata.create\_all()` crea las tablas que falten. No modifica la estructura de tablas existentes ni realiza migraciones.



La práctica se inició con una base de datos nueva para aplicar las reglas de eliminación definidas en esta versión.



La dependencia `get\_db` proporciona una sesión por petición, realiza rollback ante excepciones y cierra la sesión mediante `finally`.



Las claves foráneas se activan en cada conexión mediante `PRAGMA foreign\_keys=ON`.



\## Relaciones



```mermaid

erDiagram

&#x20;   PROJECT ||--o{ TASK : contiene

&#x20;   CATEGORY o|--o{ TASK : clasifica

&#x20;   USER o|--o{ TASK : tiene\_asignadas

```



Cada tarea pertenece obligatoriamente a un proyecto. La categoría y el usuario asignado son opcionales.



Los proyectos son compartidos: no se filtran por propietario.



\### Reglas de eliminación



| Recurso | Comportamiento |

| --- | --- |

| Proyecto | Su eliminación borra también sus tareas mediante cascada. |

| Categoría | Su eliminación se bloquea mientras tenga tareas asociadas. |

| Usuario | La relación conserva las tareas y deja su usuario asignado a NULL. |



El proyecto representa el contexto al que pertenecen sus tareas. Por ello, se utiliza `ON DELETE CASCADE` y la cascada correspondiente del ORM.



Una categoría clasifica tareas que pueden pertenecer a distintos proyectos. Para evitar perder esa clasificación por accidente, se utiliza `ON DELETE RESTRICT`.



En `Category.tasks`, `passive\_deletes="all"` evita que el ORM desvincule automáticamente las tareas al borrar una categoría. La base de datos mantiene la restricción.



La ruta DELETE de categorías comprueba previamente si existen tareas y devuelve un mensaje claro. La restricción de la base de datos añade protección de integridad.



No se implementa un endpoint de borrado de usuarios en esta entrega.



\## Contrato de la API



\### Tareas



| Método | Ruta | Función |

| --- | --- | --- |

| GET | `/tasks` | Listar tareas con filtros y paginación. |

| GET | `/tasks/{task\_id}` | Consultar una tarea. |

| POST | `/tasks` | Crear una tarea. |

| PUT | `/tasks/{task\_id}` | Modificar sus campos editables. |

| DELETE | `/tasks/{task\_id}` | Eliminar una tarea. |



\### Proyectos



| Método | Ruta | Función |

| --- | --- | --- |

| GET | `/projects` | Listar proyectos con paginación. |

| GET | `/projects/{project\_id}` | Consultar un proyecto con sus tareas. |

| POST | `/projects` | Crear un proyecto. |

| PUT | `/projects/{project\_id}` | Modificar nombre y descripción. |

| DELETE | `/projects/{project\_id}` | Eliminar un proyecto y sus tareas. |

| GET | `/projects/{project\_id}/summary` | Consultar contadores de tareas. |



\### Categorías



| Método | Ruta | Función |

| --- | --- | --- |

| GET | `/categories` | Listar categorías con paginación. |

| GET | `/categories/{category\_id}` | Consultar una categoría con sus tareas. |

| POST | `/categories` | Crear una categoría. |

| PUT | `/categories/{category\_id}` | Modificar su nombre. |

| DELETE | `/categories/{category\_id}` | Eliminar una categoría sin tareas. |

| GET | `/categories/{category\_id}/summary` | Consultar contadores de tareas. |



\## Creación y modificación



Ejemplo de creación de una tarea:



```json

{

&#x20; "title": "Probar el CRUD completo",

&#x20; "description": "Comprobar las operaciones desde Postman.",

&#x20; "project\_id": 1,

&#x20; "category\_id": 1,

&#x20; "assignee\_id": null

}

```



Los identificadores relacionados deben existir. Si no existen, la API devuelve 404 con un mensaje que identifica el recurso que falta.



Las tareas nuevas se crean con `completed: false`.



Ejemplo de modificación mediante PUT:



```json

{

&#x20; "title": "CRUD comprobado",

&#x20; "description": "Tarea actualizada desde Postman.",

&#x20; "project\_id": 1,

&#x20; "category\_id": 1,

&#x20; "assignee\_id": null,

&#x20; "completed": true

}

```



PUT sustituye los campos editables. Los campos opcionales omitidos toman el valor `null`.



El identificador y la fecha de creación se conservan.



\## Filtros, ordenación y paginación



GET `/tasks` admite:



| Parámetro | Función |

| --- | --- |

| `project\_id` | Filtrar por proyecto. |

| `completed` | Filtrar tareas completadas o pendientes. |

| `category\_id` | Filtrar por categoría. |

| `assignee\_id` | Filtrar por usuario asignado. |

| `skip` | Número de registros que se omiten; mínimo 0. |

| `limit` | Máximo de registros devueltos; entre 1 y 100. |

| `sort\_by` | Ordenar por `id`, `title` o `created\_at`. |

| `order` | Dirección `asc` o `desc`. |



Los filtros pueden combinarse y deben cumplirse simultáneamente.



Ejemplo:



```text

/tasks?project\_id=1\&completed=false\&category\_id=1\&skip=0\&limit=10\&sort\_by=id\&order=asc

```



Los listados devuelven esta estructura:



```json

{

&#x20; "items": \[],

&#x20; "total": 0,

&#x20; "skip": 0,

&#x20; "limit": 10

}

```



`total` indica cuántos registros cumplen los filtros antes de aplicar la paginación.



Los proyectos se pueden ordenar por `id`, `name` o `created\_at`. Las categorías, por `id` o `name`.



Cuando se ordena por un campo distinto del identificador, se utiliza también el identificador como desempate para mantener un orden estable.



\## Consultas y contadores



Los filtros, la ordenación y los límites se aplican en SQL.



El total de resultados se obtiene mediante COUNT, sin cargar todos los registros en memoria.



Los detalles de proyectos y categorías utilizan `selectinload` para cargar sus tareas asociadas de forma explícita.



Los resúmenes calculan los contadores mediante agregaciones SQL:



\- `total\_tasks`.

\- `completed\_tasks`.

\- `pending\_tasks`.



Una categoría o un proyecto sin tareas devuelve sus contadores a cero.



Las claves foráneas de las tareas tienen índices. No se han realizado pruebas de rendimiento con grandes volúmenes de datos.



\## Códigos de respuesta y errores



| Código | Significado |

| --- | --- |

| 200 | Consulta o modificación correcta. |

| 201 | Registro creado. |

| 204 | Registro eliminado; respuesta sin cuerpo. |

| 404 | Recurso solicitado o relacionado inexistente. |

| 409 | Conflicto, como nombre de categoría repetido o categoría con tareas. |

| 422 | Datos que no cumplen la validación del esquema. |



Ejemplo de bloqueo del borrado:



```json

{

&#x20; "detail": "No se puede eliminar una categoría con tareas. Reasigna o elimina sus tareas primero."

}

```



Los conflictos de integridad gestionados realizan rollback antes de responder.



\## Colección Postman



\[Descargar la colección](postman/TaskFlow-1.6-CRUD.postman\_collection.json)



Formato: Postman Collection v2.1.



La colección contiene las 15 operaciones CRUD obligatorias y peticiones adicionales para contadores, errores y cascada.



| Nº | Petición | Resultado esperado en la secuencia de prueba |

| --- | --- | --- |

| 01 | Crear proyecto | 201 |

| 02 | Crear categoría | 201 |

| 03 | Crear tarea | 201 |

| 04 | Listar tareas con filtros | 200 |

| 05 | Consultar tarea | 200 |

| 06 | Consultar proyecto con tareas | 200 |

| 07 | Consultar categoría con tareas | 200 |

| 08 | Listar proyectos | 200 |

| 09 | Listar categorías | 200 |

| 10 | Modificar tarea | 200 |

| 11 | Modificar proyecto | 200 |

| 12 | Modificar categoría | 200 |

| 13 | Resumen del proyecto | 200 |

| 14 | Resumen de la categoría | 200 |

| 15 | Bloquear borrado de categoría con tareas | 409 |

| 16 | Eliminar tarea | 204 |

| 17 | Consultar tarea eliminada | 404 |

| 18 | Eliminar categoría sin tareas | 204 |

| 19 | Crear tarea para probar cascada | 201 |

| 20 | Eliminar proyecto con cascada | 204 |

| 21 | Consultar proyecto eliminado | 404 |

| 22 | Comprobar tarea eliminada por cascada | 404 |



\### Cómo utilizar la colección



1\. Arrancar la API en el puerto 8004.

2\. Importar el archivo JSON en Postman.

3\. Ejecutar las peticiones en el orden indicado.

4\. Revisar los identificadores devueltos al crear registros.

5\. Adaptar los identificadores de las siguientes peticiones si son distintos.



La colección utiliza URLs locales e identificadores concretos de la sesión de pruebas. No contiene variables que propaguen automáticamente los identificadores.



Por tanto, no debe ejecutarse de forma desatendida sobre cualquier estado de la base de datos.



Las peticiones DELETE eliminan los datos de prueba. Repetir una petición DELETE sobre un registro ya eliminado devuelve 404.



En la prueba realizada, SQLite reutilizó el identificador 1 para la tarea creada después de borrar la anterior. Debe comprobarse siempre el identificador real de la respuesta.



\## Evidencias de las pruebas



Las capturas del documento de entrega muestran:



\- Creación de proyectos, categorías y tareas.

\- Listados con metadatos de paginación.

\- Consulta de una tarea.

\- Detalle de proyectos y categorías con tareas asociadas.

\- Modificación de los tres recursos.

\- Contadores de tareas completadas y pendientes.

\- Bloqueo del borrado de una categoría con tareas.

\- Borrado de una categoría sin tareas.

\- Respuesta 404 al consultar una tarea eliminada.

\- Borrado de un proyecto y desaparición de su tarea por cascada.



Las pruebas se ejecutaron manualmente en Postman. Exportar la colección conserva las definiciones de las peticiones, pero no equivale a generar un informe automático de pruebas ni garantiza que se incluyan las respuestas observadas.



\## Middleware y funcionalidades anteriores



Se conservan:



\- Cabeceras `X-Process-Time` y `X-Request-ID`.

\- Gestión global de excepciones.

\- Configuración de CORS.

\- Rutas de estado.

\- Usuarios de prueba y dependencias anidadas.



CORS permite los métodos GET, POST, PUT y DELETE.



La cabecera `X-User-ID` de la demostración anterior no constituye autenticación. Esta práctica no implementa control de acceso por usuario.



\## Control de versiones



Se incluyen el código, los requisitos, la documentación y la colección Postman.



El entorno virtual, las cachés de Python y la base de datos local se excluyen de Git mediante `.gitignore`.



La base de datos se genera al ejecutar la aplicación.



\## Entrega



\- Enlace a la carpeta de la práctica en GitHub.

\- Colección Postman exportada en formato JSON.

\- Documento de capturas y explicaciones como evidencia complementaria.

