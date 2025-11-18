# Manual de Administrador: Configuración de 2FA con TOTP y Port Knocking

**Versión:** 1.0
**Fecha:** Noviembre 2023
**Audiencia:** Administradores de Sistemas y TI

## Resumen

Manual detallado para configurar MikroTik, desplegar el servidor de verificación TOTP y preparar el cliente.

## Pasos clave
- Habilitar API SSL en MikroTik y crear usuario `api-user`.
- Crear `vpn_authorized_ips` en `IP > Firewall > Address Lists`.
- Configurar la cadena de port-knocking y reglas que añaden `knock_stage_*`.
- Desplegar servidor Flask con variables de entorno: `MIKROTIK_IP`, `MIKROTIK_USER`, `MIKROTIK_PASS`, `TOTP_SECRET`.

Consulta el archivo completo en el repositorio para detalles de cada comando y ejemplos.
# Manual de Administrador: Configuración de 2FA con TOTP y Port Knocking

**Versión:** 1.0
**Fecha:** Noviembre 2023
**Audiencia:** Administradores de Sistemas y TI

---

## Índice

1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Paso 1: Configuración del Router MikroTik](#paso-1-configuración-del-router-mikrotik)
4. [Paso 2: Configuración y Despliegue del Servidor de Verificación](#paso-2-configuración-y-despliegue-del-servidor-de-verificación)
5. [Paso 3: Configuración del Cliente VPN](#paso-3-configuración-del-cliente-vpn)
6. [Flujo de Conexión](#flujo-de-conexión)
7. [Solución de Problemas](#solución-de-problemas)

---

## Introducción

Este manual detalla los pasos para configurar un sistema de seguridad multicapa para el acceso a la VPN corporativa. El sistema combina tres técnicas:

1.  **Autenticación de Dos Factores (2FA) con TOTP:** El usuario debe proporcionar un código de un solo uso desde una aplicación de autenticación.
2.  **IP Whitelisting Dinámico:** La IP pública del usuario es autorizada temporalmente en el firewall.
3.  **Port Knocking:** La aplicación cliente ejecuta una secuencia de "golpes" a puertos cerrados para abrir el puerto de la VPN.

Este enfoque asegura que solo los usuarios autenticados, desde una IP autorizada y con la secuencia correcta, puedan acceder a la VPN.

## Arquitectura del Sistema

El sistema consta de tres componentes principales:

1.  **Cliente VPN (`VPNConnect.exe`)**: La aplicación de escritorio que el usuario final utiliza.
2.  **Servidor de Verificación TOTP**: Un servicio web simple que valida los códigos 2FA y se comunica con el router.
3.  **Router MikroTik**: El firewall de la red que gestiona las listas de IPs autorizadas y la secuencia de port knocking.


## Paso 1: Configuración del Router MikroTik

La configuración del router es crucial y se divide en tres partes: habilitar la API, crear la lista de direcciones para IPs autorizadas y configurar las reglas de port knocking.

### 1.1 Habilitar la API SSL

El servidor de verificación necesita comunicarse con el router. Es fundamental habilitar la API y protegerla con SSL.

1.  **Crea un Certificado SSL:**
    - Ve a `System > Certificates`.
    - Crea un nuevo certificado. Asígnale un nombre (ej. `api-ssl`) y en `Common Name`, pon la dirección IP del router.
    - Fírmalo (`Sign`) y asegúrate de que sea de confianza (`trusted=yes`).

2.  **Habilita el Servicio de API SSL:**
    - Ve a `IP > Services`.
    - Busca `api-ssl` y habilítalo.
    - Asigna el certificado que acabas de crear en el campo `Certificate`.
    - Anota el puerto (por defecto `8729`).

3.  **Crea un Usuario para la API:**
    - Ve a `System > Users`.
    - Crea un nuevo usuario (ej. `api-user`) y asígnale una contraseña segura.
    - En el grupo (`Group`), dale permisos de `write` y `api`.

### 1.2 Crear la Lista de Direcciones

Esta lista almacenará temporalmente las IPs de los usuarios que han pasado la verificación 2FA.

- Ve a `IP > Firewall > Address Lists`.
- Crea una nueva lista con el nombre `vpn_authorized_ips`.

### 1.3 Configurar las Reglas de Port Knocking

Estas reglas solo procesarán los "golpes" que vengan de una IP autorizada.

1.  **Regla de Salto (Jump Rule):**
    - Ve a `IP > Firewall > Filter Rules`.
    - Crea una regla en la cadena `forward` (o `input`, según tu configuración).
    - En la pestaña `Advanced`, en `Src. Address List`, selecciona `vpn_authorized_ips`.
    - En la pestaña `Action`, elige `jump` y en `Jump Target`, escribe `port-knocking-chain`.

2.  **Cadena de Port Knocking (`port-knocking-chain`):**
    - Esta cadena contendrá la secuencia de "golpes". Por cada puerto en tu secuencia (ej. 7000, 8000), crea una regla:
        - **Regla 1 (Puerto 7000):**
            - `Chain`: `port-knocking-chain`
            - `Protocol`: `tcp`
            - `Dst. Port`: `7000`
            - `Action`: `add src to address list`
            - `Address List`: `knock_stage_1`
            - `Timeout`: `1m`
        - **Regla 2 (Puerto 8000):**
            - `Chain`: `port-knocking-chain`
            - `Protocol`: `tcp`
            - `Dst. Port`: `8000`
            - `Src. Address List`: `knock_stage_1`
            - `Action`: `add src to address list`
            - `Address List`: `knock_final_stage`
            - `Timeout`: `1m`

3.  **Regla de Acceso a la VPN:**
    - Finalmente, crea la regla que permite el acceso al puerto de la VPN (ej. 1194).
    - `Chain`: `forward` (o `input`)
    - `Protocol`: `udp` (o `tcp`, según tu VPN)
    - `Dst. Port`: `1194`
    - `Src. Address List`: `knock_final_stage`
    - `Action`: `accept`

## Paso 2: Configuración y Despliegue del Servidor de Verificación

El servidor es una aplicación Flask que se puede ejecutar en un contenedor Docker o directamente en un servidor Linux.

### 2.1 Configuración con Variables de Entorno

El servidor se configura exclusivamente con variables de entorno.

| Variable             | Descripción                                                | Ejemplo                               |
|----------------------|------------------------------------------------------------|---------------------------------------|
| `MIKROTIK_IP`        | La dirección IP de la API del router MikroTik.             | `192.168.88.1`                        |
| `MIKROTIK_USER`      | El usuario creado para la API.                             | `api-user`                            |
| `MIKROTIK_PASS`      | La contraseña del usuario de la API.                       | `una-contraseña-muy-segura`           |
| `TOTP_SECRET`        | El secreto compartido para generar los códigos TOTP.       | (Genera uno con `pyotp.random_base32()`) |
| `MIKROTIK_CA_CERT`   | (Opcional) Ruta al certificado CA para verificar el SSL.   | `/certs/ca.crt`                       |

### 2.2 Despliegue

1.  **Instala las Dependencias:**
    ```bash
    pip install Flask pyotp routeros-api
    ```
2.  **Inicia el Servidor:**
    ```bash
    export MIKROTIK_IP="192.168.88.1"
    export MIKROTIK_USER="api-user"
    export MIKROTIK_PASS="tu-contraseña"
    export TOTP_SECRET="SECRETO_GENERADO_AQUI"

    python src/server/main.py
    ```

Al iniciar, el servidor te proporcionará una **URI de aprovisionamiento**. Guárdala, la necesitarás para que los usuarios configuren sus aplicaciones de autenticación.

## Paso 3: Configuración del Cliente VPN

La configuración del cliente (`VPNConnect`) se realiza a través del archivo `src/config.json` antes de compilar el ejecutable.

### 3.1 El Archivo `config.json`

Asegúrate de que el archivo `src/config.json` esté configurado correctamente.

```json
{
  "target_ip": "203.0.113.10",  // IP pública del router
  "knock_sequence": [
    [7000, "tcp"],
    [8000, "tcp"]
  ],
  "interval": 0.5,
  "target_port": 1194,
  "totp_verification_url": "http://<IP_DEL_SERVIDOR_TOTP>:5000/verify_totp"
}
```

- **`target_ip`**: La IP pública de tu red, a la que se conectará el cliente.
- **`knock_sequence`**: Debe coincidir con las reglas configuradas en el MikroTik.
- **`totp_verification_url`**: La URL donde está desplegado el servidor de verificación.

### 3.2 Compilación del Ejecutable

Una vez configurado, compila el cliente siguiendo las instrucciones del `README.md` principal para generar el `.exe` (Windows), `.app` (macOS) o el binario de Linux.

## Flujo de Conexión

1.  El usuario abre el cliente `VPNConnect`.
2.  Introduce el código de 6 dígitos de su app de autenticación.
3.  El cliente envía el código al **Servidor de Verificación**.
4.  El servidor valida el código. Si es correcto, usa la API de MikroTik para agregar la IP pública del usuario a la lista `vpn_authorized_ips`.
5.  El cliente, al recibir la confirmación, ejecuta la secuencia de **Port Knocking**.
6.  El router MikroTik detecta los "golpes" desde una IP autorizada y abre el puerto de la VPN.
7.  El cliente establece la conexión VPN.

## Solución de Problemas

- **Error: "Código TOTP inválido"**:
    - Asegúrate de que la hora del servidor y del teléfono del usuario estén sincronizadas.
    - Confirma que el `TOTP_SECRET` en el servidor es el mismo con el que se generó el QR.

- **Error: "No se pudo autorizar la IP"**:
    - Revisa la conectividad entre el servidor de verificación y el router MikroTik.
    - Verifica que el usuario y la contraseña de la API sean correctos.
    - Asegúrate de que el firewall del router permite conexiones a la API desde la IP del servidor.

- **La Conexión VPN Falla Después del Port Knocking**:
    - Confirma que las reglas de port knocking y la secuencia en `config.json` son idénticas.
    - Revisa que el timeout de las listas de direcciones en el MikroTik sea suficiente.

