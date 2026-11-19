\# Práctica 1.7 — Autenticación JWT



\## Objetivo



Incorporar autenticación mediante tokens JWT a la API TaskFlow,

partiendo del CRUD de la práctica 1.6.



Se implementan el registro, el inicio de sesión, la consulta del

usuario autenticado y la protección de las operaciones de escritura

de tareas y proyectos.



\## Funcionalidades



\- POST /auth/register: registra un usuario y guarda su contraseña como hash.

\- POST /auth/login: verifica las credenciales y devuelve un JWT.

\- GET /users/me: devuelve los datos públicos del usuario autenticado.

\- POST, PUT y DELETE de tareas y proyectos: requieren un token válido.

\- Tokens con una duración de 30 minutos.

\- Respuestas 401 con la cabecera WWW-Authenticate: Bearer.

\- Contraseñas almacenadas mediante bcrypt con coste 12.

\- Firma de tokens mediante HS256 y una clave externa al código.



Se conservan los filtros, la paginación, los contadores, las relaciones

y las reglas de borrado del CRUD anterior.



\## Estructura principal



\- app/models.py: modelos y campo hashed\_password.

\- app/security.py: hash, verificación de contraseñas y creación de JWT.

\- app/dependencies.py: validación del token y obtención del usuario.

\- app/routers/auth.py: registro e inicio de sesión.

\- app/routers/users.py: consulta del usuario autenticado.

\- app/routers/tasks.py: CRUD de tareas con escritura protegida.

\- app/routers/projects.py: CRUD de proyectos con escritura protegida.

\- app/main.py: registro de routers y configuración de middleware.

\- requirements.txt: dependencias de la aplicación base.

\- requirements-auth.txt: dependencias base y de autenticación.

\- evidencias/: resultados de las comprobaciones.



\## Ejecución en Windows



Los siguientes comandos se ejecutan en PowerShell.



Desde la raíz del repositorio:



```powershell

cd .\\practicas\\desarrollo\\1.7-jwt

```



Crear el entorno virtual si todavía no existe:



```powershell

py -m venv .venv

```



Instalar todas las dependencias:



```powershell

.\\.venv\\Scripts\\python.exe -m pip install -r requirements-auth.txt

```



Generar una clave aleatoria para esta sesión:



```powershell

$env:JWT\_SECRET\_KEY = \& .\\.venv\\Scripts\\python.exe -c "import secrets; print(secrets.token\_hex(32))"

```



Arrancar la API desde esa misma ventana:



```powershell

.\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --reload --port 8005

```



Abrir Swagger:



http://127.0.0.1:8005/docs



La clave permanece en esa sesión de PowerShell. Si se cierra la ventana,

debe volver a configurarse antes de arrancar la aplicación.



Generar una clave diferente invalida los tokens firmados con la anterior.

Para conservar los tokens entre reinicios sería necesario mantener

la misma clave mediante una configuración segura.



El código lee JWT\_SECRET\_KEY del entorno; no carga automáticamente

un archivo .env.



\## Base de datos



Por defecto, SQLite utiliza el archivo taskflow.db situado dentro

de la carpeta de esta práctica.



La variable DATABASE\_URL permite sustituir esa ubicación. Si está

definida, debe comprobarse que apunta a la base de datos deseada.



Las tablas se crean al arrancar la aplicación.



Esta práctica se inició sin una base de datos previa, de modo que

la tabla users se creó incluyendo hashed\_password.



create\_all no modifica automáticamente las columnas de tablas existentes.

No debe reutilizarse una base de datos de la práctica anterior sin

preparar su correspondiente migración.



La base de datos local está excluida de Git.



\## Registro



En Swagger se utiliza POST /auth/register.



El cuerpo es JSON y contiene:



```json

{

&#x20; "username": "uriel",

&#x20; "email": "uriel@example.com",

&#x20; "password": "SUSTITUIR-POR-UNA-CONTRASENA-EXCLUSIVA"

}

```



La contraseña del ejemplo debe sustituirse por una propia.

Este JSON se introduce en Request body de Swagger, no en PowerShell.



Requisitos:



\- Username: entre 3 y 100 caracteres; letras ASCII, números, guion,

&#x20; punto o guion bajo.

\- Email: comprobación básica de formato y un máximo de 254 caracteres.

\- Contraseña: al menos 12 caracteres y un máximo de 72 bytes en UTF-8.



Los espacios de la contraseña se conservan.



El límite de bytes evita que bcrypt trunque silenciosamente

contraseñas demasiado largas.



Un registro correcto devuelve 201 con:



\- id

\- username

\- email



La respuesta no incluye la contraseña ni su hash.



Los conflictos de nombre o correo devuelven 409 con un mensaje genérico.

Aunque no se identifica qué campo está ocupado, esta diferencia de

respuesta puede permitir inferir que existe un conflicto de registro.



\## Inicio de sesión



POST /auth/login recibe un formulario con username y password,

mediante OAuth2PasswordRequestForm.



Un inicio de sesión válido devuelve:



\- access\_token: JWT firmado.

\- token\_type: bearer.

\- expires\_in: 1800 segundos.



Si el usuario no existe o la contraseña es incorrecta, devuelve el mismo

mensaje genérico y el código 401.



Se comprueba un hash ficticio cuando el usuario no existe para reducir

las diferencias de tiempo entre ambos casos. Esto no garantiza

tiempos de respuesta idénticos.



\## Autorización desde Swagger



1\. Pulsar Authorize.

2\. Introducir el usuario y la contraseña registrados.

3\. Dejar client\_id y client\_secret vacíos.

4\. Pulsar Authorize y cerrar el cuadro.

5\. Ejecutar GET /users/me.



Swagger obtiene el token mediante /auth/login y lo envía en las

peticiones protegidas.



La cabecera utilizada es:



```http

Authorization: Bearer TOKEN

```



No deben incluirse tokens reales en capturas ni documentación.



\## Contenido y validación del JWT



El token contiene:



\- sub: identificador del usuario convertido a texto.

\- iat: instante de emisión.

\- exp: instante de expiración, 30 minutos después de la emisión.



Se firma mediante HS256.



La validación permite únicamente el algoritmo configurado, exige

sub y exp, verifica la firma y comprueba la expiración.



Después se valida el formato del identificador y se busca al usuario

en la base de datos.



Un token firmado correctamente no permite acceder si su usuario

ya no existe.



El JWT está firmado, no cifrado. Su contenido puede leerse sin conocer

la clave, por lo que no contiene contraseñas ni otros secretos.



\## Dependencias anidadas



Las rutas protegidas utilizan get\_current\_user.



Esta dependencia utiliza:



\- OAuth2PasswordBearer para obtener el token.

\- get\_db para acceder a una sesión de base de datos.



Así, la autenticación se reutiliza sin repetir su implementación

en cada operación.



Las operaciones de escritura incluyen:



```python

dependencies=\[Depends(get\_current\_user)]

```



\## Alcance de la protección



Requieren JWT:



\- POST /tasks

\- PUT /tasks/{task\_id}

\- DELETE /tasks/{task\_id}

\- POST /projects

\- PUT /projects/{project\_id}

\- DELETE /projects/{project\_id}

\- GET /users/me



El registro y el inicio de sesión son públicos.



Las consultas GET de tareas y proyectos permanecen públicas.

Las rutas de categorías conservan el comportamiento de la práctica

anterior y no se protegen con JWT en esta entrega.



No hay roles ni permisos por propietario: cualquier usuario autenticado

puede realizar las operaciones protegidas de tareas y proyectos.



\## Comprobaciones realizadas



| Comprobación | Resultado |

| --- | --- |

| Registro de usuario | 201 |

| Repetición del registro | 409 |

| Creación de proyecto con token válido | 201 |

| POST de tareas sin token | 401 |

| PUT de tareas sin token | 401 |

| DELETE de tareas sin token | 401 |

| POST de proyectos sin token | 401 |

| PUT de proyectos sin token | 401 |

| DELETE de proyectos sin token | 401 |

| Consulta con token de prueba caducado | 401 y WWW-Authenticate: Bearer |



Se realizó también una comprobación local del formato bcrypt

y de su coste, sin imprimir el hash completo.



\## Prueba de expiración



Para comprobar el rechazo sin esperar 30 minutos, se generó localmente

un token firmado con la misma clave de la API, con:



\- iat situado 31 minutos antes del momento de la prueba.

\- exp situado un minuto antes del momento de la prueba.



Se envió a GET /users/me y se obtuvo 401.



Esta prueba utiliza una fecha de expiración ya pasada.

No representa una espera real de 30 minutos después de un login.



Los tokens emitidos por /auth/login mantienen su duración normal

de 30 minutos.



No se añadió un endpoint público para fabricar tokens caducados.



\## Evidencias



\- \[Escritura sin token](evidencias/escritura-sin-token.txt)

\- \[Rechazo del token caducado](evidencias/token-expirado.txt)

\- \[Resumen del almacenamiento de contraseñas](evidencias/hash-contrasenas.txt)



Las capturas del registro, la autorización y las respuestas observadas

se recogen en el documento de entrega.



\## Decisiones de seguridad



\### Hash de contraseñas



Se utiliza passlib con bcrypt y coste 12.



Cada hash genera una sal aleatoria. Por ello, dos usuarios que elijan

la misma contraseña no deberían tener el mismo hash.



El coste 12 aumenta el trabajo necesario para comprobar cada contraseña,

dificultando los ataques de adivinación sobre hashes robados.

Debe revisarse según el rendimiento del servidor.



Se fija bcrypt 4.0.1 por compatibilidad con passlib 1.7.4,

siguiendo las librerías exigidas por el enunciado.



\### Clave de firma



La clave se genera con secrets y se proporciona mediante una variable

de entorno.



No está escrita en el código ni se incluye en Git.



La aplicación exige una longitud mínima, pero esa comprobación por sí

sola no garantiza aleatoriedad: debe utilizarse una clave generada

de forma segura.



\### Respuestas de autenticación



Los fallos de autenticación devuelven 401 y WWW-Authenticate: Bearer.



Los mensajes no distinguen entre un usuario inexistente y una

contraseña incorrecta durante el login.



\### Transporte



La práctica se prueba en localhost mediante HTTP.



En un despliegue real debe utilizarse HTTPS: quien obtenga un token

Bearer puede utilizarlo mientras siga siendo válido.



CORS permite la cabecera Authorization, pero no sustituye

la autenticación ni impide el acceso desde clientes ajenos al navegador.



\## Amenazas y limitaciones



\- Robo de tokens: requiere HTTPS y almacenamiento cuidadoso en el cliente.

\- Fuerza bruta: no se ha implementado limitación de intentos de login.

\- Filtración de la clave: permitiría fabricar tokens; exige protegerla

&#x20; y sustituirla si queda expuesta.

\- Filtración de la base de datos: bcrypt dificulta la recuperación

&#x20; de contraseñas, pero no elimina el riesgo.

\- Enumeración de usuarios: los conflictos de registro pueden aportar

&#x20; información aunque el mensaje sea genérico.

\- Revocación: no hay lista de tokens revocados. Un token válido puede

&#x20; seguir funcionando hasta expirar, salvo que cambie la clave o se

&#x20; elimine el usuario.

\- Un cambio de contraseña no revoca automáticamente los tokens existentes.

\- No se implementan refresh tokens, rotación de refresh tokens,

&#x20; scopes por rol ni autorización por propietario.



\## Conservación de las prácticas anteriores



El código de esta entrega está en su propia carpeta.



La práctica 1.6 conserva su versión del CRUD y no necesita los cambios

de autenticación de esta práctica.

