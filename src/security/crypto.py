import base64
from cryptography.fernet import Fernet
from pathlib import Path
from typing import Tuple

from utils.exceptions import AuthenticationError

class CredentialsEncryptor:
    """Gestor de cifrado de credenciales"""
    
    def __init__(self, key_file: str = ".key"):
        self.key_file = Path(key_file)
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)
    
    def _load_or_generate_key(self) -> bytes:
        """Carga o genera clave de cifrado"""
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            # Ocultar archivo en Unix
            if self.key_file.exists():
                import os
                if os.name != 'nt':  # No Windows
                    os.chmod(self.key_file, 0o600)
            return key
    
    def encrypt_credentials(self, username: str, password: str) -> bytes:
        """Cifra credenciales"""
        data = f"{username}\n{password}".encode('utf-8')
        return self.cipher.encrypt(data)
    
    def decrypt_credentials(self, encrypted_data: bytes) -> Tuple[str, str]:
        """Descifra credenciales"""
        try:
            decrypted = self.cipher.decrypt(encrypted_data)
            lines = decrypted.decode('utf-8').split('\n')
            if len(lines) != 2:
                raise AuthenticationError("Formato de credenciales inválido")
            return lines[0], lines[1]
        except Exception as e:
            raise AuthenticationError(f"Error descifrando credenciales: {e}")
    
    def save_encrypted_credentials(self, username: str, password: str, 
                                   output_file: str = "credentials.enc"):
        """Guarda credenciales cifradas en archivo"""
        encrypted = self.encrypt_credentials(username, password)
        with open(output_file, 'wb') as f:
            f.write(encrypted)
    
    def load_encrypted_credentials(self, input_file: str = "credentials.enc") -> Tuple[str, str]:
        """Carga credenciales cifradas desde archivo"""
        with open(input_file, 'rb') as f:
            encrypted = f.read()
        return self.decrypt_credentials(encrypted)
