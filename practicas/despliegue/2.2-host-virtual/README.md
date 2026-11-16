\# Práctica 2.2 — Host virtual taskflow.local



\## Objetivo



Configurar Apache para servir una página de TaskFlow mediante el nombre

taskflow.local, manteniendo un sitio localhost independiente y registros

separados para cada host virtual.



\## Entorno utilizado



\- Ubuntu Server con Apache.

\- Administración mediante SSH.

\- IP del servidor durante la práctica: 172.20.10.11.

\- Cliente Windows con navegador web.

\- Sitio TaskFlow: http://taskflow.local.

\- DocumentRoot de TaskFlow: /var/www/taskflow.

\- DocumentRoot de localhost: /var/www/localhost.



La dirección IP puede cambiar según la red utilizada.



\## Página publicada



La carpeta frontend contiene una página estática sencilla creada para

esta práctica.



Incluye una presentación de TaskFlow, un proyecto de ejemplo y tres

tareas que se pueden marcar.



No necesita compilación. El archivo index.html se copia directamente a

/var/www/taskflow/index.html.



Los datos son de demostración: la página no está conectada a la API

ni guarda los cambios en una base de datos.



\## Archivos incluidos



\- frontend/index.html: página de TaskFlow.

\- config/taskflow.conf: configuración del host taskflow.local.

\- config/000-localhost.conf: configuración del sitio localhost.

\- evidencias/configtest.txt: comprobación de sintaxis.

\- evidencias/hosts-virtuales.txt: hosts virtuales activos.

\- evidencias/taskflow-accesos.txt: petición registrada por TaskFlow.

\- evidencias/localhost-accesos.txt: petición registrada por localhost.



\## Configuración de TaskFlow



La configuración está en:



/etc/apache2/sites-available/taskflow.conf



Su contenido se conserva en config/taskflow.conf.



Las directivas principales son:



\- VirtualHost \*:80: atiende conexiones HTTP en el puerto 80.

\- ServerName taskflow.local: identifica el nombre del sitio.

\- DocumentRoot /var/www/taskflow: indica la carpeta publicada.

\- Options -Indexes: desactiva el listado automático de directorios.

\- AllowOverride None: no permite cambios mediante archivos .htaccess.

\- Require all granted: permite acceder al directorio publicado.

\- DirectoryIndex index.html: utiliza index.html como página inicial.

\- ErrorLog y CustomLog: definen los registros propios del sitio.



\## Sitio localhost independiente



Se creó un segundo host virtual en:



/etc/apache2/sites-available/000-localhost.conf



Este sitio utiliza ServerName localhost y publica /var/www/localhost.



Su página muestra el título «Sitio localhost», mientras que

taskflow.local muestra «TaskFlow».



El host localhost figura como predeterminado en la salida de

apache2ctl -S.



\## Activación y validación



Se activaron los dos sitios y se desactivó el sitio inicial de Apache:



```bash

sudo a2ensite 000-localhost.conf taskflow.conf

sudo a2dissite 000-default.conf

sudo apache2ctl configtest

```



La comprobación devolvió:



```text

Syntax OK

```



Después se recargó Apache:



```bash

sudo systemctl reload apache2

```



Los hosts activos se comprobaron con:



```bash

sudo apache2ctl -S

```



La salida identifica localhost como sitio predeterminado y

taskflow.local como otro host virtual del puerto 80.

000-default.conf no aparece entre los sitios activos.



\## Resolución del nombre



En Ubuntu se añadió esta entrada a /etc/hosts:



```text

127.0.0.1 taskflow.local

```



En el archivo hosts de Windows se añadió:



```text

172.20.10.11 taskflow.local

```



El archivo de Windows se encuentra en:



```text

C:\\Windows\\System32\\drivers\\etc\\hosts

```



La entrada de Ubuntu permite probar el sitio desde el propio servidor.

La de Windows permite acceder al servidor desde el navegador del cliente.



Si cambia la IP del servidor, debe actualizarse la entrada de Windows.



\## Comprobación de las páginas



Desde Ubuntu se ejecutó:



```bash

curl --noproxy '\*' -s http://taskflow.local | grep '<h1>'

curl --noproxy '\*' -s http://localhost | grep '<h1>'

```



Las respuestas mostraron títulos diferentes:



```html

<h1>TaskFlow</h1>

<h1>Sitio localhost</h1>

```



También se abrió http://taskflow.local desde el navegador de Windows y

se comprobó que aparecía la página de TaskFlow.



La comprobación de localhost se realiza dentro de Ubuntu: localhost

siempre se refiere al equipo desde el que se hace la petición.



\## Registros independientes



TaskFlow utiliza:



```text

/var/log/apache2/taskflow-access.log

/var/log/apache2/taskflow-error.log

```



Localhost utiliza:



```text

/var/log/apache2/localhost-access.log

/var/log/apache2/localhost-error.log

```



Se generaron peticiones identificables desde Ubuntu:



```bash

curl --noproxy '\*' -s -o /dev/null -w 'TaskFlow: %{http\_code}\\n' 'http://taskflow.local/?prueba=taskflow-22'

curl --noproxy '\*' -s -o /dev/null -w 'Localhost: %{http\_code}\\n' 'http://localhost/?prueba=localhost-22'

```



Las dos devolvieron el código HTTP 200.



Las evidencias guardadas contienen la petición prueba=taskflow-22

en el registro de TaskFlow y prueba=localhost-22 en el de localhost.



\## Resultado



Apache sirve la página estática de TaskFlow mediante taskflow.local.

El sitio localhost muestra un contenido distinto, cada host tiene

configurados sus propios registros y la sintaxis de Apache es válida.



Esta práctica utiliza HTTP. No incluye la configuración de HTTPS

ni la conexión del frontend con la API.

