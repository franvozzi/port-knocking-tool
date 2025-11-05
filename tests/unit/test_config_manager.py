import pytest
import json
from pathlib import Path
from src.core.config_manager import ConfigManager
from src.utils.exceptions import ConfigurationError
from src.utils import exceptions

# Test para verificar que _load_and_validate maneja archivos inexistentes
def test_load_and_validate_missing_file():
    try:
        ConfigManager(config_path="/nonexistent/config.json")
        pytest.fail("No se lanzó ConfigurationError para un archivo faltante.")
    except exceptions.ConfigurationError as e:
        assert "no existe" in str(e)

# Test para verificar que _load_and_validate detecta configuración inválida
def test_load_and_validate_invalid_content(tmp_path):
    invalid_config = {
        "target_ip": "invalid",
        "knock_sequence": [[1234, "tcp"]],
        "interval": 0.2,
        "target_port": 1194
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(invalid_config))
    
    try:
        ConfigManager(config_path=str(config_file))
        pytest.fail("No se lanzó ConfigurationError para contenido inválido.")
    except exceptions.ConfigurationError as e:
        assert "Configuración inválida" in str(e)

# Test de un caso válido para asegurar que no se rompió la funcionalidad correcta
def test_load_and_validate_valid_config(tmp_path):
    config_content = {
        "target_ip": "127.0.0.1",
        "knock_sequence": [[1234, "tcp"]],
        "interval": 0.2,
        "target_port": 1194
    }
    config_file = tmp_path / "config.json"
    import json
    config_file.write_text(json.dumps(config_content))
    
    # Esta inicialización no debería lanzar una excepción
    try:
        ConfigManager(config_path=str(config_file))
    except ConfigurationError as e:
        pytest.fail(f"Se lanzó una ConfigurationError inesperadamente: {e}")
