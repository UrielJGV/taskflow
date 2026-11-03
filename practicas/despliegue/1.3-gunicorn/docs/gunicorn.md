# Práctica 1.3 — Instalación básica de Gunicorn

## 1. Objetivo de la práctica

El objetivo de esta práctica es instalar y ejecutar Gunicorn en Ubuntu
Server para servir el backend de TaskFlow, desarrollado con FastAPI
en la práctica 1.1.

Además de poner en funcionamiento el servidor, se comprueba que los
endpoints `/health`, `/version` y `/ping` responden correctamente y se
explica la función de los componentes utilizados.

Los requisitos principales son:

- Utilizar Python 3.13 o superior.
- Crear un entorno virtual para el proyecto.
- Instalar las dependencias desde `requirements.txt`.
- Ejecutar la aplicación con Gunicorn y un worker compatible con ASGI.
- Comprobar las respuestas de los tres endpoints.
- Documentar el procedimiento y aportar evidencias.

## 2. Punto de partida y entorno de trabajo

La aplicación inicial se desarrolló en Windows utilizando PowerShell.
El proyecto estaba guardado en la carpeta `taskflow` del escritorio.

Para esta práctica se ha trasladado el código a una máquina virtual
con Ubuntu Server ejecutada en VirtualBox.

El entorno utilizado es:

| Elemento | Valor |
|---|---|
| Sistema operativo del servidor | Ubuntu Server 22.04.5 LTS |
| Virtualización | VirtualBox |
| Equipo desde el que se administra | Windows |
| Usuario de Ubuntu | `urcerino` |
| Carpeta del proyecto en Ubuntu | `/home/urcerino/TaskFlow` |
| Python inicial de Ubuntu | 3.10.12 |
| Python instalado para el proyecto | 3.13.16 |
| Gunicorn observado en el arranque | 26.2.0 |
| Framework de la aplicación | FastAPI |
| Dirección de escucha | `127.0.0.1` |
| Puerto de la aplicación | `8000` |

La carpeta contiene el código de los tres endpoints desarrollados
en la práctica anterior. Por tanto, no ha sido necesario volver a
crear la aplicación desde cero.

## 3. Comprobaciones iniciales de Ubuntu Server

Antes de instalar paquetes se consultó la información del sistema:

```bash
cat /etc/os-release
```

Este comando muestra la distribución y su versión. Se comprobó que
la máquina virtual utiliza Ubuntu 22.04.5 LTS.

Después se consultó la versión de Python disponible:

```bash
python3 --version
```

El resultado inicial fue Python 3.10.12. Esta versión no cumplía el
requisito de Python 3.13 o superior, por lo que fue necesario instalar
otra versión para el proyecto.

También se comprobó la ubicación de trabajo y el contenido de las carpetas:

```bash
pwd
ls -l
ls -la ~/TaskFlow
```

La carpeta `TaskFlow` ya existía en Ubuntu y estaba vacía.

En Linux los nombres distinguen entre mayúsculas y minúsculas.
Por este motivo, `TaskFlow` y `taskflow` son rutas diferentes.

## 4. Conexión entre Windows y Ubuntu

### 4.1. Comprobación de la dirección IP

Para conocer las direcciones IP de Ubuntu se utilizó:

```bash
hostname -I
```

La opción lleva una `I` mayúscula.

Durante el trabajo se observaron distintas direcciones IP en diferentes
sesiones, entre ellas `192.168.1.107` y `172.20.10.11`.

Por este motivo, antes de conectarse desde Windows conviene comprobar
la IP actual de la máquina virtual.

### 4.2. Comprobación del servicio SSH

Se comprobó el estado del servicio mediante:

```bash
systemctl status ssh --no-pager
```

El servicio mostró el estado:

```text
active (running)
```

SSH permite abrir una terminal remota de Ubuntu desde Windows.
También permite transferir archivos mediante herramientas como SCP.

### 4.3. Acceso desde PowerShell

Desde PowerShell de Windows se utilizó una conexión de este tipo:

```powershell
ssh urcerino@IP_ACTUAL_DE_UBUNTU
```

`IP_ACTUAL_DE_UBUNTU` debe sustituirse por la dirección real obtenida
con `hostname -I`.

Tras introducir la contraseña, la terminal pasó a mostrar el usuario
y el nombre del equipo Ubuntu:

```text
urcerino@urcerino:~$
```

A partir de ese momento, los comandos escritos en esa sesión se ejecutan
en Ubuntu, aunque la ventana esté abierta en Windows.

Esta conexión facilita copiar y pegar comandos y reduce los errores
al escribirlos manualmente en la consola de VirtualBox.

## 5. Transferencia del proyecto

En PowerShell de Windows se accedió a la carpeta del proyecto:

```powershell
cd "$env:USERPROFILE\Desktop\taskflow"
```

Después se copiaron el código, las dependencias declaradas y el archivo
de exclusiones:

```powershell
scp -r app requirements.txt .gitignore urcerino@IP_ACTUAL_DE_UBUNTU:/home/urcerino/TaskFlow/
```

La opción `-r` permite copiar la carpeta `app` con su contenido.

Los elementos transferidos fueron:

- `app/main.py`: aplicación FastAPI y definición de los endpoints.
- `app/__init__.py`: archivo que identifica `app` como un paquete Python.
- `requirements.txt`: dependencias del proyecto.
- `.gitignore`: reglas para excluir archivos del control de versiones.

El entorno virtual creado en Windows no se reutilizó. Los entornos
virtuales contienen rutas y ejecutables asociados al sistema donde
se crean, por lo que se preparó uno nuevo en Ubuntu.

La transferencia se comprobó desde Ubuntu:

```bash
cd ~/TaskFlow
ls -la
ls -la app
```

## 6. Instalación de Python 3.13

### 6.1. Consulta de disponibilidad

Se actualizó la información de los paquetes:

```bash
sudo apt update
```

Este comando actualiza los índices de los repositorios. No equivale
a actualizar todos los paquetes instalados.

Después se comprobó si Python 3.13 estaba disponible:

```bash
apt-cache policy python3.13 python3.13-venv
```

Los repositorios configurados inicialmente no localizaron esos paquetes.

### 6.2. Incorporación del repositorio

Se instaló la herramienta necesaria para gestionar repositorios:

```bash
sudo apt install software-properties-common
```

A continuación se añadió Deadsnakes, un repositorio externo que proporciona
versiones adicionales de Python:

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
```

Tras confirmar la operación, se actualizaron los índices:

```bash
sudo apt update
```

### 6.3. Instalación y comprobación

Se instalaron el intérprete y el soporte para entornos virtuales:

```bash
sudo apt install python3.13 python3.13-venv
```

La instalación se comprobó con:

```bash
python3.13 --version
```

El resultado fue:

```text
Python 3.13.16
```

Esta versión cumple el requisito de la práctica.

Se instaló Python 3.13 para el proyecto sin sustituir manualmente
el intérprete que utiliza Ubuntu para sus herramientas del sistema.

## 7. Creación del entorno virtual

Desde la carpeta del proyecto se ejecutó:

```bash
cd ~/TaskFlow
python3.13 -m venv .venv
```

Este comando crea el entorno virtual en la carpeta `.venv` utilizando
Python 3.13.

El entorno virtual permite instalar las dependencias de TaskFlow
de forma aislada, evitando mezclarlas con las de otros proyectos
o con los paquetes Python del sistema.

Para activarlo se utilizó:

```bash
source .venv/bin/activate
```

Después de la activación apareció `(.venv)` al principio del indicador
de la terminal.

Se comprobó la versión y la ruta del intérprete:

```bash
python --version
which python
```

Los resultados fueron:

```text
Python 3.13.16
/home/urcerino/TaskFlow/.venv/bin/python
```

La ruta confirma que el comando `python` utiliza el intérprete del
entorno virtual del proyecto.

La activación afecta a la sesión de terminal actual. Si se abre una
nueva sesión para ejecutar el servidor, hay que activar de nuevo
el entorno.

## 8. Instalación de dependencias

Con el entorno virtual activado se ejecutó:

```bash
python -m pip install -r requirements.txt
```

La opción `-r` indica que las dependencias deben leerse del archivo
`requirements.txt`.

Utilizar `python -m pip` permite ejecutar el instalador asociado
al intérprete Python seleccionado en esa terminal.

El archivo del proyecto incluye las dependencias necesarias para
FastAPI y Uvicorn, además de Gunicorn condicionado a sistemas distintos
de Windows. En Ubuntu se instala Gunicorn.

Después se ejecutó:

```bash
python -m pip check
```

Esta comprobación revisa si las dependencias instaladas tienen requisitos
ausentes o incompatibles según sus metadatos.

Una instalación coherente muestra:

```text
No broken requirements found.
```

Esta comprobación no sustituye a las pruebas de funcionamiento de la API,
que se realizaron después con `curl`.

## 9. Aplicación utilizada

El archivo `app/main.py` contiene una aplicación FastAPI cuyo objeto
principal se llama `app`.

Los endpoints implementados son:

| Método | Ruta | Finalidad | Respuesta |
|---|---|---|---|
| GET | `/health` | Comprobar que la API responde | `{"status":"ok"}` |
| GET | `/version` | Consultar la versión de la aplicación | `{"version":"1.0.0"}` |
| GET | `/ping` | Realizar una comprobación sencilla de respuesta | `{"message":"pong"}` |

El endpoint `/health` es una comprobación básica de la aplicación.
En este proyecto no verifica servicios externos como una base de datos.

## 10. Arranque de Gunicorn

Con el entorno virtual activado y desde `~/TaskFlow` se ejecutó:

```bash
gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
```

El servidor mostró mensajes de inicio que incluían:

```text
Starting gunicorn 26.2.0
Listening at: http://127.0.0.1:8000
Using worker: uvicorn.workers.UvicornWorker
Application startup complete.
```

Estos mensajes indican que Gunicorn inició el worker, cargó la aplicación
y completó su arranque.

El proceso quedó ejecutándose en primer plano. Por ello, esa terminal
permaneció ocupada y las comprobaciones se realizaron desde otra terminal.

### 10.1. Significado del comando

| Elemento | Explicación |
|---|---|
| `gunicorn` | Inicia el servidor de aplicaciones |
| `app.main` | Identifica el módulo Python `app/main.py` |
| `:app` | Selecciona el objeto `app` definido dentro del módulo |
| `--worker-class` | Establece la clase de worker |
| `uvicorn.workers.UvicornWorker` | Utiliza Uvicorn para ejecutar la aplicación ASGI |
| `--bind` | Configura la dirección y el puerto de escucha |
| `127.0.0.1:8000` | Escucha en loopback IPv4 y en el puerto 8000 |

Ejecutar el comando desde la raíz del proyecto permite localizar
el paquete `app` mediante la ruta de importación indicada.

## 11. WSGI, ASGI y necesidad del worker adecuado

WSGI es una interfaz tradicional entre servidores y aplicaciones web
Python, basada en un modelo de comunicación síncrono.

ASGI es una interfaz que permite aplicaciones asíncronas y contempla
otros tipos de comunicación, como WebSocket.

FastAPI utiliza ASGI. Por tanto, necesita un servidor o worker que
comprenda esa interfaz.

El worker síncrono WSGI predeterminado de Gunicorn no ejecuta directamente
una aplicación FastAPI. En esta práctica se selecciona explícitamente
`UvicornWorker`, que proporciona la compatibilidad ASGI.

Por ello, UvicornWorker es necesario para la configuración concreta
solicitada en el enunciado. De forma general, el requisito es utilizar
un worker compatible con ASGI; UvicornWorker no es la única opción posible.

Aunque algunos endpoints se definan mediante funciones `def`, la aplicación
FastAPI sigue utilizando la interfaz ASGI.

## 12. ¿Por qué Gunicorn y no solamente Uvicorn?

Gunicorn utiliza un proceso principal que administra procesos worker.
Estos workers son los encargados de atender las peticiones.

La combinación utilizada reparte las responsabilidades:

- Gunicorn gestiona los procesos, sus señales y su ciclo de vida.
- El worker de Uvicorn ejecuta la aplicación ASGI.

Gunicorn permite configurar el número de workers y gestionar aspectos
como sus reinicios y tiempos de espera.

Uvicorn también puede ejecutar la aplicación por sí solo y dispone
de gestión de varios procesos. Por tanto, Gunicorn no es obligatorio
para todos los despliegues de FastAPI.

En esta práctica se utiliza para aprender un modelo de despliegue
con gestión de workers y cumplir la configuración indicada.

No se indicó `--workers` en el comando utilizado. La captura de arranque
muestra un worker iniciado; no se ha demostrado una configuración
con varios workers.

## 13. Servidor web y servidor de aplicaciones

Un servidor web como Apache o Nginx puede servir archivos estáticos,
gestionar conexiones HTTPS y actuar como proxy inverso.

Un proxy inverso recibe peticiones del cliente y las reenvía al backend.

En esta práctica, Gunicorn con el worker de Uvicorn carga y ejecuta
el código Python de TaskFlow para generar las respuestas de la API.

No se ha configurado Apache, Nginx ni un proxy inverso en este ejercicio.
Las comprobaciones se realizaron directamente contra Gunicorn
desde la propia máquina Ubuntu.

## 14. Dirección de escucha y accesibilidad

### 14.1. Dirección 127.0.0.1

`127.0.0.1` es una dirección de loopback IPv4. Identifica al propio
sistema desde el que se realiza la conexión.

Al escuchar en `127.0.0.1:8000`, el servidor queda accesible localmente
dentro de Ubuntu.

La dirección `127.0.0.1` de Windows corresponde a Windows, no a Ubuntu.
Por eso las pruebas con `curl` se ejecutaron dentro de la máquina virtual.

### 14.2. Dirección 0.0.0.0

Configurar un servidor con `0.0.0.0` hace que escuche en todas las
interfaces IPv4 locales.

Esto puede permitir conexiones desde otros equipos, siempre que
la configuración de red y el cortafuegos lo permitan.

`0.0.0.0` se utiliza como dirección de escucha; desde otro equipo
se accedería utilizando una IP real del servidor.

### 14.3. Nombre localhost

`localhost` es un nombre que normalmente resuelve a una dirección
de loopback, como `127.0.0.1` en IPv4 o `::1` en IPv6.

No es una dirección IP por sí mismo.

### 14.4. Motivo de utilizar loopback

El enunciado pide escuchar en `127.0.0.1`.

Esta configuración evita exponer directamente el puerto del backend
a otros equipos. En un despliegue posterior, un proxy inverso situado
en el mismo servidor podría recibir las peticiones externas y
reenviarlas al backend local.

## 15. Verificación de los endpoints

Con Gunicorn funcionando se abrió otra terminal dentro de Ubuntu.

No fue necesario activar el entorno virtual en esa terminal para
utilizar `curl`, porque es una herramienta del sistema.

Se ejecutaron los siguientes comandos:

```bash
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/version
curl -i http://127.0.0.1:8000/ping
```

La opción `-i` muestra las cabeceras HTTP junto con el cuerpo
de la respuesta.

Los resultados observados fueron:

| Endpoint | Estado HTTP | Tipo de contenido | Cuerpo |
|---|---|---|---|
| `/health` | `200 OK` | `application/json` | `{"status":"ok"}` |
| `/version` | `200 OK` | `application/json` | `{"version":"1.0.0"}` |
| `/ping` | `200 OK` | `application/json` | `{"message":"pong"}` |

El estado `200 OK` indica que la petición se atendió correctamente.

El tipo `application/json` identifica el formato del contenido devuelto.

Las respuestas coinciden con los valores definidos en `app/main.py`.
Esto demuestra que está respondiendo la aplicación TaskFlow y no
una página predeterminada del servidor.

La cabecera `server: uvicorn` es coherente con el worker utilizado:
Gunicorn administra el proceso y Uvicorn atiende la aplicación ASGI.

## 16. Parada y nuevo arranque

### 16.1. Detener el servidor

Para detener el servidor ejecutado en primer plano, se utiliza:

```text
Ctrl + C
```

Debe hacerse en la terminal donde está funcionando Gunicorn.

### 16.2. Volver a arrancarlo

En una sesión de Ubuntu:

```bash
cd ~/TaskFlow
source .venv/bin/activate
gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
```

Después se puede comprobar de nuevo:

```bash
curl -i http://127.0.0.1:8000/health
```

La comprobación se realiza desde otra terminal mientras el servidor
permanece activo.

### 16.3. Alcance de esta configuración

No se ha creado un servicio systemd para TaskFlow.

El arranque es manual y no se ha configurado el inicio automático
del backend al encender Ubuntu. Tampoco debe suponerse que seguirá
funcionando tras cerrar la sesión SSH donde se ejecuta.

La gestión como servicio puede realizarse en una práctica posterior.

## 17. Incidencias encontradas y solución

### 17.1. Ruta escrita con mayúsculas incorrectas

Se intentó acceder a una ruta con un nombre distinto en mayúsculas
y minúsculas.

La solución fue utilizar el nombre real:

```bash
cd ~/TaskFlow
```

### 17.2. Error al escribir un nombre de paquete

Se escribió `sofware-properties-common`, omitiendo una letra.

El nombre correcto es:

```text
software-properties-common
```

Tras corregirlo se pudo continuar.

### 17.3. Python 3.13 no disponible inicialmente

Los repositorios configurados no localizaron los paquetes requeridos.

La solución fue añadir el repositorio Deadsnakes, actualizar los
índices e instalar `python3.13` y `python3.13-venv`.

### 17.4. Conexión a una IP anterior

Una transferencia SCP falló al intentar conectar con una dirección
que no coincidía con la IP observada después en Ubuntu.

Se consultó de nuevo:

```bash
hostname -I
```

Después se utilizó la dirección actual para la conexión.

### 17.5. Entrada accidental en la consola de Python

Al ejecutar directamente la ruta del intérprete apareció:

```text
>>>
```

Este indicador corresponde a la consola interactiva de Python,
no a la terminal de comandos de Ubuntu.

Se salió mediante:

```python
exit()
```

### 17.6. Ejecución de nano en Windows

Se intentó abrir el archivo con `nano` desde una ventana local
de PowerShell, que no reconoció el comando.

La solución fue ejecutar Nano en una sesión de Ubuntu, mediante SSH
o desde la consola de VirtualBox.

El indicador `PS C:\...>` corresponde a PowerShell local.
El indicador `urcerino@...:...$` corresponde a la sesión de Ubuntu.

## 18. Comprobaciones útiles ante otros errores

Las siguientes acciones son instrucciones de diagnóstico; no significan
que todos estos errores hayan ocurrido durante la práctica.

| Problema | Comprobación |
|---|---|
| `gunicorn: command not found` | Activar `.venv` y comprobar la instalación de dependencias |
| Error al importar `app.main` | Ejecutar desde `~/TaskFlow` y comprobar `app/main.py` |
| Puerto ocupado | Revisar si ya existe otro servidor escuchando en 8000 |
| `Connection refused` | Comprobar que Gunicorn sigue activo y que la dirección es correcta |
| Respuesta `404 Not Found` | Revisar que la ruta solicitada coincide con el endpoint |
| Fallo de conexión SSH | Comprobar IP actual, red y estado del servicio SSH |

Para consultar si hay un proceso escuchando en el puerto 8000:

```bash
ss -ltnp 'sport = :8000'
```

Para comprobar dependencias:

```bash
cd ~/TaskFlow
source .venv/bin/activate
python -m pip check
```

## 19. Evidencias y documentación entregada

Las capturas del proceso se incluyen en el documento de la práctica
entregado junto con el proyecto.

Las evidencias principales muestran:

- La comprobación inicial de Ubuntu y Python.
- La preparación y transferencia del proyecto.
- La instalación de Python 3.13.16.
- La creación y activación del entorno virtual.
- El arranque correcto de Gunicorn.
- Las respuestas HTTP 200 y los JSON de los tres endpoints.

Este archivo recoge los comandos, las explicaciones técnicas y las
incidencias del proceso. El documento adjunto aporta las capturas.

## 20. Resultado de la práctica

Se ha ejecutado el backend de TaskFlow en Ubuntu Server con
Python 3.13.16 y un entorno virtual propio.

Gunicorn ha arrancado correctamente utilizando UvicornWorker y
escuchando en `127.0.0.1:8000`.

Las pruebas realizadas muestran que `/health`, `/version` y `/ping`
devuelven estado HTTP 200 y el JSON esperado.

Quedan fuera del alcance realizado el proxy inverso, HTTPS, el arranque
automático mediante systemd y las pruebas de carga.

## 21. Referencias y nota de compatibilidad

- Documentación de despliegue de Uvicorn:
  https://www.uvicorn.org/deployment/
- Diseño y gestión de workers de Gunicorn:
  https://gunicorn.org/design/

La documentación de Uvicorn marca el módulo `uvicorn.workers`
como obsoleto y recomienda el paquete independiente `uvicorn-worker`
para futuras configuraciones.

En esta práctica se ha mantenido el comando solicitado por el enunciado,
cuyo funcionamiento se ha comprobado con las versiones instaladas.
