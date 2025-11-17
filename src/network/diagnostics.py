import socket
import subprocess
import platform
from typing import List, Dict


class NetworkDiagnostics:
    """Herramientas de diagnóstico de red"""

    @staticmethod
    def can_ping(host: str, timeout: int = 2) -> bool:
        """Verifica conectividad básica"""
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = [
            "ping",
            param,
            "1",
            "-W" if platform.system().lower() != "windows" else "-w",
            str(timeout),
            host,
        ]

        try:
            result = subprocess.run(command, capture_output=True, timeout=timeout + 1)
            return result.returncode == 0
        except:
            return False

    @staticmethod
    def check_port_open(host: str, port: int, timeout: int = 2) -> bool:
        """Verifica si puerto está abierto"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False

    @staticmethod
    def get_public_ip() -> str:
        """Obtiene IP pública"""
        try:
            import urllib.request

            response = urllib.request.urlopen("https://api.ipify.org", timeout=5)
            return response.read().decode("utf-8")
        except:
            return "unknown"

    def diagnose_connection_failure(self, target_ip: str, target_port: int) -> List[str]:
        """Diagnostica fallo de conexión"""
        issues = []

        # Test 1: Ping básico
        if not self.can_ping(target_ip):
            issues.append("No hay conectividad básica al servidor")

        # Test 2: Puerto específico
        if not self.check_port_open(target_ip, target_port):
            issues.append(f"Puerto {target_port} no accesible")

        # Test 3: DNS (si es hostname)
        try:
            socket.gethostbyname(target_ip)
        except socket.gaierror:
            if not self._is_ip(target_ip):
                issues.append("Error de resolución DNS")

        return issues

    @staticmethod
    def _is_ip(address: str) -> bool:
        """Verifica si es dirección IP válida"""
        try:
            socket.inet_aton(address)
            return True
        except:
            return False

    def get_diagnostic_report(self, target_ip: str, target_port: int) -> Dict:
        """Genera reporte de diagnóstico"""
        return {
            "target_ip": target_ip,
            "target_port": target_port,
            "can_ping": self.can_ping(target_ip),
            "port_open": self.check_port_open(target_ip, target_port),
            "public_ip": self.get_public_ip(),
            "issues": self.diagnose_connection_failure(target_ip, target_port),
        }
