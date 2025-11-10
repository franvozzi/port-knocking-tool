
# Arquitectura del Proyecto

Este documento describe los componentes principales del sistema y cómo interactúan entre sí.

## Componentes Principales

El sistema se compone de tres partes fundamentales:

1.  **Cliente de Escritorio (`VPNConnect`)**:
    - Es una aplicación Python con una interfaz gráfica desarrollada en `tkinter`.
    - Su función es guiar al usuario a través del proceso de conexión segura.
    - Se encarga de:
        - Recoger el código TOTP del usuario.
        - Comunicarse con el **Servidor de Verificación** para validar el código.
        - Ejecutar la secuencia de **port knocking** contra el router.
        - Establecer la conexión final a través de OpenVPN.
    - Es un cliente compilado (ej. `.exe` o `.app`) que se distribuye a los usuarios finales.

2.  **Servidor de Verificación TOTP**:
    - Es una aplicación web ligera construida con `Flask`.
    - Actúa como el "guardián" del sistema de seguridad.
    - Sus responsabilidades son:
        - Exponer un endpoint (`/verify_totp`) para recibir los códigos TOTP.
        - Validar que el código recibido sea correcto y no haya expirado.
        - Si el código es válido, se comunica con el **Router MikroTik** a través de su API para agregar la IP del cliente a una lista de direcciones autorizadas (`vpn_authorized_ips`).
    - Este servidor debe estar desplegado en un lugar accesible para los clientes, pero no necesariamente expuesto públicamente a todo internet.

3.  **Router MikroTik (Firewall)**:
    - Es el componente de hardware que controla el acceso a la red.
    - Está configurado para:
        - Solo aceptar intentos de "port knocking" de IPs que se encuentren en la lista `vpn_authorized_ips`.
        - Gestionar la secuencia de "port knocking" para abrir el puerto de la VPN solo a aquellos que completen la secuencia correctamente.
        - Permitir la conexión final a la VPN.

## Flujo de Datos

A continuación se describe el flujo de comunicación durante un intento de conexión exitoso:

1.  **Usuario -> Cliente**: El usuario introduce su código TOTP en la aplicación `VPNConnect`.
2.  **Cliente -> Servidor**: El cliente envía una petición `POST` al endpoint `/verify_totp` del servidor, incluyendo el código TOTP.
3.  **Servidor -> Router**: El servidor valida el código. Si es correcto, establece una conexión a la API del router MikroTik y añade la IP del cliente a la lista `vpn_authorized_ips`.
4.  **Servidor -> Cliente**: El servidor responde al cliente con un mensaje de éxito.
5.  **Cliente -> Router**: El cliente ejecuta la secuencia de "port knocking" (ej. golpes a los puertos 7000 y 8000).
6.  **Router**: El router, al detectar la secuencia de golpes desde una IP autorizada, abre el puerto de la VPN (ej. 1194) para esa IP.
7.  **Cliente -> Router**: El cliente inicia la conexión OpenVPN al puerto recién abierto.

Este diseño asegura que cada paso del proceso de autenticación y autorización esté separado y protegido, minimizando la superficie de ataque.
