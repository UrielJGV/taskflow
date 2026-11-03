Práctica 1.1 — Preparar el servidor base

1. Objetivo
Preparar un servidor Ubuntu Server 22.04 LTS virtualizado mediante VirtualBox y configurar el acceso remoto mediante SSH.
2. Especificaciones del servidor
Característica	Configuración
Sistema operativo	Ubuntu Server 22.04 LTS
Virtualizador	VirtualBox
Memoria RAM	\[RAM REAL]
CPU	\[NÚMERO REAL DE CPU]
Almacenamiento	\[TAMAÑO REAL DEL DISCO]
Dirección IP	\[IP REAL DEL SERVIDOR]
Nombre del servidor	\[NOMBRE REAL]
3. Instalación de la máquina virtual
Se ha creado una máquina virtual en VirtualBox con Ubuntu Server 22.04 LTS.

La máquina virtual arranca correctamente y permite iniciar sesión en el sistema.

4. Actualización del sistema
Se ha actualizado el sistema mediante el siguiente comando:

sudo apt update \&\& sudo apt upgrade -y
La actualización se ha realizado correctamente.

5. Usuario de trabajo
Se ha creado/configurado un usuario de trabajo con permisos sudo.

Se ha comprobado el funcionamiento de los permisos administrativos mediante:

sudo whoami
El resultado obtenido ha sido root.

6. Configuración de red
La máquina virtual utiliza una red NAT con redirección de puertos para permitir el acceso SSH desde el equipo host.

Puerto SSH del servidor: 22
Puerto del host: 2222
Dirección del host: 127.0.0.1
7. Acceso remoto por SSH
Se ha instalado y configurado el servicio OpenSSH Server.

El acceso remoto se ha probado desde Windows mediante PowerShell:

ssh -p 2222 \[USUARIO]@127.0.0.1
La conexión se ha realizado correctamente.

8. Snapshot
Se ha creado una instantánea de la máquina virtual para poder recuperar el estado guardado.

Nombre de la instantánea:

Estado inicial Ubuntu Server

9. Almacenamiento y recursos
Memoria RAM: \[DATO REAL]
CPU: \[DATO REAL]
Disco virtual: \[DATO REAL]
Tipo de red: NAT
Redirección de puertos: TCP 2222 → 22
10. Problemas y soluciones
\[Escribir los problemas encontrados durante la práctica y las soluciones aplicadas.]
11. Conclusión
Se ha preparado un servidor Ubuntu Server 22.04 LTS virtualizado, actualizado y accesible mediante SSH desde el equipo host.

La configuración y las pruebas se han documentado en este README.md.

\## Evidencias de la práctica



\[Ver el documento con las capturas](evidencias-servidor-base.pdf).



\[Volver al índice principal](../../../README.md).

