\# TaskFlow — Prácticas de desarrollo y despliegue

| [1.4 — Middleware](practicas/desarrollo/1.4-middleware/) | CORS, tiempo de procesamiento, trazabilidad y manejo global de errores | Implementación propia sobre la práctica 1.3 |

Proyecto educativo de una API de tareas y proyectos con FastAPI.



Cada práctica tiene su propia carpeta con el código correspondiente

a su entrega. Las versiones se han recuperado del historial de Git

para conservar la evolución del proyecto.



\## Índice de prácticas



\### Desarrollo de aplicaciones web usando frameworks



| Práctica | Contenido | Código de origen |

|---|---|---|

| \[1.1 — Primeros endpoints](practicas/desarrollo/1.1-primeros-endpoints/) | Aplicación inicial, health, version y ping | `418d284` |

| \[1.2 — Modelado con Pydantic](practicas/desarrollo/1.2-pydantic/) | Schemas, validación y creación simulada de tareas | `5484701` |

| \[1.3 — Organización con APIRouter](practicas/desarrollo/1.3-apirouter/) | Rutas separadas por recurso y Swagger agrupado | `ebbc322` |



\### Despliegue de aplicaciones web



| Práctica | Contenido | Código de origen |

|---|---|---|

| \[1.3 — Instalación de Gunicorn](practicas/despliegue/1.3-gunicorn/) | Ejecución del backend en Ubuntu Server | `e7ada53` |

| \[1.4 — Docker y primer contenedor](practicas/despliegue/1.4-docker/) | Imagen Docker, contenedor y comparación de arquitecturas | `17c5cd6` |



La numeración se repite porque las prácticas pertenecen a módulos distintos.



\## Cómo consultar el repositorio



1\. Seleccionar el módulo y la práctica en las tablas anteriores.

2\. Consultar su código dentro de `app/`.

3\. Instalar las dependencias de su propio `requirements.txt`.

4\. Ejecutar los comandos desde la raíz de esa práctica.



Cada carpeta contiene una copia de los archivos de su versión.

No depende del código situado en otra carpeta de prácticas.



Los entornos virtuales no se incluyen en Git: deben crearse

en el equipo donde se vaya a ejecutar cada ejercicio.



\## Documentación disponible



\- \[Organización con APIRouter](practicas/desarrollo/1.3-apirouter/docs/routers.md)

\- \[Instalación de Gunicorn](practicas/despliegue/1.3-gunicorn/docs/gunicorn.md)

\- \[Docker y comparación de arquitecturas](practicas/despliegue/1.4-docker/docs/arquitectura.md)



Estos documentos describen el proceso original y pueden mencionar

la ubicación de trabajo utilizada durante las prácticas.

Para ejecutar las copias organizadas, hay que situarse en la

carpeta concreta del ejercicio.



Las capturas entregadas en Classroom se encuentran en los documentos

de entrega correspondientes. No se incluyen automáticamente en este

repositorio al recuperar el código desde Git.



\## Estado del proyecto original



La carpeta `app/` de la raíz conserva la versión de trabajo utilizada

antes de organizar las prácticas.



También se mantienen los archivos de despliegue y la documentación

originales. Las entregas separadas se consultan desde `practicas/`.



\## Alcance



Las operaciones de creación de tareas y proyectos son simuladas.

Todavía no existe persistencia en una base de datos.



La reorganización en carpetas conserva el código de las entregas;

no supone que todas las copias se hayan vuelto a ejecutar después

de exportarlas.

| [1.1 — Preparar el servidor base](practicas/despliegue/1.1-servidor-base/) | Ubuntu Server, máquina virtual y acceso SSH | Repositorio original de Despliegue |
| [1.2 — Instalación básica de Apache](practicas/despliegue/1.2-apache/) | Servidor web Apache y comprobación del puerto 80 | Repositorio original de Despliegue |