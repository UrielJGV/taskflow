\# Funcionamiento de los hosts virtuales



\## Varios sitios en un mismo servidor



Los hosts virtuales permiten que Apache publique varios sitios web

desde un mismo servidor.



En esta práctica, los dos sitios utilizan el puerto 80, pero tienen

nombres y carpetas diferentes:



| Nombre | Carpeta publicada | Configuración |

| --- | --- | --- |

| taskflow.local | /var/www/taskflow | taskflow.conf |

| localhost | /var/www/localhost | 000-localhost.conf |



\## Cómo selecciona Apache el sitio



Primero, el cliente resuelve el nombre para obtener la dirección IP

del servidor. En esta práctica se utilizan entradas del archivo hosts.



Después, el navegador envía una petición HTTP que incluye el nombre

solicitado en la cabecera Host.



Para una petición a http://taskflow.local, la cabecera contiene:



```http

Host: taskflow.local

```



Apache busca entre los hosts virtuales de la dirección y el puerto

correspondientes. Compara el nombre solicitado con las directivas

ServerName y, si existen, ServerAlias.



Cuando encuentra taskflow.local, utiliza su configuración y sirve

el contenido de /var/www/taskflow.



Si no encuentra un nombre coincidente, utiliza el primer host virtual

de ese conjunto de dirección y puerto.



En esta configuración, apache2ctl -S muestra localhost como

predeterminado. Así, TaskFlow no queda como sitio de respaldo para

los nombres desconocidos.



\## Función del archivo hosts



El archivo hosts relaciona un nombre con una dirección IP.

No configura Apache ni selecciona una carpeta del servidor.



Por tanto, hacen falta dos elementos:



1\. Resolver taskflow.local hacia la IP del servidor.

2\. Configurar Apache para reconocer ese nombre y publicar su contenido.



\## Separación entre los sitios



Cada host virtual tiene su propio DocumentRoot y sus propios registros

de acceso y errores.



Esto permite organizar los archivos de cada sitio y consultar sus

peticiones por separado.



Esta separación no equivale al aislamiento de una máquina virtual:

los sitios siguen compartiendo el servicio Apache y los recursos

del servidor.



\## Uso en desarrollo y producción



En desarrollo, los nombres locales y el archivo hosts permiten probar

varios sitios sin contratar un dominio.



En producción, normalmente se utilizan dominios registrados y DNS.

También deben configurarse HTTPS, certificados y los controles de

seguridad adecuados.



Los hosts virtuales permiten publicar distintos dominios o subdominios

en un mismo servidor, cada uno con su contenido y configuración.



\## Ejemplo de ampliación: un tercer sitio



El siguiente ejemplo es una propuesta de ampliación.

No forma parte de la configuración aplicada en esta práctica.



Para añadir un sitio llamado proyectos.test, se podría crear la carpeta

/var/www/proyectos con su propio index.html y guardar esta configuración

en /etc/apache2/sites-available/proyectos.conf:



```apache

<VirtualHost \*:80>

&#x20;   ServerName proyectos.test

&#x20;   DocumentRoot /var/www/proyectos



&#x20;   <Directory /var/www/proyectos>

&#x20;       Options -Indexes

&#x20;       AllowOverride None

&#x20;       Require all granted

&#x20;   </Directory>



&#x20;   DirectoryIndex index.html



&#x20;   ErrorLog ${APACHE\_LOG\_DIR}/proyectos-error.log

&#x20;   CustomLog ${APACHE\_LOG\_DIR}/proyectos-access.log combined

</VirtualHost>

```



Después habría que activar el sitio y comprobar la sintaxis:



```bash

sudo a2ensite proyectos.conf

sudo apache2ctl configtest

```



Solo si la comprobación es correcta, se recargaría Apache:



```bash

sudo systemctl reload apache2

```



Para acceder desde Windows, se añadiría al archivo hosts una entrada

con la IP vigente del servidor:



```text

172.20.10.11 proyectos.test

```



Finalmente, se abriría http://proyectos.test y se comprobarían su página

y sus registros.

