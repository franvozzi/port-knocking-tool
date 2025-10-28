import ipaddress
from typing import Dict, Any, List, Union

class ConfigValidator:
    """Valida configuración del sistema"""
    
    def __init__(self):
        self.errors = []
    
    def validate(self, config: Dict[str, Any]) -> bool:
        """Valida configuración completa"""
        self.errors = []
        
        # Validar campos requeridos
        required_fields = ['target_ip', 'knock_sequence', 'interval', 'target_port']
        for field in required_fields:
            if field not in config:
                self.errors.append(f"Campo requerido faltante: {field}")
        
        if self.errors:
            return False
        
        # Validar IP
        if not self.validate_ip(config['target_ip']):
            self.errors.append(f"IP inválida: {config['target_ip']}")
        
        # Validar secuencia de knocks
        if not self.validate_knock_sequence(config['knock_sequence']):
            self.errors.append("Secuencia de knocks inválida")
        
        # Validar intervalo
        if not self.validate_interval(config['interval']):
            self.errors.append("Intervalo inválido (debe ser 0.1 - 5.0)")
        
        # Validar puerto objetivo
        if not self.validate_port(config['target_port']):
            self.errors.append(f"Puerto inválido: {config['target_port']}")
        
        return len(self.errors) == 0
    
    @staticmethod
    def validate_ip(ip: str) -> bool:
        """Valida dirección IP"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_knock_sequence(sequence: List) -> bool:
        """Valida secuencia de knocks"""
        if not isinstance(sequence, list) or len(sequence) == 0:
            return False
        
        for knock in sequence:
            if not isinstance(knock, list) or len(knock) != 2:
                return False
            
            port, protocol = knock
            if not isinstance(port, int) or not (1 <= port <= 65535):
                return False
            if protocol not in ['tcp', 'udp']:
                return False
        
        return True
    
    @staticmethod
    def validate_port(port: Union[int, str]) -> bool:
        """Valida puerto"""
        try:
            port_int = int(port)
            return 1 <= port_int <= 65535
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_interval(interval: Union[float, int]) -> bool:
        """Valida intervalo de knocking"""
        try:
            interval_float = float(interval)
            return 0.1 <= interval_float <= 5.0
        except (ValueError, TypeError):
            return False
