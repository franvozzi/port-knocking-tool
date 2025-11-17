import pytest
from src.security.crypto import CredentialsEncryptor


class TestCredentialsEncryptor:
    """Tests para CredentialsEncryptor"""

    @pytest.fixture
    def encryptor(self, tmp_path):
        """Crea encryptor con archivo temporal"""
        key_file = tmp_path / ".key"
        return CredentialsEncryptor(str(key_file))

    def test_encrypt_decrypt_credentials(self, encryptor):
        """Test cifrar y descifrar credenciales"""
        username = "testuser"
        password = "testpass123"

        encrypted = encryptor.encrypt_credentials(username, password)
        decrypted_user, decrypted_pass = encryptor.decrypt_credentials(encrypted)

        assert decrypted_user == username
        assert decrypted_pass == password

    def test_save_and_load_encrypted_credentials(self, encryptor, tmp_path):
        """Test guardar y cargar credenciales cifradas"""
        username = "testuser"
        password = "testpass123"
        creds_file = tmp_path / "creds.enc"

        encryptor.save_encrypted_credentials(username, password, str(creds_file))
        loaded_user, loaded_pass = encryptor.load_encrypted_credentials(str(creds_file))

        assert loaded_user == username
        assert loaded_pass == password

    def test_invalid_encrypted_data_raises_error(self, encryptor, authentication_error):
        """Test que datos inválidos levantan error"""
        with pytest.raises(authentication_error):
            encryptor.decrypt_credentials(b"invalid_data")
