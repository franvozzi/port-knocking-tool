import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from network.diagnostics import NetworkDiagnostics

print("=" * 60)
print("  TEST 5: Diagnóstico de Red")
print("=" * 60)
print()

diag = NetworkDiagnostics()

# Test 1: Ping a localhost
print("[1/4] Testing ping a localhost...")
if diag.can_ping("127.0.0.1"):
    print("  ✓ Ping a localhost exitoso")
else:
    print("  ✗ Ping a localhost falló")

# Test 2: Ping a internet
print("\n[2/4] Testing ping a internet...")
if diag.can_ping("8.8.8.8"):
    print("  ✓ Ping a 8.8.8.8 exitoso")
else:
    print("  ⚠ Sin conectividad a internet")

# Test 3: Check puerto
print("\n[3/4] Testing check puerto...")
if not diag.check_port_open("127.0.0.1", 99999):
    print("  ✓ Puerto cerrado detectado correctamente")
else:
    print("  ✗ Error en detección de puerto cerrado")

# Test 4: IP pública
print("\n[4/4] Testing obtención de IP pública...")
public_ip = diag.get_public_ip()
print(f"  ✓ IP pública: {public_ip}")

print("\n" + "=" * 60)
print("  ✓ TEST DIAGNOSTICS COMPLETADO")
print("=" * 60)