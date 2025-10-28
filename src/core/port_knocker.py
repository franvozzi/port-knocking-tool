import socket
import time
from typing import List, Tuple, Optional
from datetime import datetime

from utils.exceptions import PortKnockingError, NetworkError
from utils.constants import DEFAULT_KNOCK_TIMEOUT, DEFAULT_FIREWALL_PROCESS_TIME
from monitoring.logger import StructuredLogger

class PortKnocker:
    """Cliente de Port Knocking"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.logger = StructuredLogger()
    
    def execute_sequence(self, 
                        target_ip: str,
                        knock_sequence: List[Tuple[int, str]],
                        interval: float,
                        target_port: int,
                        progressive_check: bool = False) -> bool:
        """
        Ejecuta secuencia de port knocking
        
        Args:
            target_ip: IP del servidor
            knock_sequence: Lista de (puerto, protocolo)
            interval: Intervalo entre knocks en segundos
            target_port: Puerto final a verificar
            progressive_check: Verificar tras cada knock
            
        Returns:
            True si exitoso, False si falló
        """
        try:
            self._print_header(target_ip, len(knock_sequence), interval)
            
            # Verificar estado inicial
            initial_open = self._tcp_ping(target_ip, target_port)
            self._log(f"[?] Verificando estado inicial del puerto {target_port}...")
            
            if initial_open:
                self._log(f"[!] Puerto {target_port} ya está abierto")
            else:
                self._log(f"[+] Puerto {target_port} cerrado (esperado)")
            
            # Ejecutar secuencia
            self._log("\n[>>] Ejecutando secuencia de knocks:\n")
            
            for idx, (port, protocol) in enumerate(knock_sequence, 1):
                result = self._knock_port(target_ip, port, protocol)
                status = "[+]" if result else "[!]"
                self._log(f"[{idx}/{len(knock_sequence)}] Knock {protocol.upper()} -> Puerto {port}... {status}")
                
                if progressive_check:
                    if self._tcp_ping(target_ip, target_port):
                        self._log(f"\n[SUCCESS] Puerto {target_port} abierto tras knock #{idx}")
                        return True
                
                time.sleep(interval)
            
            # Resumen
            self._log(f"\n{'='*70}")
            self._log(f"SECUENCIA COMPLETADA: {len(knock_sequence)}/{len(knock_sequence)} knocks exitosos")
            self._log(f"{'='*70}\n")
            
            # Esperar procesamiento del firewall
            self._log(f"[*] Esperando {DEFAULT_FIREWALL_PROCESS_TIME}s que el firewall procese la address list...\n")
            time.sleep(DEFAULT_FIREWALL_PROCESS_TIME)
            
            # Verificación final
            verification_result = self._verify_port_open(target_ip, target_port)
            
            if verification_result['open']:
                self._log_success(target_port, verification_result)
                self.logger.log_connection_attempt(target_ip, True, 0)
                return True
            else:
                self._log_failure(target_port, verification_result)
                self.logger.log_connection_attempt(target_ip, False, 0)
                return False
                
        except Exception as e:
            self.logger.log_error(f"Error en port knocking: {e}")
            raise PortKnockingError(f"Error ejecutando port knocking: {e}")
    
    def _knock_port(self, ip: str, port: int, protocol: str) -> bool:
        """Ejecuta knock en un puerto específico"""
        try:
            if protocol == 'tcp':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(DEFAULT_KNOCK_TIMEOUT)
                sock.connect_ex((ip, port))
                sock.close()
                return True
            elif protocol == 'udp':
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(b'', (ip, port))
                sock.close()
                return True
        except Exception as e:
            if self.verbose:
                self._log(f"    Error en knock {port}/{protocol}: {e}")
            return False
    
    def _tcp_ping(self, ip: str, port: int, timeout: int = 1) -> bool:
        """Verifica si puerto TCP está abierto"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def _verify_port_open(self, ip: str, port: int, attempts: int = 3) -> dict:
        """Verifica apertura del puerto con múltiples intentos"""
        successful_attempts = 0
        latencies = []
        
        for _ in range(attempts):
            start_time = time.time()
            is_open = self._tcp_ping(ip, port, timeout=2)
            latency = (time.time() - start_time) * 1000
            
            if is_open:
                successful_attempts += 1
                latencies.append(latency)
            
            time.sleep(0.5)
        
        return {
            'open': successful_attempts > 0,
            'success_count': successful_attempts,
            'total_attempts': attempts,
            'avg_latency': sum(latencies) / len(latencies) if latencies else 0
        }
    
    def _print_header(self, ip: str, knock_count: int, interval: float):
        """Imprime encabezado de información"""
        if not self.verbose:
            return
        
        self._log("\n" + "="*70)
        self._log(f"INICIANDO PORT KNOCKING A {ip}")
        self._log(f"Knocks: {knock_count} | Intervalo: {interval}s")
        self._log("Modo: TCP SYN-only (primer handshake solamente)")
        self._log(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._log("="*70 + "\n")
    
    def _log_success(self, port: int, result: dict):
        """Log de éxito"""
        self._log("-"*70)
        self._log("RESULTADO DE VERIFICACION:")
        self._log("-"*70)
        self._log(f"Puerto: {port}")
        self._log(f"Estado: [+] ABIERTO")
        self._log(f"Intentos exitosos: {result['success_count']}/{result['total_attempts']}")
        if result['avg_latency'] > 0:
            self._log(f"Latencia promedio: {result['avg_latency']:.2f}ms")
        self._log("-"*70 + "\n")
        self._log("[SUCCESS] PORT KNOCKING EXITOSO - Puerto accesible\n")
    
    def _log_failure(self, port: int, result: dict):
        """Log de fallo"""
        self._log("-"*70)
        self._log("RESULTADO DE VERIFICACION:")
        self._log("-"*70)
        self._log(f"Puerto: {port}")
        self._log(f"Estado: [-] CERRADO")
        self._log(f"Intentos exitosos: {result['success_count']}/{result['total_attempts']}")
        self._log("-"*70 + "\n")
        self._log("[FAILED] PORT KNOCKING FALLO - Puerto sigue cerrado")
        self._log("   Verifica la secuencia y configuracion del servidor\n")
    
    def _log(self, message: str):
        """Log condicional según verbosity"""
        if self.verbose:
            print(message)
