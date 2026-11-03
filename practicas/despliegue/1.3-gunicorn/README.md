\# Despliegue 1.3 — Instalación básica de Gunicorn



\## Objetivo



Ejecutar el backend de TaskFlow con Gunicorn en Ubuntu Server

y comprobar sus tres endpoints.



Esta carpeta contiene el código recuperado del commit `e7ada53`.



\## Archivos principales



| Archivo | Función |

|---|---|

| app/main.py | Aplicación FastAPI y endpoints |

| app/\_\_init\_\_.py | Identifica el paquete Python |

| requirements.txt | Dependencias de esta versión |

| docs/gunicorn.md | Procedimiento original y explicaciones técnicas |

| .gitignore | Exclusiones del control de versiones |



\## Entorno utilizado en la práctica original



\- Ubuntu Server 22.04.5 LTS en VirtualBox.

\- Python 3.13.16.

\- Gunicorn 26.2.0.

\- Administración desde Windows mediante SSH.



El servidor Gunicorn se ejecuta en Ubuntu.

Windows se utiliza para administrar y editar los archivos.



\## Requisitos



\- Python 3.13 o superior.

\- Soporte para crear entornos virtuales.

\- Acceso a Internet para instalar las dependencias.



La instalación de Python utilizada originalmente está explicada

en \[docs/gunicorn.md](docs/gunicorn.md).



\## Preparación en Ubuntu



Los siguientes comandos se ejecutan en Ubuntu, desde la raíz

de una copia del repositorio que contenga esta carpeta:



```bash

cd practicas/despliegue/1.3-gunicorn

python3.13 -m venv .venv

source .venv/bin/activate

python -m pip install -r requirements.txt

python -m pip check

```



El entorno virtual se crea en Ubuntu. No se debe reutilizar

un entorno virtual procedente de Windows.



\## Arranque



Desde la carpeta de esta práctica y con el entorno activado:



```bash

gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000

```



| Elemento | Significado |

|---|---|

| app.main:app | Objeto app del archivo app/main.py |

| --worker-class | Selección del tipo de worker |

| UvicornWorker | Ejecuta la aplicación ASGI |

| --bind | Configura la dirección y el puerto |

| 127.0.0.1:8000 | Acceso local en Ubuntu, puerto 8000 |



Gunicorn queda ejecutándose en primer plano. Las comprobaciones

se realizan desde otra terminal de Ubuntu.



\## Verificación



```bash

curl -i http://127.0.0.1:8000/health

curl -i http://127.0.0.1:8000/version

curl -i http://127.0.0.1:8000/ping

```



| Endpoint | Código esperado | Respuesta esperada |

|---|---|---|

| /health | 200 | {"status":"ok"} |

| /version | 200 | {"version":"1.0.0"} |

| /ping | 200 | {"message":"pong"} |



127.0.0.1 identifica el equipo desde el que se realiza la petición.

Por ello, las comprobaciones anteriores deben ejecutarse dentro

de Ubuntu, incluida una sesión SSH conectada a ese servidor.



\## Gunicorn y Uvicorn



Gunicorn administra los procesos worker.

UvicornWorker ejecuta la aplicación FastAPI mediante la interfaz ASGI.



El worker WSGI síncrono predeterminado no es adecuado para ejecutar

directamente esta aplicación ASGI.



Uvicorn también puede funcionar por sí solo. En este ejercicio se

utiliza la combinación solicitada por el enunciado.



\## Parada y nuevo arranque



Para detener Gunicorn, pulsar Ctrl+C en su terminal.



Para volver a arrancarlo en otra sesión, entrar en la carpeta,

activar el entorno y repetir el comando de Gunicorn.



No se ha configurado un servicio systemd para TaskFlow ni su inicio

automático al encender Ubuntu.



Si el puerto 8000 está ocupado, detener la otra instancia o utilizar

otro puerto y adaptar las URLs de comprobación.



\## Compatibilidad



Se conserva el comando utilizado en la entrega original.



El módulo uvicorn.workers está marcado como obsoleto en la

documentación de Uvicorn. Para futuras configuraciones se recomienda

revisar el paquete independiente uvicorn-worker.



\## Documentación y evidencias



\[Consultar el procedimiento original](docs/gunicorn.md).



Ese documento menciona /home/urcerino/TaskFlow, la ubicación original.

En esta copia organizada, los comandos deben ejecutarse desde

practicas/despliegue/1.3-gunicorn.



Las capturas de la instalación, el arranque y las respuestas HTTP

se incluyeron en el documento entregado en Classroom.



Esta copia histórica todavía no se ha vuelto a ejecutar después

de reorganizar las carpetas.



\[Volver al índice principal](../../../README.md)

