#!/usr/bin/env python3
"""Test manual de cifrado"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from security.crypto import CredentialsEncryptor

print("=" * 60)
print("  TEST 4: Cifrado de Credenciales")
print("=" * 60)
print()

# Test 1: Cifrar/Descifrar
print("[1/3] Testing cifrado/descifrado...")
encryptor = CredentialsEncryptor(".test_key")

username = "testuser"
password = "testpass123"

encrypted = encryptor.encrypt_credentials(username, password)
print(f"  ✓ Cifrado: {len(encrypted)} bytes")

decrypted_user, decrypted_pass = encryptor.decrypt_credentials(encrypted)
if decrypted_user == username and decrypted_pass == password:
    print(f"  ✓ Descifrado correcto: {decrypted_user}")
else:
    print(f"  ✗ Error en descifrado")

# Test 2: Guardar/Cargar
print("\n[2/3] Testing guardar/cargar...")
creds_file = "test_creds.enc"
encryptor.save_encrypted_credentials(username, password, creds_file)
print(f"  ✓ Guardado en {creds_file}")

loaded_user, loaded_pass = encryptor.load_encrypted_credentials(creds_file)
if loaded_user == username and loaded_pass == password:
    print(f"  ✓ Cargado correctamente")
else:
    print(f"  ✗ Error al cargar")

# Test 3: Datos inválidos
print("\n[3/3] Testing datos inválidos...")
try:
    encryptor.decrypt_credentials(b"invalid_data")
    print("  ✗ Datos inválidos no detectados")
except Exception:
    print("  ✓ Datos inválidos detectados")

# Cleanup
Path(".test_key").unlink()
Path(creds_file).unlink()

print("\n" + "=" * 60)
print("  ✓ TEST CRYPTO COMPLETADO")
print("=" * 60)
