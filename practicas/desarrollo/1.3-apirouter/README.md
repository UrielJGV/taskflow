\# Desarrollo 1.3 — Organización con APIRouter



\## Objetivo



Separar los endpoints de TaskFlow por recurso y mantener main.py

centrado en configurar la aplicación y registrar los routers.



Esta carpeta contiene el código recuperado del commit `ebbc322`.



\## Estructura



| Archivo | Responsabilidad |

|---|---|

| app/main.py | Configuración de FastAPI y registro de routers |

| app/schemas.py | Contratos de entrada y salida de tareas y proyectos |

| app/routers/tasks.py | Operaciones de tareas |

| app/routers/projects.py | Operaciones de proyectos |

| app/routers/status.py | Salud, versión y conectividad |

| app/routers/\_\_init\_\_.py | Identifica el paquete de routers |

| requirements.txt | Dependencias de esta versión |

| docs/routers.md | Explicación detallada de la práctica |



\## Organización de las rutas



| Grupo de Swagger | Método | Ruta |

|---|---|---|

| tasks | POST | /tasks |

| projects | POST | /projects |

| status | GET | /health |

| status | GET | /version |

| status | GET | /ping |



Los routers de tareas y proyectos utilizan estos prefijos y etiquetas:



```python

APIRouter(prefix="/tasks", tags=\["tasks"])

APIRouter(prefix="/projects", tags=\["projects"])

```



El router de estado utiliza la etiqueta status sin añadir un prefijo,

para conservar las direcciones de las comprobaciones anteriores.



\## Registro en la aplicación



main.py registra los tres routers:



```python

app.include\_router(tasks.router)

app.include\_router(projects.router)

app.include\_router(status.router)

```



No contiene funciones de endpoints. También configura las descripciones

de los grupos que aparecen en Swagger.



\## Ejecución en Windows



Utilizar Python 3.13 o superior. Comprobar la versión seleccionada:



```powershell

py -3 --version

```



Desde la raíz del repositorio:



```powershell

cd .\\practicas\\desarrollo\\1.3-apirouter

py -3 -m venv .venv

.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt

.\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --reload

```



\## Ejecución en Ubuntu



Con Python 3.13 y el soporte para entornos virtuales instalados,

desde la raíz del repositorio:



```bash

cd practicas/desarrollo/1.3-apirouter

python3.13 -m venv .venv

.venv/bin/python -m pip install -r requirements.txt

.venv/bin/python -m uvicorn app.main:app --reload

```



\## Acceso a Swagger



Abrir desde el equipo donde se ejecuta Uvicorn:



http://127.0.0.1:8000/docs



Deben aparecer los grupos tasks, projects y status con sus descripciones.



\## Prueba de creación de una tarea



En POST /tasks, pulsar Try it out e introducir:



```json

{

&#x20; "title": "Comprobar los routers",

&#x20; "description": "Verificar la creación simulada de tareas.",

&#x20; "project\_id": 1

}

```



Pulsar Execute.



Resultado esperado: HTTP 201 con los datos enviados y los campos

id, completed y created\_at.



\## Prueba de creación de un proyecto



En POST /projects, introducir:



```json

{

&#x20; "name": "Proyecto TaskFlow",

&#x20; "description": "Organización de la API mediante routers."

}

```



Resultado esperado: HTTP 201 con name, description, id y created\_at.



\## Prueba de estado



Ejecutar GET /health desde Swagger.



Resultado esperado: HTTP 200 con:



```json

{"status":"ok"}

```



\## Validación conservada



POST /tasks sigue utilizando TaskCreate como entrada y TaskRead

como salida.



Un título vacío debe devolver HTTP 422. Separar los endpoints

en routers no elimina las restricciones de los schemas.



\## Ventajas de esta estructura



\- Facilita localizar las operaciones de cada recurso.

\- Reduce el contenido y las responsabilidades de main.py.

\- Permite añadir endpoints dentro de su módulo correspondiente.

\- Agrupa la documentación mediante etiquetas.

\- Facilita repartir el trabajo y revisar cambios.



La separación introduce más archivos e importaciones, pero resulta

útil conforme crece el proyecto.



La aplicación sigue siendo un monolito modular: todos los routers

forman parte de la misma aplicación y se despliegan juntos.

No son microservicios independientes.



\## Decisiones y alcance



Se mantienen las rutas /tasks y /projects sin un prefijo /api/v1.



Los schemas continúan en un único archivo porque su cantidad

todavía es pequeña.



La creación de tareas y proyectos es simulada. Los identificadores

son fijos y no existe persistencia ni comprobación de relaciones

en una base de datos.



\## Documentación y evidencias



\[Consultar la explicación detallada](docs/routers.md).



La captura de Swagger agrupado y las pruebas se incluyeron en

el documento de entrega de la práctica.



Esta carpeta se ha recuperado del historial de Git. No se ha vuelto

a ejecutar esta copia después de reorganizar el repositorio.



\## Parada



Pulsar Ctrl+C en la terminal donde se ejecuta Uvicorn.



Si otra práctica ocupa el puerto 8000, detenerla o arrancar esta

con `--port 8002` y utilizar ese puerto en el navegador.



\[Volver al índice principal](../../../README.md)

