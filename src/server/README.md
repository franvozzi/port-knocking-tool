
# Servidor de Verificación TOTP

Este servidor es un componente simple de Flask diseñado para verificar códigos TOTP (Time-based One-Time Password) y, si son válidos, agregar la dirección IP del cliente a una lista de direcciones en un router MikroTik.

## Requisitos

- Python 3.9+
- Flask
- pyotp
- routeros-api

Puedes instalar las dependencias con:

```bash
pip install Flask pyotp routeros-api
```

## Configuración

El servidor se configura a través de variables de entorno. A continuación se muestran las variables disponibles y sus valores predeterminados:

| Variable        | Descripción                                      | Valor Predeterminado        |
|-----------------|--------------------------------------------------|-----------------------------|
| `MIKROTIK_IP`   | La dirección IP de tu router MikroTik.            | `192.168.88.1`              |
| `MIKROTIK_USER` | El nombre de usuario para la API de MikroTik.      | `api-user`                  |
| `MIKROTIK_PASS` | La contraseña para la API de MikroTik.             | `api-password`              |
| `TOTP_SECRET`   | El secreto compartido para la generación de TOTP.  | (Se genera uno aleatorio)   |

## Ejecución

Para iniciar el servidor, ejecuta el siguiente comando:

```bash
python src/server/main.py
```

Al iniciar, el servidor imprimirá el secreto TOTP que está utilizando y una URI de aprovisionamiento. Puedes usar esta URI para generar un código QR y agregarlo a tu aplicación de autenticación (como Google Authenticator o Authy).

## Endpoint

El servidor expone un único endpoint:

### `POST /verify_totp`

Este endpoint acepta una solicitud JSON con el siguiente formato:

```json
{
  "totp_code": "123456"
}
```

Si el código TOTP es válido, el servidor agregará la dirección IP del cliente a la lista de direcciones `vpn_authorized_ips` en el router MikroTik.
