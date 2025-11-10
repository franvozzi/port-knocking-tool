
# Guía de Pruebas de Principio a Fin (E2E)

**Versión:** 1.0
**Fecha:** Noviembre 2023
**Audiencia:** Administradores y Desarrolladores

---

## Introducción

Esta guía describe los pasos necesarios para configurar un entorno de pruebas completo y validar la funcionalidad del sistema de conexión VPN con 2FA y Port Knocking.

Para realizar una prueba exitosa, es necesario configurar y ejecutar los tres componentes del sistema en el orden correcto:

1.  **Router MikroTik:** El firewall que controla el acceso.
2.  **Servidor de Verificación TOTP:** El servicio que valida los códigos 2FA.
3.  **Cliente VPN (`VPNConnect`):** La aplicación de escritorio del usuario.

## Paso 1: Configurar el Router MikroTik

La correcta configuración del router es la base de todo el sistema.

- **Objetivo:** Preparar el firewall para que acepte conexiones de la API, gestione una lista de IPs autorizadas y ejecute la secuencia de port knocking.
- **Instrucciones:** Sigue al pie de la letra el **Paso 1** del `docs/Manual_Administrador_2FA.md`.

### Checklist de Verificación del Router:

- [ ] El servicio `api-ssl` está habilitado y funcionando en el puerto `8729` (o el que hayas configurado).
- [ ] Existe un usuario con permisos de `api` y `write`.
- [ ] Existe una lista de direcciones vacía llamada `vpn_authorized_ips` en `IP > Firewall > Address Lists`.
- [ ] Existen las reglas de firewall para el `port knocking`, incluyendo la regla `jump` que depende de `vpn_authorized_ips`.
- [ ] La regla final que permite el acceso a la VPN (puerto `1194`) está configurada y depende de la lista de direcciones del último paso del "knocking".

## Paso 2: Poner en Marcha el Servidor de Verificación

El servidor actúa como intermediario entre el cliente y el router.

- **Objetivo:** Ejecutar el servidor Flask para que escuche las peticiones de verificación del cliente.
- **Instrucciones:** Sigue las indicaciones de `src/server/README.md` o del **Paso 2** del manual de administrador.

### Pasos Detallados para la Ejecución:

1.  **Abre una terminal** en la raíz del proyecto.

2.  **Establece las Variables de Entorno:**
    - Reemplaza los valores de ejemplo con tus credenciales reales del router.

    ```bash
    # IP de la API SSL de tu MikroTik
    export MIKROTIK_IP="192.168.88.1"

    # Usuario y contraseña creados para la API
    export MIKROTIK_USER="api-user"
    export MIKROTIK_PASS="tu-contraseña-segura"

    # Secreto para los códigos TOTP. Puedes generar uno nuevo si lo necesitas.
    # Si lo cambias, tendrás que volver a escanear el QR en la app de autenticación.
    export TOTP_SECRET="TU_SECRETO_TOTP_AQUI"
    ```

3.  **Inicia el Servidor:**
    ```bash
    python src/server/main.py
    ```

4.  **Verifica que está en funcionamiento:**
    - La terminal debería mostrar un mensaje indicando que el servidor está escuchando en `http://0.0.0.0:5000`.
    - También te mostrará la **URI de aprovisionamiento**. Si aún no has configurado tu app de autenticación (como Google Authenticator), usa esta URI para generar un código QR y escanearlo.

## Paso 3: Configurar y Probar el Cliente

Con el router y el servidor listos, ya puedes probar el cliente.

- **Objetivo:** Simular la acción de un usuario final que se conecta a la VPN.
- **Instrucciones:** Sigue el **Paso 3** del manual de administrador.

### Pasos Detallados para la Prueba:

1.  **Verifica la Configuración del Cliente:**
    - Abre el archivo `src/config.json`.
    - Asegúrate de que la `totp_verification_url` apunte a la IP de la máquina donde estás ejecutando el servidor. Si estás probando todo en la misma máquina, puedes usar `http://127.0.0.1:5000/verify_totp`.

2.  **Abre una nueva terminal** en la raíz del proyecto.

3.  **Inicia el Cliente:**
    ```bash
    python src/main.py
    ```
    - Se abrirá la ventana de la aplicación `VPNConnect`.

4.  **Realiza la Prueba de Conexión:**
    - Abre tu aplicación de autenticación en el teléfono (ej. Google Authenticator).
    - Introduce el código de 6 dígitos que se muestra en la casilla "Código 2FA".
    - Haz clic en **"Conectar"**.

## Resultados Esperados

Si todo está configurado correctamente, deberías observar el siguiente flujo:

1.  **En la terminal del servidor:** Verás una petición `POST` al endpoint `/verify_totp` y un mensaje indicando que la IP ha sido autorizada.
2.  **En el Router MikroTik:** Si vas a `IP > Firewall > Address Lists`, verás que tu IP pública aparece ahora en la lista `vpn_authorized_ips`.
3.  **En el Cliente:** La barra de progreso avanzará, indicando que la verificación 2FA fue exitosa, que el port knocking se completó y que la conexión VPN se está estableciendo.

Si alguno de estos pasos falla, consulta la sección de **"Solución de Problemas"** en el `docs/Manual_Administrador_2FA.md`.
