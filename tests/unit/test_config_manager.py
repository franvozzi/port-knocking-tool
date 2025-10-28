import pytest
import json
from pathlib import Path
from src.core.config_manager import ConfigManager
from src.utils.exceptions import ConfigurationError

@pytest.fixture
def temp_config_file(tmp_path):
    """Crea archivo de configuración temporal"""
    config = {
        "target_ip": "192.168.1.1",
        "knock_sequence": [[7000, "tcp"], [8000, "tcp"]],
        "interval": 0.5,
        "target_port": 1194
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config))
    return config_file

class TestConfigManager:
    """Tests para ConfigManager"""
    
    def test_load_valid_config(self, temp_config_file):
        """Test cargar configuración válida"""
        manager = ConfigManager(str(temp_config_file))
        assert manager.get_target_ip() == "192.168.1.1"
        assert len(manager.get_knock_sequence()) == 2
        assert manager.get_interval() == 0.5
        assert manager.get_target_port() == 1194
    
    def test_invalid_config_raises_error(self, tmp_path):
        """Test que configuración inválida levanta error"""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"target_ip": "invalid"}')
        
        with pytest.raises(ConfigurationError):
            ConfigManager(str(config_file))
    
    def test_missing_config_raises_error(self):
        """Test que archivo faltante levanta error"""
        with pytest.raises(ConfigurationError):
            ConfigManager("/nonexistent/config.json")
    
    def test_get_methods(self, temp_config_file):
        """Test métodos getter"""
        manager = ConfigManager(str(temp_config_file))
        assert isinstance(manager.get_target_ip(), str)
        assert isinstance(manager.get_knock_sequence(), list)
        assert isinstance(manager.get_interval(), float)
        assert isinstance(manager.get_target_port(), int)
