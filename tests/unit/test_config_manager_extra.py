import json
import pytest

from src.core.config_manager import ConfigManager
from src.utils.exceptions import ConfigurationError


def write_config(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def test_config_manager_load_and_getters(tmp_path):
    cfg = {
        "target_ip": "10.0.0.1",
        "knock_sequence": [[7000, "tcp"]],
        "interval": 0.2,
        "target_port": 1194
    }

    file = tmp_path / 'config.json'
    write_config(file, cfg)

    manager = ConfigManager(str(file))

    assert manager.get_target_ip() == "10.0.0.1"
    assert manager.get_knock_sequence() == [[7000, "tcp"]]
    assert manager.get_interval() == 0.2
    assert manager.get_target_port() == 1194


def test_config_manager_update_and_reload(tmp_path):
    cfg = {
        "target_ip": "10.0.0.1",
        "knock_sequence": [[7000, "tcp"]],
        "interval": 0.2,
        "target_port": 1194
    }

    file = tmp_path / 'config.json'
    write_config(file, cfg)

    manager = ConfigManager(str(file))
    manager.update('target_ip', '192.168.0.5')

    # Reload from disk and verify
    manager.reload()
    assert manager.get_target_ip() == '192.168.0.5'


def test_config_manager_invalid_json(tmp_path):
    file = tmp_path / 'config.json'
    file.write_text('{ invalid json')

    with pytest.raises(ConfigurationError):
        ConfigManager(str(file))


def test_config_manager_missing_required(tmp_path):
    cfg = {"some": "value"}
    file = tmp_path / 'config.json'
    write_config(file, cfg)

    with pytest.raises(ConfigurationError):
        ConfigManager(str(file))
