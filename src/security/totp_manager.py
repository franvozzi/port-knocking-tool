import pyotp
import time

class TOTPManager:
    """
    Gestiona la lógica de generación y verificación de TOTP.
    """

    def __init__(self, secret: str = None):
        """
        Inicializa el gestor con un secreto o genera uno nuevo.

        Args:
            secret (str, optional): El secreto TOTP en base32. Si no se provee, se genera uno nuevo.
        """
        if secret:
            self.secret = secret
        else:
            self.secret = pyotp.random_base32()

        self.totp = pyotp.TOTP(self.secret)

    def get_secret(self) -> str:
        """
        Retorna el secreto TOTP en formato base32.
        """
        return self.secret

    def get_provisioning_uri(self, user: str, issuer: str = "VPN Corporativa") -> str:
        """
        Genera una URI de aprovisionamiento para la configuración de la app de autenticación.

        Args:
            user (str): El nombre de usuario a mostrar en la app de autenticación.
            issuer (str, optional): El nombre del emisor.

        Returns:
            str: La URI de aprovisionamiento.
        """
        return self.totp.provisioning_uri(name=user, issuer_name=issuer)

    def verify(self, code: str) -> bool:
        """
        Verifica un código TOTP.

        Args:
            code (str): El código de 6 dígitos a verificar.

        Returns:
            bool: True si el código es válido, False en caso contrario.
        """
        return self.totp.verify(code)

# Ejemplo de uso (para pruebas)
if __name__ == "__main__":
    manager = TOTPManager()

    secret_key = manager.get_secret()
    print(f"Secreto generado: {secret_key}")

    uri = manager.get_provisioning_uri("usuario@empresa.com", issuer="MiEmpresa VPN")
    print(f"Provisioning URI (para QR code): {uri}")

    # Simulación de verificación
    print("\n--- Simulación de Verificación ---")

    # Generar un código actual
    current_code = manager.totp.now()
    print(f"Código TOTP actual: {current_code}")

    # Verificar el código correcto
    is_valid = manager.verify(current_code)
    print(f"Verificando '{current_code}': {'Válido' if is_valid else 'Inválido'}")

    # Verificar un código incorrecto
    invalid_code = "123456"
    is_valid = manager.verify(invalid_code)
    print(f"Verificando '{invalid_code}': {'Válido' if is_valid else 'Inválido'}")

    print("\nEsperando 30 segundos para el siguiente código...")
    time.sleep(30)

    new_code = manager.totp.now()
    print(f"Nuevo código TOTP: {new_code}")

    # Verificar el código anterior (debería fallar)
    is_valid_old = manager.verify(current_code)
    print(f"Verificando código antiguo '{current_code}': {'Válido' if is_valid_old else 'Inválido'}")

    # Verificar el nuevo código
    is_valid_new = manager.verify(new_code)
    print(f"Verificando código nuevo '{new_code}': {'Válido' if is_valid_new else 'Inválido'}")
