class VPNToolError(Exception):
    """Excepción base para todas las excepciones del sistema"""
    user_message = "Ha ocurrido un error. Contacte a Soporte IT."

class ConfigurationError(VPNToolError):
    """Errores relacionados con configuración"""
    user_message = "Configuración inválida o corrupta. Contacte a Soporte IT."

class NetworkError(VPNToolError):
    """Errores de conectividad de red"""
    user_message = "No hay conexión a internet. Verifique su red."

class PortKnockingError(VPNToolError):
    """Errores durante el proceso de port knocking"""
    user_message = "No se pudo autenticar con el servidor. Reintente o contacte a IT."

class VPNConnectionError(VPNToolError):
    """Errores de conexión VPN"""
    user_message = "No se pudo conectar a la VPN. Verifique su configuración."

class AuthenticationError(VPNToolError):
    """Errores de autenticación"""
    user_message = "Credenciales inválidas. Contacte a Soporte IT."

class TimeoutError(VPNToolError):
    """Errores por timeout"""
    user_message = "La operación ha excedido el tiempo límite. Reintente."
