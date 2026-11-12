\# Práctica 2.1 — Módulos de Apache



\## Objetivo



Activar los módulos de Apache necesarios para preparar el despliegue del proyecto:



\- proxy

\- proxy\_http

\- ssl

\- rewrite

\- headers



Comprobar la configuración, reiniciar Apache y documentar el propósito de cada módulo.



\## Entorno de trabajo



\- Ubuntu Server en una máquina virtual de VirtualBox.

\- Administración mediante SSH desde PowerShell de Windows.

\- Servidor web Apache.

\- Repositorio y documentación organizados por prácticas.



La dirección IP de la máquina virtual puede cambiar. Antes de conectarse se puede consultar con:



```bash

hostname -I

```



\## Qué es un módulo de Apache



Un módulo es un componente que añade funcionalidades al servidor web, como proxy, cifrado TLS, reescritura de URLs o gestión de cabeceras.



Apache utiliza una arquitectura modular: se habilitan las funciones necesarias para cada despliegue.



En Ubuntu, `a2enmod` habilita los módulos instalados. Después se comprueba la configuración y se reinicia o recarga Apache para aplicar los cambios.



La etiqueta `(shared)` de la lista de módulos indica que el módulo se carga dinámicamente.



\## 1. Comprobación inicial



Consultar la versión:



```bash

apache2 -v

```



Consultar el estado del servicio:



```bash

sudo systemctl status apache2 --no-pager -l

```



Consultar los módulos cargados:



```bash

sudo apache2ctl -M

```



Las capturas iniciales permiten comparar el estado del servidor antes y después de la activación.



\## 2. Activación de los módulos



```bash

sudo a2enmod proxy proxy\_http ssl rewrite headers

```



Si aparece `already enabled`, el módulo ya estaba habilitado.



La herramienta también puede habilitar dependencias necesarias.



Antes de reiniciar:



```bash

sudo apache2ctl configtest

```



El resultado esperado es:



```text

Syntax OK

```



Después:



```bash

sudo systemctl restart apache2

```



\## 3. Aviso encontrado y solución



Durante la comprobación apareció el aviso:



```text

AH00558: Could not reliably determine the server's fully qualified domain name

```



Apache no tenía definido un `ServerName` global y utilizaba un valor deducido.



Para este entorno local se creó una configuración independiente:



```bash

echo 'ServerName localhost' | sudo tee /etc/apache2/conf-available/taskflow-servername.conf

```



Se activó mediante:



```bash

sudo a2enconf taskflow-servername

```



Se comprobó la sintaxis y se reinició:



```bash

sudo apache2ctl configtest

sudo systemctl restart apache2

```



`ServerName localhost` identifica el servidor principal en este entorno de prácticas. No configura un dominio público ni limita por sí solo las interfaces de red donde escucha Apache.



Los futuros VirtualHost pueden definir su propio ServerName.



\## 4. Verificación final



Consultar el servicio:



```bash

sudo systemctl status apache2 --no-pager -l

```



El estado esperado es:



```text

active (running)

```



Filtrar los cinco módulos solicitados:



```bash

sudo apache2ctl -M | grep -E '^\[\[:space:]]\*(proxy|proxy\_http|ssl|rewrite|headers)\_module\[\[:space:]]'

```



La salida debe contener:



```text

headers\_module (shared)

proxy\_module (shared)

proxy\_http\_module (shared)

rewrite\_module (shared)

ssl\_module (shared)

```



El orden puede variar.



\## 5. Propósito de cada módulo



\### proxy



Proporciona la infraestructura de proxy de Apache.



En un proxy inverso, Apache recibe las peticiones del cliente y las dirige a un backend definido en la configuración.



Para TaskFlow, permitiría situar Apache delante del servidor que ejecuta FastAPI.



Fragmento de ejemplo para un VirtualHost:



```apache

ProxyRequests Off

ProxyPass "/" "http://127.0.0.1:8000/"

ProxyPassReverse "/" "http://127.0.0.1:8000/"

```



`ProxyRequests Off` mantiene desactivado el proxy directo. No desactiva el proxy inverso configurado mediante `ProxyPass`.



`ProxyPassReverse` adapta determinadas cabeceras de redirección devueltas por el backend.



\### proxy\_http



Añade a `mod\_proxy` el soporte para comunicarse con backends mediante HTTP.



Depende de `mod\_proxy` y no dispone de directivas propias. Se utiliza a través de la configuración del proxy.



Ejemplo para enviar únicamente las peticiones de `/api/` a un backend:



```apache

ProxyRequests Off

ProxyPass "/api/" "http://127.0.0.1:8000/"

ProxyPassReverse "/api/" "http://127.0.0.1:8000/"

```



Con este mapeo, una petición a `/api/tasks` se enviaría al backend como `/tasks`.



La configuración presupone que el backend escucha en el puerto 8000 de la misma máquina Ubuntu. No se ha configurado ni comprobado este proxy en esta práctica.



\### ssl



Proporciona soporte TLS para servir contenido mediante HTTPS utilizando OpenSSL.



TLS permite cifrar la comunicación y, con certificados correctamente verificados, autenticar el servidor.



Ejemplo ilustrativo:



```apache

<VirtualHost \*:443>

&#x20;   ServerName taskflow.example.com

&#x20;   DocumentRoot /var/www/html



&#x20;   SSLEngine on

&#x20;   SSLCertificateFile /etc/ssl/certs/taskflow.crt

&#x20;   SSLCertificateKeyFile /etc/ssl/private/taskflow.key

</VirtualHost>

```



Este ejemplo requiere un certificado y una clave reales, configuración de escucha en el puerto 443 y acceso de red a ese puerto.



Las rutas y el dominio son ejemplos. No deben activarse tal cual si esos archivos no existen.



Activar `ssl` no significa que HTTPS ya esté configurado.



\### rewrite



Permite reescribir URLs y realizar redirecciones mediante reglas y condiciones.



Puede utilizarse para migrar rutas, mantener enlaces antiguos o aplicar reglas de navegación.



Ejemplo dentro de un VirtualHost:



```apache

RewriteEngine On

RewriteRule "^/antigua/?$" "/nueva" \[R=302,L]

```



Las peticiones a `/antigua` o `/antigua/` reciben una redirección temporal hacia `/nueva`.



`R=302` define la redirección temporal y `L` detiene el procesamiento de las reglas de ese conjunto.



Este ejemplo está pensado para el contexto de un VirtualHost. Los patrones en `.htaccess` tienen diferencias de funcionamiento.



\### headers



Permite añadir, modificar o eliminar cabeceras HTTP de peticiones y respuestas.



Es útil para incorporar información de diagnóstico y determinadas cabeceras de seguridad.



Ejemplo dentro de un VirtualHost:



```apache

Header always set X-Practica "2.1"

Header always set X-Content-Type-Options "nosniff"

```



La primera cabecera identifica la práctica.



La segunda indica al navegador que respete el tipo de contenido declarado, evitando ciertos comportamientos de detección automática.



`Header` actúa sobre cabeceras de respuesta. Para modificar cabeceras de petición se utiliza `RequestHeader`.



\## 6. Alcance de los ejemplos



Los fragmentos anteriores son ejemplos documentales, no configuraciones que se hayan aplicado durante esta práctica.



El trabajo realizado consiste en:



\- Activar los cinco módulos.

\- Configurar el ServerName global del entorno local.

\- Comprobar la sintaxis.

\- Reiniciar Apache.

\- Verificar los módulos cargados.

\- Guardar las evidencias.



No se afirma haber desplegado un proxy inverso, configurado HTTPS ni probado las reglas de reescritura o cabeceras de ejemplo.



\## 7. Otros módulos relevantes



| Módulo | Utilidad |

| --- | --- |

| `alias` | Asociar rutas URL con directorios y realizar redirecciones sencillas. |

| `dir` | Gestionar índices de directorio, como `index.html`. |

| `mime` | Asociar extensiones con tipos de contenido. |

| `deflate` | Comprimir respuestas para reducir su tamaño. |

| `status` | Consultar información de actividad del servidor; su acceso debe restringirse. |

| `http2` | Añadir soporte para HTTP/2 cuando la configuración lo permite. |



Se mencionan como ampliación conceptual. Esta práctica no solicita activarlos.



\## 8. Evidencias



Se guardaron las salidas de los comandos en archivos de texto:



```bash

mkdir -p \~/practica-2.1-apache/evidencias

```



```bash

sudo apache2ctl -M 2>\&1 | tee \~/practica-2.1-apache/evidencias/modulos-activos.txt

```



```bash

sudo apache2ctl configtest 2>\&1 | tee \~/practica-2.1-apache/evidencias/configtest.txt

```



```bash

sudo systemctl status apache2 --no-pager -l 2>\&1 | tee \~/practica-2.1-apache/evidencias/estado-apache.txt

```



`tee` muestra la salida y la guarda. `2>\&1` incluye también los mensajes de error y advertencia.



Los archivos se copiaron al repositorio de Windows mediante SCP.



\### Archivos de evidencia



\- \[Lista completa de módulos](../evidencias/modulos-activos.txt)

\- \[Comprobación de sintaxis](../evidencias/configtest.txt)

\- \[Estado de Apache](../evidencias/estado-apache.txt)



Las capturas del proceso se incorporan al documento de entrega.



\## 9. Criterios de comprobación



| Criterio | Evidencia |

| --- | --- |

| Los cinco módulos están activos | Lista completa y captura de la verificación filtrada. |

| La configuración es válida | `Syntax OK` en `configtest.txt`. |

| Apache funciona después del reinicio | Estado `active (running)`. |

| Se ha corregido AH00558 | Comprobación posterior a configurar ServerName. |

| Se explica cada módulo | Apartado de propósito y ejemplos. |



Si los registros incluyen mensajes antiguos, deben distinguirse de los correspondientes al último reinicio.



\## 10. Referencias oficiales



\- \[mod\_proxy](https://httpd.apache.org/docs/2.4/mod/mod\_proxy.html)

\- \[mod\_proxy\_http](https://httpd.apache.org/docs/2.4/mod/mod\_proxy\_http.html)

\- \[mod\_ssl](https://httpd.apache.org/docs/2.4/mod/mod\_ssl.html)

\- \[mod\_rewrite](https://httpd.apache.org/docs/2.4/mod/mod\_rewrite.html)

\- \[mod\_headers](https://httpd.apache.org/docs/2.4/mod/mod\_headers.html)

\- \[Directiva ServerName](https://httpd.apache.org/docs/2.4/mod/core.html#servername)

