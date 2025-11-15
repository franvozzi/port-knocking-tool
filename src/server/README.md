
# Servidor de Verificación TOTP (retirado)

La funcionalidad del servidor de verificación TOTP fue retirada del MVP.
Este directorio y sus archivos quedan como referencia histórica. Para el
MVP actual la aplicación realiza únicamente Port Knocking seguido de la
conexión VPN, sin pasos de 2FA/TOTP.

Si deseas restaurar el servidor 2FA en el futuro, revisa los commits
anteriores o reimplementa un servicio independiente con las dependencias
necesarias (Flask, pyotp, routeros-api) y documenta las variables de
entorno requeridas.
