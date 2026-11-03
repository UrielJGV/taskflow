\# Desarrollo 1.4 — Middleware



\## Objetivo



Añadir comportamiento común a las peticiones de TaskFlow:



\- Control de acceso entre orígenes mediante CORS.

\- Medición del tiempo de procesamiento.

\- Identificación de peticiones.

\- Manejo global de excepciones no controladas.



Se reutiliza la aplicación organizada con APIRouter de la práctica 1.3.



\## Estructura



| Archivo | Responsabilidad |

|---|---|

| app/main.py | Configuración de FastAPI, CORS, handlers y routers |

| app/middleware.py | Tiempo de procesamiento, identificador y registro de peticiones |

| app/errors.py | Respuesta genérica y registro interno de excepciones |

| app/routers/debug.py | Ruta opcional para provocar un error de prueba |

| app/routers/tasks.py | Operaciones de tareas |

| app/routers/projects.py | Operaciones de proyectos |

| app/routers/status.py | Salud, versión y conectividad |

| app/schemas.py | Schemas de tareas y proyectos |

| pruebas/index.html | Página para comprobar CORS desde el navegador |



\## Qué es un middleware



Es una capa que interviene en el recorrido de las peticiones y respuestas.



Permite aplicar funciones comunes sin repetirlas dentro de cada endpoint.

En esta práctica se utiliza para medir tiempos, añadir cabeceras,

registrar peticiones y aplicar CORS.



La aplicación utiliza middleware ASGI para intervenir en el envío

de las cabeceras de respuesta.



\## Orden de ejecución



La petición pasa por:



1\. ProcessTimeMiddleware.

2\. CORSMiddleware.

3\. La aplicación FastAPI y sus routers.



Las respuestas regresan a través de las capas exteriores.



El middleware de tiempo crea el identificador e inicia la medición

antes de que se ejecute el endpoint o el handler de errores.



CORS envuelve toda la aplicación FastAPI, por lo que también puede

añadir sus cabeceras a las respuestas 500 del handler global.



ProcessTimeMiddleware es la capa exterior para añadir sus cabeceras

tanto a las respuestas de FastAPI como a las respuestas preflight

generadas por CORS.



\## Tiempo de procesamiento



Se utiliza perf\_counter() y se convierte el resultado a milisegundos.



La cabecera X-Process-Time contiene un valor numérico con tres decimales.



La medición termina cuando comienzan a enviarse las cabeceras.

No representa el tiempo completo de descarga hasta el navegador.



\## Identificador de petición



Se genera un UUID para cada petición HTTP y se devuelve mediante

X-Request-ID.



El mismo identificador se guarda en el estado de la petición para

que el handler de errores pueda consultarlo.



Esto permite relacionar:



\- La respuesta recibida por el cliente.

\- El registro de la petición.

\- El registro de una excepción interna.



\## Configuración CORS



Por defecto se permite:



http://localhost:5173



Configuración utilizada:



| Opción | Valor |

|---|---|

| allow\_origins | Lista obtenida de CORS\_ORIGINS |

| allow\_methods | GET y POST |

| allow\_headers | Content-Type |

| allow\_credentials | false |

| expose\_headers | X-Process-Time y X-Request-ID |



Los métodos y cabeceras corresponden a las operaciones actuales

y al envío de JSON.



No se habilitan credenciales porque esta práctica no utiliza

autenticación mediante cookies.



expose\_headers permite que JavaScript lea nuestras cabeceras

desde un origen distinto al de la API.



No basta con que las cabeceras aparezcan en DevTools: para leerlas

mediante response.headers.get(), deben estar expuestas por CORS.



\## Orígenes por entorno



La variable CORS\_ORIGINS acepta una lista separada por comas.



Ejemplo en PowerShell, antes de arrancar el servidor:



```powershell

$env:CORS\_ORIGINS = "http://localhost:5173"

```



En otro entorno se deben indicar los orígenes reales del frontend.



Se rechaza el comodín \* para mantener una lista explícita.

Un origen se especifica mediante protocolo, nombre de host y puerto,

sin añadir rutas como /docs.



CORS es una política aplicada por los navegadores.

No sustituye a la autenticación ni impide por sí solo peticiones

desde clientes como curl.



\## Manejo global de excepciones



La aplicación registra:



```python

api.add\_exception\_handler(Exception, unhandled\_exception\_handler)

```



El handler devuelve HTTP 500 con este formato:



```json

{

&#x20; "error": "Se ha producido un error interno en el servidor.",

&#x20; "error\_code": "INTERNAL\_SERVER\_ERROR",

&#x20; "request\_id": "identificador-de-la-peticion"

}

```



El mensaje público no incluye el texto original de la excepción

ni el traceback.



El servidor registra la excepción completa junto con el identificador

para facilitar su diagnóstico.



debug=False evita que FastAPI genere páginas de depuración

con detalles internos.



Este esquema se aplica a las excepciones no controladas.

Los errores de validación 422 y los errores HTTP gestionados conservan

los formatos predeterminados de FastAPI.



Si una respuesta ya ha empezado a enviarse, por ejemplo durante

streaming, no es posible sustituirla por un nuevo JSON 500.

Las pruebas de esta práctica utilizan respuestas JSON normales.



\## Ruta de prueba



GET /debug/error provoca una excepción RuntimeError.



Solo se registra cuando ENABLE\_DEBUG\_ROUTES tiene el valor true.

Es una herramienta de diagnóstico y debe permanecer deshabilitada

fuera de las pruebas.



\## Preparación en Windows



Desde la raíz del repositorio:



```powershell

cd .\\practicas\\desarrollo\\1.4-middleware

py -3 -m venv .venv

.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt

```



Utilizar Python 3.13 o superior y comprobar previamente la versión:



```powershell

py -3 --version

```



\## Arranque de la API para pruebas



Desde la carpeta de esta práctica:



```powershell

$env:ENABLE\_DEBUG\_ROUTES = "true"

$env:CORS\_ORIGINS = "http://localhost:5173"

.\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --reload --port 8002

```



Swagger:



http://127.0.0.1:8002/docs



\## Servidor de la página de pruebas



En otra terminal, desde la misma carpeta:



```powershell

.\\.venv\\Scripts\\python.exe -m http.server 5173 --bind 127.0.0.1 --directory pruebas

```



Abrir:



http://localhost:5173



La página permite consultar /health y /debug/error y muestra

el estado HTTP, las cabeceras personalizadas y el cuerpo JSON.



\## Pruebas y resultados esperados



| Prueba | Resultado esperado |

|---|---|

| GET /health | HTTP 200 y cabeceras personalizadas |

| GET /debug/error | HTTP 500 con mensaje genérico |

| Cabeceras del error 500 | X-Process-Time y X-Request-ID presentes |

| GET /health después del error | HTTP 200 sin reiniciar |

| Petición con Origin localhost:5173 | Access-Control-Allow-Origin para ese origen |

| Preflight de POST con Content-Type | HTTP 200 con permisos CORS |

| Página en localhost:5173 | JavaScript lee cuerpo y cabeceras |

| Página en 127.0.0.1:5173 | El navegador bloquea la lectura por CORS |



localhost y 127.0.0.1 son nombres de host diferentes y, por tanto,

constituyen orígenes distintos aunque apunten al mismo equipo.



Un bloqueo CORS puede producirse aunque el servidor responda HTTP 200:

el navegador impide que el JavaScript lea esa respuesta.



\## Comprobaciones con curl



Ejecutar en PowerShell mientras la API está funcionando.



Origen permitido:



```powershell

curl.exe -i -H "Origin: http://localhost:5173" http://127.0.0.1:8002/health

```



Preflight:



```powershell

curl.exe -i -X OPTIONS http://127.0.0.1:8002/tasks -H "Origin: http://localhost:5173" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: Content-Type"

```



Error con CORS:



```powershell

curl.exe -i -H "Origin: http://localhost:5173" http://127.0.0.1:8002/debug/error

```



Las respuestas preflight también deben incluir X-Process-Time

y X-Request-ID.



\## Evidencias de la entrega



El documento de capturas acompaña esta práctica e incluye:



\- Arranque de la aplicación.

\- Cabeceras de /health en DevTools.

\- Respuesta 500 sin detalles internos.

\- Respuesta 200 posterior al error.

\- Comprobaciones de CORS y preflight.

\- Lectura desde el origen permitido.

\- Bloqueo desde el origen no autorizado.



Conservar únicamente evidencias realmente obtenidas.

Los valores de tiempo e identificador cambian en cada petición.



\## Parada y desactivación de la ruta de diagnóstico



Pulsar Ctrl+C en cada terminal de servidor.



En la terminal donde se activó la ruta de diagnóstico:



```powershell

Remove-Item Env:ENABLE\_DEBUG\_ROUTES -ErrorAction SilentlyContinue

```



Al arrancar de nuevo Uvicorn sin esa variable, /debug/error

no estará registrado.



\## Alcance



La práctica conserva la creación simulada de tareas y proyectos.

No incorpora base de datos ni autenticación.



El registro incluye método, ruta, estado, identificador y tiempo.

No registra el cuerpo de las peticiones.



\[Volver al índice principal](../../../README.md)

