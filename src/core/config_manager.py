import json
from pathlib import Path
from typing import Dict, Any, Optional
import sys

from utils.validators import ConfigValidator
from utils.exceptions import ConfigurationError
from utils.constants import CONFIG_FILENAME, HIDDEN_CONFIG_FILENAME

class ConfigManager:
    """Gestor de configuración del sistema"""
    
    def __init__(self, config_path: Optional[str] = None):
        self._config_path_str = config_path
        self._load_and_validate()

    def _load_and_validate(self):
        """Carga y valida la configuración."""
        if self._config_path_str:
            self.config_path = Path(self._config_path_str)
            if not self.config_path.exists():
                raise ConfigurationError(f"El archivo de configuración especificado no existe: {self._config_path_str}")
        else:
            self.config_path = self._find_config()

        self.config = self._load_config()
        self._validate_config()
    
    def _find_config(self) -> Path:
        """Busca config.json en múltiples ubicaciones"""
        # Si está empaquetado con PyInstaller
        if getattr(sys, 'frozen', False):
            base_path = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path('.')
            search_paths = [
                base_path / CONFIG_FILENAME,
                base_path / HIDDEN_CONFIG_FILENAME,
            ]
        else:
            # Modo desarrollo
            search_paths = [
                Path.cwd() / CONFIG_FILENAME,
                Path.cwd() / HIDDEN_CONFIG_FILENAME,
                Path(__file__).parent.parent / CONFIG_FILENAME,
                Path(__file__).parent.parent.parent / CONFIG_FILENAME,
            ]
        
        for path in search_paths:
            if path.exists():
                return path
        
        raise ConfigurationError(
            f"{CONFIG_FILENAME} no encontrado en las ubicaciones esperadas"
        )
    
    def _load_config(self) -> Dict[str, Any]:
        """Carga configuración desde archivo"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Archivo de configuración corrupto: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error al leer configuración: {e}")
    
    def _validate_config(self):
        """Valida la configuración cargada"""
        validator = ConfigValidator()
        if not validator.validate(self.config):
            errors = "\n".join(validator.errors)
            raise ConfigurationError(f"Configuración inválida:\n{errors}")
    
    def get(self, key: str, default=None):
        """Obtiene valor de configuración"""
        return self.config.get(key, default)
    
    def get_target_ip(self) -> str:
        """Obtiene IP objetivo"""
        return self.config['target_ip']
    
    def get_knock_sequence(self) -> list:
        """Obtiene secuencia de knocks"""
        return self.config['knock_sequence']
    
    def get_interval(self) -> float:
        """Obtiene intervalo entre knocks"""
        return float(self.config['interval'])
    
    def get_target_port(self) -> int:
        """Obtiene puerto objetivo"""
        return int(self.config['target_port'])
    
    def update(self, key: str, value: Any):
        """Actualiza valor de configuración"""
        self.config[key] = value
        self._save_config()
    
    def _save_config(self):
        """Guarda configuración actualizada"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ConfigurationError(f"Error al guardar configuración: {e}")
    
    def reload(self):
        """Recarga configuración desde archivo"""
        self.config = self._load_config()
        self._validate_config()
