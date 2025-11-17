#!/usr/bin/env python3
"""Test manual de validadores"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from utils.validators import ConfigValidator

print("=" * 60)
print("  TEST 2: Validadores")
print("=" * 60)
print()

validator = ConfigValidator()

# Test 1: Config válido
print("[1/5] Testing config válido...")
config_valid = {
    "target_ip": "192.168.1.1",
    "knock_sequence": [[7000, "tcp"], [8000, "tcp"]],
    "interval": 0.5,
    "target_port": 1194,
}
if validator.validate(config_valid):
    print("  ✓ Config válido aceptado")
else:
    print(f"  ✗ Config válido rechazado: {validator.errors}")

# Test 2: IP inválida
print("\n[2/5] Testing IP inválida...")
config_invalid_ip = {**config_valid, "target_ip": "999.999.999.999"}
if not validator.validate(config_invalid_ip):
    print("  ✓ IP inválida detectada")
else:
    print("  ✗ IP inválida no detectada")

# Test 3: Puerto inválido
print("\n[3/5] Testing puerto inválido...")
config_invalid_port = {**config_valid, "knock_sequence": [[70000, "tcp"]]}
if not validator.validate(config_invalid_port):
    print("  ✓ Puerto inválido detectado")
else:
    print("  ✗ Puerto inválido no detectado")

# Test 4: Protocolo inválido
print("\n[4/5] Testing protocolo inválido...")
config_invalid_proto = {**config_valid, "knock_sequence": [[7000, "http"]]}
if not validator.validate(config_invalid_proto):
    print("  ✓ Protocolo inválido detectado")
else:
    print("  ✗ Protocolo inválido no detectado")

# Test 5: Campo faltante
print("\n[5/5] Testing campo faltante...")
config_missing = {"target_ip": "192.168.1.1"}
if not validator.validate(config_missing):
    print("  ✓ Campo faltante detectado")
else:
    print("  ✗ Campo faltante no detectado")

print("\n" + "=" * 60)
print("  ✓ TEST VALIDADORES COMPLETADO")
print("=" * 60)
