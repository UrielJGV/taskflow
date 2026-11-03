\# Desarrollo 1.2 — Modelado con Pydantic



\## Objetivo



Definir los contratos de entrada y salida de TaskFlow con Pydantic,

validar los datos recibidos y devolver una tarea simulada.



Esta carpeta contiene el código recuperado del commit `5484701`.



\## Archivos principales



| Archivo | Función |

|---|---|

| app/main.py | Aplicación y endpoints |

| app/schemas.py | Schemas y restricciones de validación |

| app/\_\_init\_\_.py | Identifica el paquete Python |

| requirements.txt | Dependencias de esta versión |

| .gitignore | Exclusiones del control de versiones |



\## Modelos definidos



| Schema | Campos |

|---|---|

| TaskCreate | title, description opcional, project\_id |

| TaskRead | Campos de TaskCreate, id, completed y created\_at |

| ProjectCreate | name y description |

| ProjectRead | Campos de ProjectCreate, id y created\_at |



Los modelos Create representan los datos enviados por el cliente.

Los modelos Read incorporan los datos que devuelve la API.



Los schemas son contratos de la API. No crean tablas ni guardan

información en una base de datos.



\## Validaciones



\- El título debe tener entre 1 y 100 caracteres.

\- La descripción de una tarea es opcional y admite hasta 1000 caracteres.

\- Los identificadores deben ser enteros positivos.

\- El nombre del proyecto debe tener entre 1 y 100 caracteres.

\- La descripción del proyecto es obligatoria y admite entre 1 y 1000 caracteres.

\- Se eliminan espacios al principio y al final de los textos.

\- Se rechazan campos adicionales no definidos en el schema.



El límite del título procede del enunciado.

Los límites adicionales son decisiones de esta implementación.



\## Ejecución en Windows



Requiere Python 3.13 o superior instalado.



Desde la raíz del repositorio:



```powershell

cd .\\practicas\\desarrollo\\1.2-pydantic

py -3 -m venv .venv

.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt

.\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --reload

```



`py -3` utiliza el Python 3 seleccionado por el lanzador de Windows.

Se puede comprobar su versión antes de crear el entorno:



```powershell

py -3 --version

```



\## Ejecución en Ubuntu



Con Python 3.13 y su soporte para entornos virtuales instalados,

desde la raíz del repositorio:



```bash

cd practicas/desarrollo/1.2-pydantic

python3.13 -m venv .venv

.venv/bin/python -m pip install -r requirements.txt

.venv/bin/python -m uvicorn app.main:app --reload

```



\## Acceso a Swagger



Abrir desde el mismo equipo donde se ejecuta la aplicación:



http://127.0.0.1:8000/docs



Desplegar POST /tasks, pulsar Try it out, introducir el JSON y

pulsar Execute.



\## Caso válido



Petición:



```json

{

&#x20; "title": "Preparar la práctica de Pydantic",

&#x20; "description": "Crear los schemas y comprobar la validación.",

&#x20; "project\_id": 1

}

```



Resultado esperado: HTTP 201 Created.



La respuesta contiene los datos enviados y añade:



\- id: 1.

\- completed: false.

\- created\_at: fecha y hora de la petición en UTC.



La fecha cambia en cada petición.



\## Caso inválido: título vacío



Petición:



```json

{

&#x20; "title": "",

&#x20; "description": "Prueba de validación con título vacío.",

&#x20; "project\_id": 1

}

```



Resultado esperado: HTTP 422.



El detalle identifica:



\- loc: \["body", "title"].

\- type: "string\_too\_short".

\- La restricción de longitud mínima de un carácter.



La validación de entrada rechaza la petición antes de ejecutar

la función de creación.



\## Endpoints conservados



| Método | Ruta | Resultado esperado |

|---|---|---|

| GET | /health | HTTP 200 |

| GET | /version | HTTP 200 |

| GET | /ping | HTTP 200 |

| POST | /tasks | HTTP 201 con datos válidos; 422 con datos inválidos |



Los schemas de proyectos están definidos, pero esta versión

todavía no publica un endpoint de creación de proyectos.



\## Evidencias



Durante la práctica original se comprobaron en Swagger:



\- Una petición válida con respuesta HTTP 201.

\- Una petición con título vacío y respuesta HTTP 422.



Las capturas se incluyeron en el documento entregado en Classroom.

Esta copia recuperada desde Git todavía no se ha vuelto a ejecutar

tras la reorganización de carpetas.



\## Limitaciones



El endpoint devuelve una tarea simulada con id fijo igual a 1.

No guarda tareas ni verifica que el proyecto indicado exista.



\## Parada



Pulsar Ctrl+C en la terminal del servidor.



Si el puerto 8000 está ocupado por otra práctica, detener esa instancia

o añadir `--port 8002` al comando de Uvicorn y utilizar ese puerto

en el navegador.



\[Volver al índice principal](../../../README.md)

