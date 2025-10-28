import sys
import logging
from pathlib import Path

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent))

from core.config_manager import ConfigManager
from ui.gui_main import VPNConnectGUI
from monitoring.logger import StructuredLogger
from utils.exceptions import VPNToolError, ConfigurationError

def setup_logging():
    """Configura logging básico"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """Función principal"""
    setup_logging()
    logger = StructuredLogger()
    
    try:
        # Cargar configuración
        logger.log_info("Iniciando aplicación...")
        config = ConfigManager()
        
        # Iniciar GUI
        app = VPNConnectGUI(config)
        logger.log_info("GUI inicializada correctamente")
        app.run()
        
    except ConfigurationError as e:
        logger.log_error(f"Error de configuración: {e}")
        print(f"Error: {e.user_message}")
        sys.exit(1)
        
    except VPNToolError as e:
        logger.log_error(f"Error de VPN: {e}")
        print(f"Error: {e.user_message}")
        sys.exit(1)
        
    except Exception as e:
        logger.log_critical(f"Error inesperado: {e}")
        print(f"Error crítico: {e}")
        raise

if __name__ == "__main__":
    main()
