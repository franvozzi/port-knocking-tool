# Versión de la aplicación
VERSION = "2.0.0"

# Timeouts (segundos)
DEFAULT_KNOCK_TIMEOUT = 2
DEFAULT_VPN_CONNECT_TIMEOUT = 30
DEFAULT_FIREWALL_PROCESS_TIME = 5

# Puertos por defecto
DEFAULT_VPN_PORT = 1194

# Intervalos por defecto
DEFAULT_KNOCK_INTERVAL = 0.5

# Paths
LOG_DIRECTORY = "logs"
CONFIG_FILENAME = "config.json"
HIDDEN_CONFIG_FILENAME = ".config.json"

# UI
DEFAULT_WINDOW_WIDTH = 450
DEFAULT_WINDOW_HEIGHT = 250

# Colores
COLORS = {
    "idle": "#666666",
    "connecting": "#FF9800",
    "connected": "#4CAF50",
    "error": "#F44336",
    "success": "#4CAF50",
}

# Mensajes de estado
STATUS_MESSAGES = {
    "idle": "Listo para conectar",
    "authenticating": "Autenticando...",
    "connecting": "Estableciendo conexión VPN...",
    "connected": "✓ Conectado exitosamente",
    "error": "✗ Error de conexión",
    "disconnecting": "Desconectando...",
    "disconnected": "Desconectado",
}
