\# Desarrollo 1.1 — Primeros endpoints



\## Objetivo



Crear la aplicación inicial de TaskFlow con FastAPI, tres endpoints

de comprobación y documentación automática en Swagger.



Esta carpeta contiene el código recuperado del commit `418d284`.



\## Archivos principales



| Archivo | Función |

|---|---|

| app/main.py | Aplicación FastAPI y endpoints |

| app/\_\_init\_\_.py | Identifica el paquete Python |

| requirements.txt | Dependencias de esta versión |

| .gitignore | Exclusiones para el control de versiones |



\## Requisitos



\- Python 3.13 o superior como entorno recomendado para estas prácticas.

\- Acceso a Internet para instalar las dependencias.



\## Ejecución en Windows



Desde la raíz del repositorio, entrar en esta práctica:



```powershell

cd .\\practicas\\desarrollo\\1.1-primeros-endpoints

```



Crear un entorno virtual propio:



```powershell

py -3 -m venv .venv

```



Instalar las dependencias:



```powershell

.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt

```



Arrancar la aplicación:



```powershell

.\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --reload

```



Los comandos utilizan directamente el Python del entorno virtual,

por lo que no es necesario activar un script de PowerShell.



\## Ejecución en Ubuntu



Desde la raíz del repositorio:



```bash

cd practicas/desarrollo/1.1-primeros-endpoints

python3.13 -m venv .venv

.venv/bin/python -m pip install -r requirements.txt

.venv/bin/python -m uvicorn app.main:app --reload

```



Python 3.13 y el soporte para crear entornos virtuales deben

estar instalados previamente.



\## Comprobación



Abrir en el navegador del mismo equipo donde se ejecuta Uvicorn:



http://127.0.0.1:8000/docs



| Método | Ruta | Respuesta esperada |

|---|---|---|

| GET | /health | `{"status":"ok"}` |

| GET | /version | `{"version":"1.0.0"}` |

| GET | /ping | `{"message":"pong"}` |



Las tres peticiones deben devolver HTTP 200.



\## Parada



Pulsar Ctrl+C en la terminal donde está funcionando Uvicorn.



Si otra práctica utiliza el puerto 8000, detenerla antes de arrancar

esta o seleccionar otro puerto mediante `--port 8002`.



\## Alcance



Esta versión corresponde a los primeros endpoints.

Todavía no incluye los schemas de tareas y proyectos ni los routers

añadidos en las prácticas posteriores.



La exportación desde Git conserva la versión original.

Las respuestas anteriores son los resultados esperados al comprobarla.



\[Volver al índice principal](../../../README.md)

