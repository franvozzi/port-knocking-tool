"""
Sistema de logging estructurado
"""
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Optional
import os

from utils.constants import LOG_DIRECTORY

class StructuredLogger:
    """Logger estructurado para auditoría y debugging"""
    
    def __init__(self, log_file: Optional[str] = None):
        self.log_dir = Path(LOG_DIRECTORY)
        self.log_dir.mkdir(exist_ok=True)
        
        if log_file is None:
            log_file = self.log_dir / f"vpn_connect_{datetime.now().strftime('%Y%m%d')}.log"
        else:
            log_file = self.log_dir / log_file
        
        self.log_file = log_file
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Configura logger"""
        logger = logging.getLogger("VPNConnect")
        logger.setLevel(logging.DEBUG)
        
        # Handler para archivo
        fh = logging.FileHandler(self.log_file, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        
        # Handler para consola
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def log_connection_attempt(self, ip: str, success: bool, duration: float):
        """Log de intento de conexión"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "connection_attempt",
            "target_ip": ip,
            "result": "success" if success else "failed",
            "duration_ms": round(duration * 1000, 2),
            "user": os.getenv("USER", "unknown")
        }
        self.logger.info(json.dumps(log_entry, ensure_ascii=False))
    
    def log_info(self, message: str):
        """Log de información"""
        self.logger.info(message)
    
    def log_warning(self, message: str):
        """Log de advertencia"""
        self.logger.warning(message)
    
    def log_error(self, message: str):
        """Log de error"""
        self.logger.error(message)
    
    def log_critical(self, message: str):
        """Log crítico"""
        self.logger.critical(message)
    
    def log_audit(self, action: str, details: str):
        """Log de auditoría"""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "audit",
            "action": action,
            "details": details,
            "user": os.getenv("USER", "unknown")
        }
        self.logger.info(f"[AUDIT] {json.dumps(audit_entry, ensure_ascii=False)}")
