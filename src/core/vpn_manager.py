import platform
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import sys

from utils.exceptions import VPNConnectionError
from monitoring.logger import StructuredLogger


class VPNManager(ABC):
    """Clase abstracta base para gestores VPN"""

    def __init__(self):
        self.logger = StructuredLogger()
        self.connected = False

    @abstractmethod
    def connect(self, profile_path: str, credentials_path: Optional[str] = None) -> bool:
        """Conecta a VPN"""
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """Desconecta de VPN"""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Verifica si está conectado"""
        pass

    def _find_profile(self, profile_name: str = "profile.ovpn") -> Path:
        """Busca archivo de perfil VPN"""
        if getattr(sys, "frozen", False):
            base_path = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(".")
            search_paths = [base_path / profile_name]
        else:
            search_paths = [
                Path.cwd() / profile_name,
                Path(__file__).parent.parent / profile_name,
                Path(__file__).parent.parent.parent / profile_name,
            ]

        for path in search_paths:
            if path.exists():
                return path

        raise VPNConnectionError(f"Perfil VPN {profile_name} no encontrado")


class MacOSVPNManager(VPNManager):
    """Gestor VPN para macOS"""

    def connect(self, profile_path: str, credentials_path: Optional[str] = None) -> bool:
        try:
            profile = self._find_profile(profile_path)

            # Comando para OpenVPN en macOS
            cmd = ["sudo", "openvpn", "--config", str(profile), "--daemon"]

            if credentials_path:
                cmd.extend(["--auth-user-pass", credentials_path])

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                self.connected = True
                self.logger.log_info("VPN conectada exitosamente (macOS)")
                return True
            else:
                self.logger.log_error(f"Error conectando VPN: {result.stderr}")
                return False

        except Exception as e:
            self.logger.log_error(f"Error en conexión VPN macOS: {e}")
            raise VPNConnectionError(f"Error conectando VPN: {e}")

    def disconnect(self) -> bool:
        try:
            # Matar proceso OpenVPN
            subprocess.run(["sudo", "pkill", "-9", "openvpn"], capture_output=True)
            self.connected = False
            self.logger.log_info("VPN desconectada (macOS)")
            return True
        except Exception as e:
            self.logger.log_error(f"Error desconectando VPN: {e}")
            return False

    def is_connected(self) -> bool:
        try:
            result = subprocess.run(["pgrep", "openvpn"], capture_output=True)
            return result.returncode == 0
        except:
            return False


class WindowsVPNManager(VPNManager):
    """Gestor VPN para Windows"""

    def connect(self, profile_path: str, credentials_path: Optional[str] = None) -> bool:
        try:
            profile = self._find_profile(profile_path)

            # OpenVPN GUI para Windows
            openvpn_path = r"C:\Program Files\OpenVPN\bin\openvpn-gui.exe"

            cmd = [openvpn_path, "--connect", str(profile)]

            subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            self.connected = True
            self.logger.log_info("VPN conectada exitosamente (Windows)")
            return True

        except Exception as e:
            self.logger.log_error(f"Error en conexión VPN Windows: {e}")
            raise VPNConnectionError(f"Error conectando VPN: {e}")

    def disconnect(self) -> bool:
        try:
            subprocess.run(["taskkill", "/F", "/IM", "openvpn-gui.exe"], capture_output=True)
            self.connected = False
            self.logger.log_info("VPN desconectada (Windows)")
            return True
        except Exception as e:
            self.logger.log_error(f"Error desconectando VPN: {e}")
            return False

    def is_connected(self) -> bool:
        try:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq openvpn-gui.exe"], capture_output=True, text=True
            )
            return "openvpn-gui.exe" in result.stdout
        except:
            return False


class LinuxVPNManager(VPNManager):
    """Gestor VPN para Linux"""

    def connect(self, profile_path: str, credentials_path: Optional[str] = None) -> bool:
        try:
            profile = self._find_profile(profile_path)

            cmd = [
                "pkexec",
                "openvpn",
                "--config",
                str(profile),
                "--daemon",
                "--log",
                "/tmp/openvpn.log",
            ]

            if credentials_path:
                cmd.extend(["--auth-user-pass", credentials_path])

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                self.connected = True
                self.logger.log_info("VPN conectada exitosamente (Linux)")
                return True
            else:
                self.logger.log_error(f"Error conectando VPN: {result.stderr}")
                return False

        except Exception as e:
            self.logger.log_error(f"Error en conexión VPN Linux: {e}")
            raise VPNConnectionError(f"Error conectando VPN: {e}")

    def disconnect(self) -> bool:
        try:
            subprocess.run(["pkexec", "killall", "openvpn"], capture_output=True)
            self.connected = False
            self.logger.log_info("VPN desconectada (Linux)")
            return True
        except Exception as e:
            self.logger.log_error(f"Error desconectando VPN: {e}")
            return False

    def is_connected(self) -> bool:
        try:
            result = subprocess.run(["pgrep", "openvpn"], capture_output=True)
            return result.returncode == 0
        except:
            return False


def get_vpn_manager() -> VPNManager:
    """Factory para obtener gestor VPN según sistema operativo"""
    system = platform.system()

    if system == "Darwin":
        return MacOSVPNManager()
    elif system == "Windows":
        return WindowsVPNManager()
    elif system == "Linux":
        return LinuxVPNManager()
    else:
        raise NotImplementedError(f"Sistema operativo {system} no soportado")
