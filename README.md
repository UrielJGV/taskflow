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
| [1.6 — CRUD completo](practicas/desarrollo/1.6-crud/) | CRUD de tareas, proyectos y categorías; filtros, paginación, contadores y colección Postman. | Evolución de la práctica 1.5 |
| [1.7 — Autenticación JWT](practicas/desarrollo/1.7-jwt/) | Registro, login, contraseñas con bcrypt y protección de escritura mediante tokens con expiración. | Evolución de la práctica 1.6 |

### Despliegue de aplicaciones web

| Práctica | Contenido | Origen |
| --- | --- | --- |
| [1.1 — Preparar el servidor base](practicas/despliegue/1.1-servidor-base/) | Ubuntu Server, máquina virtual y acceso SSH. | Repositorio original de Despliegue |
| [1.2 — Instalación básica de Apache](practicas/despliegue/1.2-apache/) | Servidor web Apache y comprobación del puerto 80. | Repositorio original de Despliegue |
| [1.3 — Instalación de Gunicorn](practicas/despliegue/1.3-gunicorn/) | Ejecución del backend en Ubuntu Server. | Commit `e7ada53` |
| [1.4 — Docker y primer contenedor](practicas/despliegue/1.4-docker/) | Imagen Docker, contenedor y comparación de arquitecturas. | Commit `17c5cd6` |
| [2.1 — Módulos de Apache](practicas/despliegue/2.1-modulos-apache/) | Activación de módulos, verificación del servicio y documentación con ejemplos. | Configuración en Ubuntu Server |
| [2.2 — Host virtual taskflow.local](practicas/despliegue/2.2-host-virtual/) | Página estática, hosts virtuales independientes y registros separados. | Configuración en Ubuntu Server |
| [2.3 — Autenticación básica de admin](practicas/despliegue/2.3-autenticacion-basica/) | Protección de /admin con contraseña, permisos y pruebas HTTP 401/200. | Configuración en Ubuntu Server |

La numeración se repite porque las prácticas pertenecen a módulos distintos.

## Cómo consultar el repositorio

1. Seleccionar el módulo y la práctica en las tablas anteriores.
2. Leer su README y la documentación asociada.
3. Consultar el código de esa entrega, cuando corresponda.
4. Instalar las dependencias indicadas en su README. La práctica 1.7 utiliza `requirements-auth.txt`, que incluye las dependencias base.
5. Ejecutar los comandos desde la carpeta y el entorno indicados en esa práctica.

Las prácticas de desarrollo contienen copias independientes de su código. No necesitan importar archivos de otras carpetas de prácticas.

Los entornos virtuales no se incluyen en Git: deben crearse en el equipo donde se vaya a ejecutar cada ejercicio.

Las prácticas de despliegue contienen documentación, configuraciones y evidencias del servidor.

## Práctica más reciente de desarrollo: autenticación JWT

La [práctica 1.7 de desarrollo](practicas/desarrollo/1.7-jwt/) incorpora:

- Registro mediante `POST /auth/register`.
- Inicio de sesión mediante `POST /auth/login`.
- Contraseñas almacenadas como hashes bcrypt con sal aleatoria y coste 12.
- Tokens JWT firmados con HS256 y una duración de 30 minutos.
- Clave de firma configurada mediante la variable de entorno `JWT_SECRET_KEY`.
- Validación de firma, expiración e identidad del usuario.
- Consulta del usuario autenticado mediante `GET /users/me`.
- Protección de todos los POST, PUT y DELETE de tareas y proyectos.
- Respuestas `401` con la cabecera `WWW-Authenticate: Bearer`.
- Evidencias de rechazo sin token y con un token de prueba caducado.

Se conservan las funcionalidades del CRUD de la práctica 1.6.

En esta versión, la autenticación utiliza la cabecera `Authorization: Bearer TOKEN` y sustituye la demostración basada en `X-User-ID`.

### Ejecución en Windows

Desde la raíz del repositorio:

```powershell
cd .\practicas\desarrollo\1.7-jwt
```

Crear el entorno virtual si todavía no existe:

```powershell
py -m venv .venv
```

Instalar todas las dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-auth.txt
```

Generar una clave aleatoria para esta sesión de PowerShell:

```powershell
$env:JWT_SECRET_KEY = & .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

Arrancar la API desde esa misma ventana:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8005
```

Abrir la documentación interactiva:

http://127.0.0.1:8005/docs

La clave queda disponible en esa sesión de PowerShell. Si se cierra la ventana, debe volver a configurarse antes de arrancar la API.

Generar una clave diferente invalida los tokens firmados con la anterior. Para mantenerlos entre reinicios debe conservarse la misma clave mediante una configuración segura.

El código lee la clave desde el entorno; no carga automáticamente un archivo `.env`.

Por defecto, la base de datos `taskflow.db` se crea dentro de la carpeta de la práctica y está excluida de Git. Si se utiliza la variable `DATABASE_URL`, debe comprobarse que apunta a la base de datos deseada.

### Flujo de prueba

1. Registrar un usuario mediante `POST /auth/register`, enviando JSON.
2. Pulsar Authorize en Swagger e introducir el usuario y la contraseña.
3. Swagger obtiene el token mediante `/auth/login`, que recibe un formulario.
4. Ejecutar `GET /users/me` para consultar la identidad autenticada.
5. Crear un proyecto mediante `POST /projects` y comprobar la respuesta `201`.
6. Cerrar la autorización y repetir la petición para comprobar el rechazo `401`.

Las contraseñas y los tokens reales no deben aparecer en capturas ni archivos del repositorio.

### Alcance de la autenticación

Las consultas GET de tareas y proyectos permanecen públicas. Las rutas de categorías conservan el comportamiento de la práctica anterior.

No se implementan roles, permisos por propietario, refresh tokens ni una lista de revocación de tokens. Cualquier usuario autenticado puede realizar las operaciones protegidas de tareas y proyectos.

Los JWT están firmados, no cifrados. En un despliegue real debe utilizarse HTTPS.

La prueba de expiración utiliza un token firmado con la misma clave y con una fecha de expiración ya pasada. No representa una espera real de 30 minutos. Los tokens emitidos por el login mantienen su duración normal de 30 minutos.

Las instrucciones completas, decisiones de seguridad y limitaciones están en el [README de la práctica 1.7](practicas/desarrollo/1.7-jwt/README.md).

## Versión anterior de desarrollo: CRUD completo

La [práctica 1.6 de desarrollo](practicas/desarrollo/1.6-crud/) incorpora:

- Creación, listado, consulta, modificación y eliminación de tareas, proyectos y categorías.
- Persistencia en SQLite mediante SQLAlchemy.
- Filtros combinables de tareas por proyecto, estado, categoría y usuario asignado.
- Paginación mediante `skip` y `limit`, con metadatos en la respuesta.
- Ordenación ascendente y descendente.
- Detalle de proyectos y categorías con sus tareas asociadas.
- Endpoints de resumen con contadores de tareas.
- Eliminación de proyectos con borrado en cascada de sus tareas.
- Bloqueo del borrado de categorías que todavía tienen tareas.
- Validación de datos y gestión de errores.
- Colección Postman con 22 peticiones.

En la práctica 1.6 se conservan los middleware y la demostración de dependencias anidadas. Su cabecera `X-User-ID` no constituye un sistema de autenticación.

### Ejecución de la práctica 1.6 en Windows

Desde la raíz del repositorio:

```powershell
cd .\practicas\desarrollo\1.6-crud
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
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8004
```

Abrir la documentación interactiva:

http://127.0.0.1:8004/docs

El archivo `taskflow.db` y las tablas se crean al arrancar. La base de datos local está excluida de Git.

### Colección Postman de la práctica 1.6

[Descargar la colección de la práctica 1.6](practicas/desarrollo/1.6-crud/postman/TaskFlow-1.6-CRUD.postman_collection.json)

La colección incluye las 15 operaciones CRUD obligatorias y peticiones adicionales para contadores, errores y cascada.

Las peticiones utilizan URLs locales e identificadores concretos de la sesión de pruebas. Si se crean registros con otros identificadores, deben adaptarse las peticiones siguientes.

La colección corresponde a la versión 1.6. Para utilizar sus operaciones protegidas contra la versión 1.7 habría que adaptar la URL y añadir un token válido.

Las instrucciones y los resultados esperados están en el [README de la práctica 1.6](practicas/desarrollo/1.6-crud/README.md).

## Publicación del sitio: host virtual taskflow.local

La [práctica 2.2 de despliegue](practicas/despliegue/2.2-host-virtual/) incluye:

- Una página estática sencilla de TaskFlow.
- Un host virtual con `ServerName taskflow.local`.
- Publicación desde `/var/www/taskflow`.
- Un sitio `localhost` independiente, con contenido diferente.
- Desactivación del sitio inicial `000-default.conf`.
- Registros de acceso y errores propios para cada sitio.
- Resolución local del nombre mediante el archivo `hosts`.
- Evidencias de sintaxis, hosts activos y peticiones HTTP con respuesta `200`.
- Explicación del funcionamiento de los hosts virtuales y un ejemplo de ampliación.

La página utiliza datos de demostración. No está conectada a la API ni guarda cambios en una base de datos.

La dirección `http://taskflow.local` funciona en los equipos que tengan configurada la resolución del nombre y acceso al servidor; no es una dirección pública.

## Práctica más reciente de despliegue: autenticación básica de admin

La [práctica 2.3 de despliegue](practicas/despliegue/2.3-autenticacion-basica/) continúa la configuración de la práctica 2.2 e incorpora:

- Una página de administración en `/var/www/taskflow/admin`.
- Protección del directorio mediante autenticación HTTP básica.
- Un usuario `admin` creado con `htpasswd`.
- Almacenamiento de la contraseña mediante un hash bcrypt.
- Archivo de contraseñas situado fuera del directorio publicado.
- Permisos de lectura para Apache y modificación para root.
- Acceso restringido mediante `Require user admin`.
- Pruebas con respuesta `401` sin credenciales y `200` con credenciales correctas.
- Documentación sobre contraseñas, gestión de usuarios y alternativas de autenticación.

La configuración y las evidencias se conservan en la carpeta de la práctica.

El archivo `.htpasswd` y la contraseña no se incluyen en el repositorio.

La protección corresponde a una página estática servida por Apache. No implementa autenticación en la API FastAPI.

Esta práctica utiliza HTTP en un entorno de laboratorio. La autenticación básica codifica las credenciales en Base64, pero no las cifra. En un entorno real debe utilizarse HTTPS.

## Documentación disponible

- [Servidor base](practicas/despliegue/1.1-servidor-base/README.md)
- [Instalación de Apache](practicas/despliegue/1.2-apache/docs/apache.md)
- [Organización con APIRouter](practicas/desarrollo/1.3-apirouter/docs/routers.md)
- [Middleware](practicas/desarrollo/1.4-middleware/README.md)
- [SQLAlchemy y conexión a base de datos](practicas/desarrollo/1.5-sqlalchemy/README.md)
- [CRUD completo y pruebas con Postman](practicas/desarrollo/1.6-crud/README.md)
- [Autenticación JWT](practicas/desarrollo/1.7-jwt/README.md)
- [Instalación de Gunicorn](practicas/despliegue/1.3-gunicorn/docs/gunicorn.md)
- [Docker y comparación de arquitecturas](practicas/despliegue/1.4-docker/docs/arquitectura.md)
- [Módulos de Apache](practicas/despliegue/2.1-modulos-apache/README.md)
- [Explicación y ejemplos de módulos](practicas/despliegue/2.1-modulos-apache/docs/modulos-apache.md)
- [Host virtual taskflow.local](practicas/despliegue/2.2-host-virtual/README.md)
- [Funcionamiento de los hosts virtuales](practicas/despliegue/2.2-host-virtual/docs/hosts-virtuales.md)
- [Autenticación básica de admin](practicas/despliegue/2.3-autenticacion-basica/README.md)

Algunos documentos describen el proceso original y pueden mencionar las ubicaciones de trabajo utilizadas durante las prácticas.

Para ejecutar las copias organizadas, hay que situarse en la carpeta concreta del ejercicio.

## Evidencias

Las capturas de las pruebas se recogen en los documentos de entrega correspondientes.

Las evidencias incorporadas al repositorio están disponibles aquí:

- [Evidencias del servidor base](practicas/despliegue/1.1-servidor-base/evidencias-servidor-base.pdf)
- [Evidencias de Apache](practicas/despliegue/1.2-apache/docs/evidencias-apache.pdf)
- [Evidencias de módulos de Apache](practicas/despliegue/2.1-modulos-apache/evidencias/)
- [Evidencias del host virtual taskflow.local](practicas/despliegue/2.2-host-virtual/evidencias/)
- [Evidencias de autenticación básica](practicas/despliegue/2.3-autenticacion-basica/evidencias/)
- [Evidencias de autenticación JWT](practicas/desarrollo/1.7-jwt/evidencias/)

Las configuraciones de Apache se conservan en:

- [Configuración de los hosts virtuales de la práctica 2.2](practicas/despliegue/2.2-host-virtual/config/)
- [Configuración con autenticación de la práctica 2.3](practicas/despliegue/2.3-autenticacion-basica/config/)

Las capturas de otras prácticas pueden estar en los documentos entregados por Classroom. Recuperar una versión del código desde Git no incorpora automáticamente esas capturas.

La colección Postman contiene las definiciones de las peticiones. Las capturas documentan las respuestas observadas durante las pruebas manuales.

## Estado del proyecto original

La carpeta `app/` situada en la raíz conserva la versión de trabajo utilizada antes de organizar las prácticas.

También se mantienen los archivos de despliegue y la documentación originales.

Las entregas separadas y sus instrucciones se consultan desde `practicas/`.

Para ejecutar la versión más reciente de la API, con autenticación JWT, debe utilizarse la carpeta `practicas/desarrollo/1.7-jwt/`.

La versión anterior del CRUD se conserva en `practicas/desarrollo/1.6-crud/`.

La página estática de la práctica 2.2 se encuentra en `practicas/despliegue/2.2-host-virtual/frontend/`.

La página de administración de la práctica 2.3 se encuentra en `practicas/despliegue/2.3-autenticacion-basica/admin/`.

## Evolución y alcance

Las primeras versiones utilizan operaciones simuladas de creación de tareas y proyectos.

La práctica 1.5 añade persistencia real en SQLite, modelos relacionados y sesiones por petición.

La práctica 1.6 amplía esa base con CRUD completo, categorías, filtros, paginación, contadores y reglas de borrado comprobadas mediante peticiones HTTP.

La práctica 1.7 añade registro, inicio de sesión, hashes de contraseñas y protección de las operaciones de escritura de tareas y proyectos mediante JWT con expiración.

En despliegue, la práctica 2.1 configura módulos de Apache, la práctica 2.2 publica una página estática mediante hosts virtuales con contenido y registros separados, y la práctica 2.3 protege una zona de administración mediante autenticación básica.

Cada cambio pertenece a la carpeta de su práctica y conserva las versiones anteriores. Las configuraciones de despliegue guardadas representan el estado de cada entrega; el servidor puede continuar evolucionando en las prácticas siguientes.

La reorganización conserva el código de cada entrega; no implica que todas las versiones históricas hayan vuelto a ejecutarse después de exportarlas.

Las decisiones de diseño y las limitaciones de cada práctica están documentadas en su propio README.