import ssl
from typing import Dict, Any

# Esta es una dependencia externa que el usuario deberá instalar.
# Se puede instalar con: pip install routeros_api
import routeros_api

class MikroTikAPIClient:
    """
    Cliente para interactuar con la API de un router MikroTik.
    """

    def __init__(self, host: str, user: str, password: str, port: int = 8729, use_ssl: bool = True, verify_ssl: bool = True, ca_cert: str = None):
        """
        Inicializa el cliente de la API.

        Args:
            host (str): La dirección IP o el nombre de host del router.
            user (str): El nombre de usuario para la autenticación.
            password (str): La contraseña para la autenticación.
            port (int): El puerto de la API (por defecto es 8729 para SSL).
            use_ssl (bool): Si se debe usar una conexión SSL.
            verify_ssl (bool): Si se debe verificar el certificado SSL.
            ca_cert (str): Ruta al archivo de certificado de la CA.
        """
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.use_ssl = use_ssl
        self.verify_ssl = verify_ssl
        self.ca_cert = ca_cert
        self.connection = None

    def _connect(self) -> None:
        """
        Establece la conexión con el router.
        """
        if self.connection:
            return

        try:
            # Configuración SSL para conexiones seguras
            if self.use_ssl:
                ssl_context = ssl.create_default_context()
                if not self.verify_ssl:
                    ssl_context.check_hostname = False
                    ssl_context.verify_mode = ssl.CERT_NONE
                elif self.ca_cert:
                    ssl_context.load_verify_locations(self.ca_cert)

                self.connection = routeros_api.RouterOsApiPool(
                    self.host,
                    username=self.user,
                    password=self.password,
                    port=self.port,
                    use_ssl=True,
                    ssl_context=ssl_context,
                    plaintext_login=True
                ).get_api()
            else:
                self.connection = routeros_api.RouterOsApiPool(
                    self.host,
                    username=self.user,
                    password=self.password,
                    port=self.port,
                    plaintext_login=True
                ).get_api()

            print(f"Conectado exitosamente a {self.host}")

        except routeros_api.exceptions.RouterOsApiConnectionError as e:
            print(f"Error de conexión con MikroTik: {e}")
            raise ConnectionError(f"No se pudo conectar a {self.host}")

    def add_ip_to_address_list(self, ip_address: str, list_name: str = "vpn_authorized_ips") -> bool:
        """
        Agrega una dirección IP a una lista de direcciones en el firewall de MikroTik.

        Args:
            ip_address (str): La dirección IP a agregar.
            list_name (str): El nombre de la lista de direcciones.

        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        self._connect()

        if not self.connection:
            return False

        try:
            # Obtener el recurso de la lista de direcciones del firewall
            address_list_resource = self.connection.get_resource('/ip/firewall/address-list')

            # Agregar la nueva entrada
            address_list_resource.add(
                list=list_name,
                address=ip_address,
                comment=f"Agregado automáticamente por VPNConnect"
            )

            print(f"IP {ip_address} agregada a la lista '{list_name}' exitosamente.")
            return True

        except Exception as e:
            print(f"Error al agregar la IP a la lista de direcciones: {e}")
            return False

    def close(self) -> None:
        """
        Cierra la conexión con el router.
        """
        if self.connection:
            self.connection.disconnect()
            print("Conexión con MikroTik cerrada.")
