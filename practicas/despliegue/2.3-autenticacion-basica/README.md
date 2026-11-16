# Práctica 2.3 — Autenticación básica de admin

## Objetivo

Proteger la zona /admin de TaskFlow mediante autenticación HTTP básica
en Apache.

El acceso sin credenciales debe devolver 401 y el acceso con las
credenciales correctas del usuario admin debe devolver 200.

## Entorno

- Ubuntu Server con Apache.
- Administración mediante SSH.
- Sitio: http://taskflow.local.
- DocumentRoot: /var/www/taskflow.
- Zona protegida: /var/www/taskflow/admin.
- Configuración: /etc/apache2/sites-available/taskflow.conf.
- Archivo de contraseñas: /etc/apache2/.htpasswd.

Esta práctica continúa la configuración del host virtual de la práctica 2.2.

## Archivos incluidos

- config/taskflow.conf: configuración de Apache con autenticación.
- admin/index.html: página de administración.
- evidencias/configtest.txt: comprobación de sintaxis.
- evidencias/sin-credenciales.txt: respuesta sin autenticación.
- evidencias/con-credenciales.txt: respuesta con autenticación válida.

El archivo .htpasswd no se incluye en el repositorio porque contiene
el hash de la contraseña del usuario.

## Creación de la zona de administración

Se creó el directorio:

```bash
sudo install -d -m 755 /var/www/taskflow/admin
```

Dentro se guardó un archivo index.html con el título
«Administración de TaskFlow».

Una copia de esa página se conserva en admin/index.html.

## Creación del usuario

Se comprobó que htpasswd estaba instalado y que el archivo de
contraseñas no existía.

Después se ejecutó:

```bash
sudo htpasswd -cB /etc/apache2/.htpasswd admin
```

El programa solicitó la contraseña dos veces, sin mostrarla en pantalla.

- -c crea el archivo. Solo debe utilizarse la primera vez, porque
  sobrescribe un archivo existente.
- -B utiliza bcrypt para almacenar el hash de la contraseña.

La contraseña se introduce de forma interactiva para evitar escribirla
como argumento en el historial de comandos.

## Permisos del archivo

Se aplicaron estos permisos:

```bash
sudo chown root:www-data /etc/apache2/.htpasswd
sudo chmod 640 /etc/apache2/.htpasswd
```

El propietario root puede leer y modificar el archivo.
El grupo www-data, utilizado por Apache, puede leerlo.
Los demás usuarios no tienen acceso mediante esos permisos.

El archivo está fuera del DocumentRoot y no se publica como parte
del sitio web.

## Configuración de Apache

Se guardó una copia de la configuración anterior:

```bash
sudo cp -n /etc/apache2/sites-available/taskflow.conf /etc/apache2/sites-available/taskflow.conf.antes-auth
```

Dentro del VirtualHost se añadió:

```apache
<Directory /var/www/taskflow/admin>
    AuthType Basic
    AuthName "Administracion de TaskFlow"
    AuthBasicProvider file
    AuthUserFile /etc/apache2/.htpasswd
    Require user admin
</Directory>
```

Las directivas tienen estas funciones:

- AuthType Basic: selecciona autenticación HTTP básica.
- AuthName: identifica la zona de autenticación.
- AuthBasicProvider file: comprueba las credenciales mediante un archivo.
- AuthUserFile: indica la ubicación de los usuarios y sus hashes.
- Require user admin: permite acceder al usuario admin con contraseña válida.

La configuración completa está en config/taskflow.conf.

La protección se aplica al directorio admin y a su contenido.
La página principal conserva su configuración de acceso público.

## Validación y aplicación

Se comprobó la sintaxis:

```bash
sudo apache2ctl configtest
```

Resultado:

```text
Syntax OK
```

Después se aplicó la configuración:

```bash
sudo systemctl reload apache2
```

## Prueba sin credenciales

Desde Ubuntu se ejecutó:

```bash
curl --noproxy '*' -s -o /dev/null -w 'Sin credenciales: %{http_code}\n' http://taskflow.local/admin/
```

Resultado observado:

```text
Sin credenciales: 401
```

Apache rechazó el acceso sin credenciales.

## Prueba con credenciales correctas

Se ejecutó:

```bash
curl --noproxy '*' -u admin -s -o /dev/null -w 'Con credenciales: %{http_code}\n' http://taskflow.local/admin/
```

curl solicitó la contraseña de admin de forma interactiva.

Resultado observado:

```text
Con credenciales: 200
```

Apache permitió el acceso con las credenciales correctas.

Las salidas se guardaron en la carpeta evidencias.

## Funcionamiento de la autenticación básica

Si el cliente solicita la zona protegida sin credenciales, Apache
responde con 401 y una cabecera WWW-Authenticate que identifica
el método Basic y la zona de autenticación.

El cliente puede repetir la petición enviando una cabecera Authorization
con el usuario y la contraseña codificados en Base64.

Base64 es una codificación reversible, no un cifrado.
Una persona que pueda observar el tráfico HTTP podría recuperar
las credenciales.

Por ello, en un entorno real debe utilizarse HTTPS para cifrar
la comunicación.

bcrypt protege el almacenamiento de la contraseña en el servidor,
pero no cifra las credenciales durante su transmisión.

## Política de contraseñas

La política indicada para esta práctica es utilizar una contraseña
exclusiva de al menos 16 caracteres, evitando nombres, fechas,
secuencias previsibles y contraseñas reutilizadas.

La longitud y la falta de predictibilidad dificultan la adivinación.
Utilizar una contraseña exclusiva reduce el impacto de una filtración
en otro servicio.

El comando utilizado no impone automáticamente esta longitud:
el usuario debe elegir una contraseña que cumpla la política.

La contraseña no debe aparecer en capturas, documentación ni archivos
del repositorio.

### Rotación de la contraseña

Para cambiar la contraseña de admin:

```bash
sudo htpasswd -B /etc/apache2/.htpasswd admin
```

No se utiliza -c porque el archivo ya existe.

Después se debe comprobar que la contraseña anterior falla y que
la nueva permite acceder.

La contraseña debe cambiarse si se sospecha que ha quedado expuesta.

## Gestión de usuarios

Los siguientes comandos son ejemplos de administración.
No forman parte de las pruebas realizadas.

Para añadir otro usuario:

```bash
sudo htpasswd -B /etc/apache2/.htpasswd operador
```

Para eliminarlo:

```bash
sudo htpasswd -D /etc/apache2/.htpasswd operador
```

Crear un usuario en el archivo no le concede acceso con la configuración
actual, porque se exige Require user admin.

Para permitir también a operador, la directiva tendría que ser:

```apache
Require user admin operador
```

Después de cambiar la configuración habría que comprobar la sintaxis
y recargar Apache.

## Alternativas de autenticación

- Digest: utiliza un mecanismo de desafío y respuesta. No sustituye
  HTTPS ni cifra el contenido de la comunicación.
- Formularios con sesión: la aplicación valida el inicio de sesión
  y mantiene la autenticación mediante una sesión, normalmente
  identificada por una cookie.
- JWT: es un formato de token que puede utilizarse en sistemas de
  autenticación y autorización. Requiere validar correctamente
  la firma, la caducidad y las demás condiciones del token.

Las cookies y los tokens también deben protegerse mediante HTTPS.

## Resultado y alcance

Las pruebas muestran que /admin/ devuelve 401 sin credenciales
y 200 con las credenciales correctas del usuario admin.

La protección corresponde a una página estática servida por Apache.
No implementa autenticación en la API FastAPI.

La práctica utiliza HTTP en un entorno de laboratorio.
HTTPS queda fuera de esta configuración.
