\# Práctica 1.3 — Organización con APIRouter



\## 1. Objetivo



Organizar los endpoints de TaskFlow por recurso mediante APIRouter,

separando la configuración de la aplicación de las funciones que

atienden las peticiones.



Esta práctica continúa el trabajo de modelado con Pydantic.



\## 2. Estructura del proyecto



| Archivo | Responsabilidad |

|---|---|

| app/main.py | Crear y configurar FastAPI y registrar los routers |

| app/schemas.py | Definir los contratos de entrada y salida |

| app/routers/\_\_init\_\_.py | Identificar routers como paquete Python |

| app/routers/tasks.py | Definir las operaciones de tareas |

| app/routers/projects.py | Definir las operaciones de proyectos |

| app/routers/status.py | Definir las comprobaciones de estado |



\## 3. Router de tareas



En app/routers/tasks.py se define:



```python

router = APIRouter(prefix="/tasks", tags=\["tasks"])

```



El prefijo establece la parte común de las URLs del recurso.

La etiqueta agrupa sus operaciones en Swagger.



El endpoint existente POST /tasks se trasladó desde main.py.

Se conserva TaskCreate como entrada, TaskRead como salida y

el código HTTP 201.



El decorador utiliza una ruta vacía:



```python

@router.post("", response\_model=TaskRead, status\_code=201)

```



Al combinarla con el prefijo, la URL resultante es /tasks.

Así se evita repetir el prefijo y generar una ruta como /tasks/tasks.



La creación sigue siendo simulada: no guarda tareas ni comprueba

la existencia del proyecto indicado.



\## 4. Router de proyectos



En app/routers/projects.py se define:



```python

router = APIRouter(prefix="/projects", tags=\["projects"])

```



Se añadió POST /projects como operación temporal para mostrar

y comprobar este recurso.



Recibe ProjectCreate y devuelve ProjectRead con un identificador

simulado y una fecha de creación en UTC. Responde con HTTP 201.



No se ha añadido persistencia en una base de datos.



\## 5. Router de estado



En app/routers/status.py se agrupan:



\- GET /health.

\- GET /version.

\- GET /ping.



Este router utiliza la etiqueta status y no añade prefijo,

por lo que conserva las URLs de las prácticas anteriores.



También contiene HealthResponse, el schema de respuesta de /health.

Los schemas de tareas y proyectos continúan en app/schemas.py.



\## 6. Registro de routers



main.py importa los módulos:



```python

from app.routers import projects, status, tasks

```



Después de crear la aplicación, registra sus routers:



```python

app.include\_router(tasks.router)

app.include\_router(projects.router)

app.include\_router(status.router)

```



Crear un archivo con un router no basta para publicar sus endpoints:

es necesario incluirlo en la aplicación.



main.py ya no contiene funciones de endpoints.

Su responsabilidad es configurar FastAPI y registrar los routers.



\## 7. Documentación Swagger



Se configuró openapi\_tags para describir los grupos:



\- tasks: operaciones de tareas.

\- projects: operaciones de proyectos.

\- status: salud, versión y conectividad.



Swagger se consulta en:



http://127.0.0.1:8000/docs



La captura general muestra los endpoints agrupados por estas etiquetas.



\## 8. Arranque en Windows



Desde la raíz del proyecto se ejecutó:



```powershell

.\\venv\\Scripts\\python.exe -m uvicorn app.main:app --reload

```



La opción --reload permite recargar la aplicación al guardar cambios

durante el desarrollo.



El punto de entrada sigue siendo app.main:app, por lo que la

reorganización conserva la ubicación del objeto principal de FastAPI.



\## 9. Comprobaciones realizadas



| Operación | Resultado comprobado |

|---|---|

| Swagger | Grupos tasks, projects y status |

| POST /projects con datos válidos | HTTP 201 |

| POST /tasks con datos válidos | HTTP 201 |

| GET /health | HTTP 200 y {"status":"ok"} |



Ejemplo utilizado para crear un proyecto:



```json

{

&#x20; "name": "Proyecto TaskFlow",

&#x20; "description": "Organización de la API mediante routers."

}

```



Ejemplo utilizado para crear una tarea:



```json

{

&#x20; "title": "Comprobar los routers",

&#x20; "description": "Verificar que la creación simulada sigue funcionando.",

&#x20; "project\_id": 1

}

```



Los identificadores devueltos son simulados. Enviar project\_id igual

a 1 no establece todavía una relación almacenada en una base de datos.



Las capturas de las pruebas se incluyen en el documento de entrega.



\## 10. Beneficios de la modularidad



Cuando todas las rutas están en main.py, el archivo crece y mezcla

la configuración con operaciones de distintos recursos.



Separarlas facilita:



\- Localizar las operaciones de cada recurso.

\- Revisar cambios más pequeños.

\- Repartir el trabajo entre varias personas.

\- Añadir endpoints sin ampliar continuamente main.py.

\- Aplicar prefijos, etiquetas y futuras dependencias por router.



La separación también introduce un coste: hay más archivos,

importaciones y registros que mantener. Para una aplicación muy

pequeña, un único archivo puede resultar más sencillo.



En TaskFlow, tareas y proyectos son recursos diferentes, por lo que

la separación ayuda a mantener el proyecto conforme crece.



\## 11. Monolito y diseño modular



Una aplicación modular puede seguir siendo un monolito.



En este proyecto los routers pertenecen a la misma aplicación FastAPI,

comparten el proceso de ejecución y se despliegan juntos.



No se han creado microservicios. La mejora consiste en organizar

internamente el código por responsabilidades.



\## 12. Decisiones de diseño



Se mantienen /tasks y /projects como nombres de recursos en plural.



No se añade todavía el prefijo /api/v1, para conservar las rutas

utilizadas en la práctica anterior y seguir los prefijos del enunciado.



Se mantiene schemas.py como archivo porque el número de modelos

todavía es pequeño.



No se crean carpetas models/ ni core/ vacías: actualmente no hay

modelos de persistencia ni configuración compartida que lo requieran.



La estructura podrá ampliarse cuando se incorporen esas funciones.



\## 13. Entrega



La entrega incluye:



\- app/main.py actualizado.

\- El paquete app/routers/ y sus archivos.

\- Los schemas existentes necesarios para ejecutar la aplicación.

\- Este documento de explicación.

\- Captura de Swagger agrupado por tags.

\- Acceso al repositorio GitHub.



Repositorio:



https://github.com/UrielJGV/taskflow

