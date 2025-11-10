
import os
from flask import Flask, request, jsonify
from src.security.totp_manager import TOTPManager
from src.network.mikrotik_api_client import MikroTikAPIClient

app = Flask(__name__)

# --- Configuración ---
# En un entorno de producción, estos valores deberían cargarse desde un
# archivo de configuración seguro o variables de entorno.
MIKROTIK_IP = os.environ.get("MIKROTIK_IP")
MIKROTIK_USER = os.environ.get("MIKROTIK_USER")
MIKROTIK_PASS = os.environ.get("MIKROTIK_PASS")
TOTP_SECRET = os.environ.get("TOTP_SECRET")

if not all([MIKROTIK_IP, MIKROTIK_USER, MIKROTIK_PASS, TOTP_SECRET]):
    raise ValueError("Missing one or more required environment variables: MIKROTIK_IP, MIKROTIK_USER, MIKROTIK_PASS, TOTP_SECRET")

# --- Inicialización de Clientes ---
totp_manager = TOTPManager(secret=TOTP_SECRET)
mikrotik_client = MikroTikAPIClient(
    host=MIKROTIK_IP,
    user=MIKROTIK_USER,
    password=MIKROTIK_PASS,
    use_ssl=True,
    verify_ssl=True,
    ca_cert=os.environ.get("MIKROTIK_CA_CERT")
)

@app.route('/verify_totp', methods=['POST'])
def verify_totp():
    """
    Endpoint para verificar un código TOTP y autorizar una IP.
    """
    data = request.get_json()
    if not data or 'totp_code' not in data:
        return jsonify({"status": "error", "message": "Falta el código TOTP."}), 400

    totp_code = data['totp_code']
    user_ip = request.remote_addr

    # 1. Verificar el código TOTP
    if not totp_manager.verify(totp_code):
        return jsonify({"status": "error", "message": "Código TOTP inválido o expirado."}), 401

    # 2. Agregar la IP del cliente a la lista de direcciones de MikroTik
    try:
        success = mikrotik_client.add_ip_to_address_list(user_ip, "vpn_authorized_ips")
        if not success:
            raise Exception("No se pudo agregar la IP a la lista de direcciones.")
    except Exception as e:
        # Aquí deberíamos tener un logging más robusto
        print(f"Error al interactuar con MikroTik: {e}")
        return jsonify({"status": "error", "message": "Error interno del servidor al autorizar la IP."}), 500

    return jsonify({"status": "success", "message": f"IP {user_ip} autorizada exitosamente."})

if __name__ == '__main__':
    print("--- Servidor de Verificación TOTP ---")
    print(f"Usando secreto TOTP: {TOTP_SECRET}")
    print("Para probar, genera un código QR con la siguiente URI:")
    print(totp_manager.get_provisioning_uri("usuario@empresa.com", issuer="MiEmpresa VPN"))
    print("\nEndpoint disponible en: http://127.0.0.1:5000/verify_totp")

    app.run(host='0.0.0.0', port=5000)
