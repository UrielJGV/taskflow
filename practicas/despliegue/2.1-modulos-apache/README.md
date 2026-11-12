\# Práctica 2.1 — Módulos de Apache



\## Objetivo



Preparar Apache en Ubuntu Server activando los módulos necesarios para el proyecto y comprobar que el servicio reinicia correctamente.



\## Módulos activados



| Módulo | Función |

| --- | --- |

| `proxy` | Infraestructura de proxy y proxy inverso. |

| `proxy\_http` | Comunicación HTTP con el backend. |

| `ssl` | Soporte TLS para configurar HTTPS. |

| `rewrite` | Reescritura de URLs y redirecciones. |

| `headers` | Gestión de cabeceras HTTP. |



\## Trabajo realizado



1\. Consulta de la versión, el estado y los módulos iniciales.

2\. Activación de los cinco módulos.

3\. Corrección del aviso AH00558 mediante un ServerName global para el entorno local.

4\. Comprobación de sintaxis y reinicio de Apache.

5\. Verificación filtrada de los módulos.

6\. Exportación de evidencias y documentación.



La administración se realizó mediante SSH desde Windows hacia Ubuntu Server en VirtualBox.



\## Documentación



\[Explicación completa y ejemplos de configuración](docs/modulos-apache.md)



El documento incluye el propósito de cada módulo, ejemplos ilustrativos, la resolución del aviso y referencias oficiales.



\## Evidencias



\- \[Lista completa de módulos activos](evidencias/modulos-activos.txt)

\- \[Comprobación de sintaxis](evidencias/configtest.txt)

\- \[Estado del servicio Apache](evidencias/estado-apache.txt)



La comprobación de sintaxis devuelve `Syntax OK` y el servicio aparece como `active (running)` después del reinicio.



Las capturas del proceso se recogen en el documento de entrega.



\## Alcance



Se han activado y verificado los módulos.



Los ejemplos de proxy inverso, HTTPS, reescritura y cabeceras incluidos en la documentación son explicativos: no se han aplicado como parte de esta práctica.



Activar un módulo prepara su funcionalidad, pero no sustituye la configuración del servicio que lo utilizará.

