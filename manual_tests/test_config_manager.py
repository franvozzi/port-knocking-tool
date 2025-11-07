import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core.config_manager import ConfigManager
from utils.exceptions import ConfigurationError

print("=" * 60)
print("  TEST 3: ConfigManager")
print("=" * 60)
print()

# Crear config temporal
test_config = {
    "target_ip": "127.0.0.1",
    "knock_sequence": [[7000, "tcp"], [8000, "tcp"]],
    "interval": 0.5,
    "target_port": 1194
}

config_path = Path("test_config.json")
with open(config_path, "w") as f:
    json.dump(test_config, f)

# Test 1: Cargar config
print("[1/4] Testing carga de config...")
try:
    manager = ConfigManager(str(config_path))
    print(f"  ✓ Config cargado: {manager.get_target_ip()}")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 2: Getters
print("\n[2/4] Testing getters...")
try:
    assert manager.get_target_ip() == "127.0.0.1"
    assert len(manager.get_knock_sequence()) == 2
    assert manager.get_interval() == 0.5
    assert manager.get_target_port() == 1194
    print("  ✓ Todos los getters funcionan")
except AssertionError as e:
    print(f"  ✗ Error en getters: {e}")

# Test 3: Config inválido
print("\n[3/4] Testing config inválido...")
invalid_config_path = Path("test_invalid_config.json")
with open(invalid_config_path, "w") as f:
    json.dump({"invalid": "data"}, f)

try:
    ConfigManager(str(invalid_config_path))
    print("  ✗ Config inválido no detectado")
except ConfigurationError:
    print("  ✓ Config inválido detectado correctamente")

# Test 4: Archivo faltante
print("\n[4/4] Testing archivo faltante...")
try:
    ConfigManager("nonexistent.json")
    print("  ✗ Archivo faltante no detectado")
except ConfigurationError:
    print("  ✓ Archivo faltante detectado correctamente")

# Cleanup
config_path.unlink()
invalid_config_path.unlink()

print("\n" + "=" * 60)
print("  ✓ TEST CONFIG MANAGER COMPLETADO")
print("=" * 60)