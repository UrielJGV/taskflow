# Práctica 1.4 — Docker y primer contenedor

## 1. Objetivo

Desplegar el backend de TaskFlow en un contenedor Docker y comparar
esta solución con la instalación directa realizada en la práctica 1.3.

También se analiza la diferencia entre contenedores y máquinas
virtuales, y qué aportaría desplegar la aplicación en la nube.

## 2. Entorno utilizado

- Equipo Windows desde el que se administra el servidor mediante SSH.
- Ubuntu Server 22.04.5 LTS ejecutado en VirtualBox.
- Proyecto situado en `/home/urcerino/TaskFlow`.
- Docker Engine 29.9.1.
- Imagen creada: `taskflow:1.4`.
- Contenedor: `taskflow-api`.
- Puerto publicado en Ubuntu: 8001.
- Puerto de la aplicación dentro del contenedor: 8000.

Se reutiliza el código FastAPI desarrollado en la práctica 1.1.
El proyecto contiene los endpoints `/health`, `/version` y `/ping`,
además de la documentación automática disponible en `/docs`.

## 3. Comprobación inicial

Se comprobó el contenido del proyecto y la disponibilidad de Docker:

```bash
cd ~/TaskFlow
ls -la
docker --version
systemctl status docker --no-pager
```

Inicialmente, Ubuntu no encontraba el comando `docker` y el servicio
`docker.service` no existía.

## 4. Instalación de Docker Engine

Se utilizó el repositorio oficial de Docker para Ubuntu.

Primero se actualizaron los índices de paquetes y se instalaron
las herramientas necesarias:

```bash
sudo apt update
sudo apt install ca-certificates curl -y
```

Después se preparó el directorio de claves y se descargó la clave
de firma del repositorio:

```bash
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

La clave permite a APT verificar las firmas del repositorio.

Se añadió el repositorio correspondiente a Ubuntu 22.04, cuyo nombre
de versión es `jammy`:

```bash
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: jammy
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```

Se actualizaron los índices y se instalaron los paquetes:

```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

Estos paquetes proporcionan el motor, el cliente de Docker, el entorno
de ejecución y herramientas para construir imágenes y utilizar Compose.
En esta práctica se utiliza `docker run`, no Docker Compose.

## 5. Servicio y permisos

Se inició Docker y se habilitó su arranque con Ubuntu:

```bash
sudo systemctl enable --now docker
```

Se comprobó la instalación:

```bash
docker --version
systemctl is-active docker
systemctl is-enabled docker
```

Los resultados observados fueron:

- Docker 29.9.1.
- Servicio `active`.
- Arranque automático `enabled`.

Para administrar Docker se utiliza `sudo`. No se añadió el usuario
al grupo `docker`.

El acceso al motor Docker concede capacidades administrativas
importantes sobre el servidor, por lo que no debe otorgarse
indiscriminadamente.

Habilitar el servicio Docker no significa que todos los contenedores
se inicien automáticamente: su arranque depende también de la política
de reinicio configurada para cada uno.

## 6. Primer contenedor de prueba

Se ejecutó:

```bash
sudo docker run hello-world
```

Esta prueba descarga una imagen pequeña, crea un contenedor,
muestra un mensaje y termina.

Después se consultaron todos los contenedores:

```bash
sudo docker ps -a
```

En este caso, un estado `Exited (0)` es normal: indica que el programa
de prueba terminó correctamente.

Esta prueba permite comprobar el funcionamiento básico del motor,
la descarga de imágenes y la ejecución de contenedores.

## 7. Imagen y contenedor

Una imagen es una plantilla que contiene el sistema de archivos
y la configuración necesarios para ejecutar una aplicación.

Un contenedor es una instancia creada a partir de una imagen.
Tiene sus propios procesos y una capa de archivos modificable.

La misma imagen puede utilizarse para crear varios contenedores.

Detener un contenedor no lo elimina. Eliminarlo tampoco elimina
automáticamente la imagen de la que procede.

## 8. Dockerfile de TaskFlow

En la raíz del proyecto se creó el archivo `Dockerfile`:

```dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### Explicación

- `FROM` utiliza una imagen base con Python 3.13.
- `PYTHONDONTWRITEBYTECODE` evita generar archivos `.pyc`.
- `PYTHONUNBUFFERED` evita el almacenamiento en búfer de la salida
  de Python, facilitando la consulta de registros.
- `WORKDIR` establece `/app` como directorio de trabajo.
- El primer `COPY` incorpora el archivo de dependencias.
- `RUN` instala esas dependencias durante la construcción.
- El segundo `COPY` incorpora el código del backend.
- `useradd` crea un usuario para ejecutar la aplicación.
- `USER` hace que el proceso de la aplicación se ejecute sin ser root
  dentro del contenedor.
- `EXPOSE` documenta el puerto interno. No publica el puerto por sí solo.
- `CMD` establece el comando de arranque de Gunicorn.

Se copian primero las dependencias y después el código para facilitar
que Docker reutilice la capa de instalación cuando solo cambia
el código de la aplicación.

La imagen contiene su propio Python y sus dependencias. No utiliza
el entorno `.venv` creado en Ubuntu durante la práctica 1.3.

La etiqueta `python:3.13-slim` puede actualizarse con el tiempo.
Para una reproducción estricta de la imagen base se podría fijar
su digest, además de las versiones de las dependencias.

## 9. Archivo .dockerignore

Se creó `.dockerignore` con este contenido:

```text
.venv/
venv/
__pycache__/
*.py[cod]
.git/
.env
.env.*
docs/
*.pdf
```

Este archivo excluye elementos del contexto enviado al constructor.

Así se evita enviar el entorno virtual local, el historial Git,
documentación y posibles archivos de variables de entorno con secretos.

No elimina esos archivos del proyecto original.

## 10. Construcción de la imagen

Desde la raíz del proyecto se ejecutó:

```bash
cd ~/TaskFlow
sudo docker build -t taskflow:1.4 .
```

- `build` construye la imagen siguiendo el Dockerfile.
- `-t taskflow:1.4` asigna el nombre y la etiqueta.
- `.` indica que la carpeta actual es el contexto de construcción.

Después se consultó la imagen:

```bash
sudo docker image ls taskflow
```

La etiqueta `1.4` identifica esta práctica; no representa la versión
de Python ni de Docker.

## 11. Creación y arranque del contenedor

Se utilizó:

```bash
sudo docker run -d --name taskflow-api -p 8001:8000 taskflow:1.4
```

| Opción | Función |
|---|---|
| `-d` | Ejecutar en segundo plano |
| `--name taskflow-api` | Asignar un nombre al contenedor |
| `-p 8001:8000` | Publicar el puerto interno 8000 en el puerto 8001 de Ubuntu |
| `taskflow:1.4` | Seleccionar la imagen |

Se eligió el puerto 8001 del servidor para evitar conflictos
con el puerto 8000 utilizado en la práctica anterior.

Dentro del contenedor, Gunicorn escucha en `0.0.0.0:8000`.
Esto permite recibir las conexiones reenviadas por Docker.

La publicación `8001:8000` no se limita a loopback. En las pruebas
permitió acceder desde Windows utilizando la IP de Ubuntu.

No se configuró una política de reinicio automático con `--restart`.

## 12. Comprobación del funcionamiento

Se consultaron el estado y los registros:

```bash
sudo docker ps
sudo docker logs --tail 30 taskflow-api
```

El contenedor apareció en estado `Up` y mostró la publicación
del puerto 8001 hacia el puerto 8000.

Los registros mostraron Gunicorn 26.2.0, el worker de Uvicorn
y el mensaje:

```text
Application startup complete.
```

Desde Ubuntu se comprobó:

```bash
curl -i http://127.0.0.1:8001/health
```

La respuesta fue HTTP `200 OK` con:

```json
{"status":"ok"}
```

### Acceso a Swagger desde Windows

Durante las pruebas se accedió en el navegador a:

```text
http://192.168.1.107:8001/docs
```

La IP corresponde a la máquina Ubuntu durante esa sesión.
Si cambia, debe consultarse de nuevo mediante `hostname -I`.

Swagger mostró TaskFlow API y los endpoints `/health`, `/version`
y `/ping`.

Desde `/health` se pulsó `Try it out` y después `Execute`.
La respuesta mostró:

- Código HTTP 200.
- Cuerpo `{"status":"ok"}`.
- Tipo de contenido `application/json`.

Esto demuestra una petición real al backend publicado en el puerto 8001.

## 13. Ciclo de vida del contenedor

### Parar

```bash
sudo docker stop taskflow-api
sudo docker ps -a --filter name=taskflow-api
```

El contenedor queda detenido, pero sigue existiendo.

### Volver a arrancar

```bash
sudo docker start taskflow-api
```

Tras esperar a que la aplicación termine de arrancar:

```bash
curl -i http://127.0.0.1:8001/health
```

`start` reutiliza el contenedor existente.

### Reiniciar

```bash
sudo docker restart taskflow-api
```

Después se vuelve a comprobar `/health`.

`restart` detiene y arranca el mismo contenedor.

### Eliminar

```bash
sudo docker stop taskflow-api
sudo docker rm taskflow-api
```

Se comprueba la desaparición del contenedor y la conservación
de la imagen:

```bash
sudo docker ps -a --filter name=taskflow-api
sudo docker image ls taskflow
```

Eliminar un contenedor elimina su capa de archivos modificable.
Los datos que deban conservarse deben guardarse mediante mecanismos
de persistencia, como volúmenes.

Este backend inicial no utiliza una base de datos ni se han configurado
volúmenes en esta práctica.

### Recrear

```bash
sudo docker run -d --name taskflow-api -p 8001:8000 taskflow:1.4
```

Se crea una nueva instancia desde la imagen existente.

```bash
sudo docker ps --filter name=taskflow-api
curl -i http://127.0.0.1:8001/health
```

Recrear el contenedor no requiere reconstruir la imagen si el código
y la configuración de construcción no han cambiado.

## 14. Contenedores y máquinas virtuales

| Aspecto | Máquina virtual | Contenedor |
|---|---|---|
| Unidad de ejecución | Sistema operativo invitado | Procesos aislados |
| Kernel | Utiliza el kernel del sistema invitado | Comparte el kernel del host Linux |
| Contenido habitual | Sistema operativo completo y aplicaciones | Aplicación y dependencias necesarias |
| Arranque habitual | Más lento | Más rápido |
| Consumo habitual | Mayor por sistema invitado | Menor por instancia de aplicación |
| Aislamiento | Límite de virtualización de hardware | Aislamiento de procesos y recursos |
| Uso típico | Ejecutar sistemas operativos completos | Empaquetar y desplegar servicios |

Los contenedores no son máquinas virtuales pequeñas.
La diferencia fundamental es que comparten el kernel del host.

El aislamiento de un contenedor no elimina todos los riesgos:
siguen siendo necesarios permisos adecuados, actualizaciones
y una configuración cuidadosa.

En esta práctica se utilizan ambas tecnologías:

1. Windows ejecuta VirtualBox.
2. VirtualBox ejecuta Ubuntu Server como máquina virtual.
3. Docker Engine funciona dentro de Ubuntu.
4. TaskFlow se ejecuta dentro de un contenedor.

El contenedor comparte el kernel de Ubuntu, no el de Windows.

## 15. Instalación directa frente a contenedor

| Criterio | Instalación directa de la práctica 1.3 | Contenedor de la práctica 1.4 |
|---|---|---|
| Python | Instalado en Ubuntu | Incluido en la imagen |
| Dependencias | Instaladas en `.venv` | Instaladas durante la construcción |
| Código | Ejecutado desde `~/TaskFlow` | Copiado dentro de la imagen |
| Aislamiento | Principalmente de paquetes Python | Procesos, red y sistema de archivos |
| Arranque | Comando Gunicorn en la terminal | `docker run` o `docker start` |
| Traslado | Requiere preparar el entorno de destino | Puede trasladarse la imagen a un entorno compatible |
| Actualización | Modificar código o dependencias y reiniciar | Construir una imagen nueva y reemplazar el contenedor |
| Diagnóstico | Registros del proceso y herramientas del sistema | `docker logs`, `docker ps` y herramientas de inspección |
| Complejidad inicial | Menor para un servicio sencillo | Requiere aprender imágenes, redes y contenedores |
| Persistencia | Archivos guardados directamente en el servidor | Debe planificarse fuera de la capa desechable del contenedor |

### Ventajas de la instalación directa

- Permite aprender el funcionamiento de Python y Gunicorn en el servidor.
- Resulta sencilla para una aplicación pequeña y un entorno controlado.
- No requiere administrar un motor de contenedores.

### Inconvenientes de la instalación directa

- Hay que preparar Python y las dependencias en cada servidor.
- Pueden existir diferencias entre entornos.
- El entorno virtual no aísla procesos, red ni todo el sistema operativo.

### Ventajas del contenedor

- Agrupa la aplicación y sus dependencias en una imagen.
- Facilita desplegar el mismo artefacto en varios entornos compatibles.
- Permite crear y reemplazar instancias de forma repetible.
- Documenta la construcción mediante el Dockerfile.

### Inconvenientes del contenedor

- Añade conceptos y herramientas que hay que administrar.
- Requiere gestionar imágenes, redes, registros y almacenamiento.
- Los datos persistentes necesitan una estrategia específica.
- Las imágenes deben reconstruirse y actualizarse para incorporar
  correcciones de seguridad.

Docker mejora la consistencia del despliegue, pero no garantiza por sí
solo seguridad, alta disponibilidad ni escalado automático.

## 16. Criterios para elegir una opción

La instalación directa puede ser adecuada para aprender, para un servicio
sencillo en un único servidor o cuando el equipo ya administra ese
entorno de forma reproducible.

Los contenedores resultan útiles cuando se necesita:

- Mantener entornos de desarrollo y despliegue similares.
- Ejecutar varios servicios con dependencias diferentes.
- Automatizar la construcción y publicación de versiones.
- Reemplazar instancias con rapidez.
- Desplegar imágenes en plataformas compatibles.

Para TaskFlow, Docker permite empaquetar el backend y preparar su
evolución hacia un despliegue con varios servicios.

## 17. Docker para el backend y para un servidor web

En esta práctica se contiene el backend porque es el componente
desarrollado: una aplicación Python con sus dependencias y su
servidor de aplicaciones.

Docker también puede ejecutar servidores web como Nginx o Apache.
No existe una limitación que lo reserve al backend.

Si más adelante se añade un proxy inverso, podría instalarse
directamente en Ubuntu o ejecutarse en otro contenedor.

Mantener componentes separados puede facilitar su configuración,
actualización y escalado independiente.

Aquí no se ha configurado un servidor web adicional, HTTPS ni
un proxy inverso.

## 18. Qué aporta desplegar en la nube

La nube permite ejecutar TaskFlow en infraestructura remota,
sin depender del ordenador local y de su máquina virtual.

Según el servicio elegido, puede aportar:

- Acceso remoto a la aplicación.
- Capacidad de ampliar o reducir recursos.
- Servicios gestionados de bases de datos, registros y monitorización.
- Registros privados de imágenes.
- Automatización de despliegues.
- Opciones de balanceo y redundancia.

Estos beneficios dependen del diseño y del servicio contratado.
Subir una imagen a la nube no crea automáticamente una arquitectura
segura, escalable o de alta disponibilidad.

También hay que considerar:

- Costes de cómputo, almacenamiento y tráfico.
- Configuración de red, permisos y secretos.
- Copias de seguridad.
- Actualizaciones.
- Protección de datos.
- Dependencia del proveedor.

### Opciones para TaskFlow

Una opción sería utilizar una máquina virtual en la nube e instalar
Docker. Se conservaría gran parte del procedimiento de esta práctica,
pero seguiría siendo necesario administrar el sistema operativo.

Otra opción sería una plataforma gestionada de contenedores.
El proveedor asumiría parte de la gestión, aunque habría que adaptar
puertos, configuración, comprobaciones de salud y persistencia.

La nube describe dónde y cómo se proporcionan los recursos.
Docker describe cómo se empaqueta y ejecuta la aplicación.
Son conceptos relacionados, pero diferentes.

En esta práctica no se ha realizado ningún despliegue en la nube.

## 19. Comparación del recorrido de una petición

En la instalación directa, una petición realizada dentro de Ubuntu
a `127.0.0.1:8000` llega al proceso Gunicorn instalado en el entorno
virtual y después a la aplicación FastAPI.

En el despliegue con Docker, una petición desde Windows a
`IP_DE_UBUNTU:8001` llega al puerto publicado por Docker, se reenvía
al puerto 8000 del contenedor y es atendida por Gunicorn,
UvicornWorker y FastAPI.

Esta comparación explica por qué el puerto externo y el interno
pueden ser diferentes.

## 20. Errores comunes y diagnóstico

| Problema | Comprobación |
|---|---|
| Permiso denegado al usar Docker | Utilizar `sudo`, según la configuración de esta práctica |
| No se puede conectar con el motor | Consultar `systemctl status docker --no-pager` |
| Nombre de contenedor ocupado | Revisar `sudo docker ps -a` antes de crear otro con el mismo nombre |
| Puerto 8001 ocupado | Comprobar qué proceso o contenedor lo utiliza |
| Contenedor detenido inesperadamente | Consultar `sudo docker logs taskflow-api` |
| Código modificado sin efecto | Reconstruir la imagen y recrear el contenedor |
| Navegador sin conexión | Comprobar IP, publicación del puerto, red y estado del contenedor |

Comandos útiles:

```bash
sudo docker ps -a
sudo docker logs --tail 50 taskflow-api
sudo docker image ls
sudo ss -ltnp 'sport = :8001'
hostname -I
```

Estos son procedimientos de diagnóstico, no una lista de errores
que necesariamente hayan ocurrido.

## 21. Evidencias

Las capturas se incluyen en el documento de pruebas entregado
junto con el proyecto.

Las evidencias recogen:

- Estado inicial antes de instalar Docker.
- Versión instalada y servicio activo y habilitado.
- Ejecución del contenedor de prueba.
- Dockerfile y archivo `.dockerignore`.
- Construcción de la imagen.
- Comando de creación del contenedor.
- Estado y registros de TaskFlow.
- Acceso a Swagger.
- Respuesta HTTP 200 del endpoint `/health`.
- Parada, arranque y reinicio.
- Eliminación y recreación del contenedor.

## 22. Archivos que forman parte de la entrega

- `Dockerfile`.
- `.dockerignore`.
- Código de la aplicación en `app/`.
- Dependencias en `requirements.txt`.
- Este documento: `docs/arquitectura.md`.
- Documento de pruebas con las capturas, el comando de arranque
  y el acceso a Swagger.

No es necesario incluir `.venv` ni `venv` en la entrega del proyecto.

## 23. Resultado

TaskFlow se ha preparado para ejecutarse desde la imagen `taskflow:1.4`.

Se ha comprobado el funcionamiento del contenedor, su publicación
en el puerto 8001 y el acceso a la documentación Swagger.

La petición a `/health` ha devuelto HTTP 200 y el JSON esperado.

Además, se han practicado las operaciones principales del ciclo
de vida del contenedor y se ha comparado este despliegue con
la instalación directa.

## 24. Fuente de instalación

Documentación oficial de Docker Engine para Ubuntu:

https://docs.docker.com/engine/install/ubuntu/
