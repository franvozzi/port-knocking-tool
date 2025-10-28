import pytest
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture
def sample_config():
    """Configuración de ejemplo"""
    return {
        "target_ip": "127.0.0.1",
        "knock_sequence": [[7000, "tcp"], [8000, "tcp"]],
        "interval": 0.5,
        "target_port": 1194
    }

@pytest.fixture
def sample_knock_sequence():
    """Secuencia de knocks de ejemplo"""
    return [[7000, "tcp"], [8000, "tcp"], [9000, "tcp"]]
