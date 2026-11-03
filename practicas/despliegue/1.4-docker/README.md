\# Despliegue 1.4 — Docker y primer contenedor



\## Objetivo



Construir una imagen del backend de TaskFlow, ejecutar un contenedor

y comprobar la API mediante Swagger.



Esta carpeta contiene el código recuperado del commit `17c5cd6`.



\## Archivos principales



| Archivo | Función |

|---|---|

| app/main.py | Aplicación FastAPI y endpoints |

| app/\_\_init\_\_.py | Identifica el paquete Python |

| requirements.txt | Dependencias instaladas en la imagen |

| Dockerfile | Instrucciones para construir la imagen |

| .dockerignore | Archivos excluidos del contexto de construcción |

| docs/arquitectura.md | Procedimiento y comparación de arquitecturas |



\## Entorno de la práctica original



\- Ubuntu Server 22.04.5 LTS en VirtualBox.

\- Docker Engine 29.9.1.

\- Imagen: taskflow:1.4.

\- Contenedor: taskflow-api.

\- Puerto de Ubuntu: 8001.

\- Puerto interno del contenedor: 8000.



\## Requisitos



Docker Engine debe estar instalado y su servicio activo.



La instalación realizada en Ubuntu está explicada en

\[docs/arquitectura.md](docs/arquitectura.md).



Para construir esta imagen no es necesario activar el entorno virtual

de Ubuntu: Python y las dependencias se incorporan a la imagen.



\## Construcción en Ubuntu



Desde la raíz de una copia del repositorio que contenga esta carpeta:



```bash

cd practicas/despliegue/1.4-docker

sudo docker build -t taskflow:1.4 .

```



El punto final indica que esta carpeta es el contexto de construcción.



Comprobar la imagen:



```bash

sudo docker image ls taskflow

```



\## Arranque



Comprobar primero si ya existe un contenedor con el nombre utilizado:



```bash

sudo docker ps -a --filter name=taskflow-api

```



Si no existe, crearlo:



```bash

sudo docker run -d --name taskflow-api -p 8001:8000 taskflow:1.4

```



Si ya existe y está detenido, se puede arrancar con:



```bash

sudo docker start taskflow-api

```



Arrancar un contenedor existente reutiliza su imagen original.

Si se ha construido una imagen nueva, es necesario recrear el

contenedor para utilizarla.



\## Significado del comando de creación



| Elemento | Función |

|---|---|

| -d | Ejecutar en segundo plano |

| --name taskflow-api | Asignar un nombre al contenedor |

| -p 8001:8000 | Publicar el puerto interno 8000 en el 8001 del servidor |

| taskflow:1.4 | Seleccionar la imagen |



Dentro del contenedor, Gunicorn escucha en 0.0.0.0:8000.



La publicación utilizada permite conexiones a través de las interfaces

del servidor, siempre que la red lo permita.



EXPOSE 8000 en el Dockerfile documenta el puerto interno;

la publicación se realiza mediante la opción -p.



\## Estado y registros



```bash

sudo docker ps

sudo docker logs --tail 30 taskflow-api

```



El contenedor debe aparecer en estado Up.



Los registros deben mostrar que la aplicación ha terminado de arrancar,

por ejemplo mediante el mensaje Application startup complete.



\## Comprobación desde Ubuntu



```bash

curl -i http://127.0.0.1:8001/health

```



Resultado esperado: HTTP 200 con:



```json

{"status":"ok"}

```



También están disponibles /version y /ping.



\## Acceso a Swagger desde Windows



Consultar la IP actual en Ubuntu:



```bash

hostname -I

```



Abrir en el navegador de Windows:



```text

http://IP\_DE\_UBUNTU:8001/docs

```



Sustituir IP\_DE\_UBUNTU por la dirección real del servidor.



En Swagger, ejecutar GET /health mediante Try it out y Execute.

Debe aparecer HTTP 200 y el JSON esperado.



\## Ciclo de vida



Detener:



```bash

sudo docker stop taskflow-api

```



Arrancar el contenedor existente:



```bash

sudo docker start taskflow-api

```



Reiniciar:



```bash

sudo docker restart taskflow-api

```



Eliminar el contenedor detenido:



```bash

sudo docker stop taskflow-api

sudo docker rm taskflow-api

```



Recrearlo desde la imagen:



```bash

sudo docker run -d --name taskflow-api -p 8001:8000 taskflow:1.4

```



Eliminar el contenedor elimina su capa modificable.

La imagen y los archivos del proyecto fuera del contenedor se conservan.



Esta práctica no configura una base de datos ni volúmenes persistentes.



\## Arranque automático



Docker se configuró como servicio habilitado en Ubuntu.



El contenedor se creó sin una política --restart, por lo que no debe

suponerse que se iniciará automáticamente al encender el servidor.



\## Imagen, contenedor y máquina virtual



La imagen es la plantilla utilizada para crear contenedores.



El contenedor ejecuta los procesos de la aplicación compartiendo

el kernel Linux de Ubuntu.



La máquina virtual de VirtualBox ejecuta Ubuntu con su propio kernel.

Por tanto, en esta práctica Docker funciona dentro de una máquina virtual.



\## Alcance de esta versión



El backend contiene /health, /version y /ping.



No incorpora todavía los cambios posteriores de Pydantic y APIRouter.



La imagen base python:3.13-slim puede actualizarse con el tiempo.

Una nueva construcción no garantiza una imagen idéntica a la original.



\## Documentación y evidencias



\[Consultar el procedimiento y la comparación de arquitecturas](docs/arquitectura.md).



El documento conserva referencias a la ubicación original del proyecto.

Para construir esta copia, debe utilizarse como directorio de trabajo

practicas/despliegue/1.4-docker.



Las capturas de instalación, construcción, Swagger y ciclo de vida

se incluyeron en el documento de entrega de Classroom.



Esta copia recuperada desde Git todavía no se ha vuelto a construir

ni ejecutar después de reorganizar el repositorio.



\[Volver al índice principal](../../../README.md)

