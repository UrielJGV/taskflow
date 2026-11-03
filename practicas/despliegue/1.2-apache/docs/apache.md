# Práctica 1.2 - Instalación básica de Apache

## 1. Objetivo

El objetivo de esta práctica es instalar y verificar el funcionamiento del servidor web Apache en Ubuntu.

## 2. Instalación de Apache

Primero actualicé los paquetes del sistema mediante:

```bash
sudo apt update
```

Después instalé Apache con:

```bash
sudo apt install apache2 -y
```

La opción `-y` permite aceptar automáticamente la instalación.

## 3. Comprobación de la instalación

Para comprobar que Apache se había instalado correctamente ejecuté:

```bash
apache2 -v
```

El comando mostró la versión instalada de Apache.

## 4. Comprobación del servicio

Comprobé que el servicio Apache estaba funcionando mediante:

```bash
sudo systemctl status apache2
```

El resultado mostró:

```text
Active: active (running)
```

Esto indica que el servidor Apache está funcionando correctamente.

## 5. Habilitar Apache al iniciar el sistema

Para conseguir que Apache se inicie automáticamente al arrancar Ubuntu utilicé:

```bash
sudo systemctl enable apache2
```

Después comprobé que estaba habilitado:

```bash
systemctl is-enabled apache2
```

El resultado fue:

```text
enabled
```

## 6. Comprobación desde el navegador

Para comprobar que Apache funcionaba correctamente abrí un navegador y accedí a:

```text
http://IP-DE-LA-MÁQUINA
```

La página de bienvenida de Apache apareció correctamente.

También comprobé el acceso desde el navegador del equipo host utilizando la dirección IP de la máquina virtual.

## 7. Puerto 80

Apache utiliza normalmente el puerto 80 para las conexiones HTTP.

Comprobé que Apache estaba escuchando en el puerto 80 mediante:

```bash
sudo ss -tulpn | grep :80
```

El resultado confirmó que Apache estaba escuchando en dicho puerto.

## 8. Conclusión

Apache quedó instalado y funcionando correctamente. El servicio está activo y habilitado para iniciarse automáticamente. Además, se pudo acceder a la página de Apache desde el navegador del equipo host mediante la dirección IP de la máquina virtual.
