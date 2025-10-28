import tkinter as tk
from tkinter import messagebox
import threading
import time
from pathlib import Path

from core.config_manager import ConfigManager
from core.port_knocker import PortKnocker
from core.vpn_manager import get_vpn_manager
from monitoring.logger import StructuredLogger
from monitoring.metrics import MetricsCollector
from utils.exceptions import VPNToolError
from utils.constants import (
    DEFAULT_WINDOW_WIDTH,
    DEFAULT_WINDOW_HEIGHT,
    COLORS,
    STATUS_MESSAGES
)
from ui.widgets.status_bar import StatusBar
from ui.widgets.progress_bar import ConnectionProgress

class VPNConnectGUI:
    """Interfaz gráfica principal de la aplicación"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.logger = StructuredLogger()
        self.metrics = MetricsCollector()
        
        # Componentes de negocio
        self.knocker = PortKnocker(verbose=False)
        self.vpn_manager = get_vpn_manager()
        
        # Ventana principal
        self.window = tk.Tk()
        self.window.title("VPN Corporativa")
        self.window.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")
        self.window.resizable(False, False)
        
        # Estado
        self.connection_start_time = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura interfaz de usuario"""
        # Título
        title = tk.Label(
            self.window,
            text="VPN Corporativa",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=20)
        
        # Widget de estado
        self.status_bar = StatusBar(self.window)
        self.status_bar.pack(pady=10)
        
        # Barra de progreso
        self.progress = ConnectionProgress(self.window)
        self.progress.pack(pady=10)
        
        # Botón conectar
        self.connect_btn = tk.Button(
            self.window,
            text="Conectar",
            command=self.start_connection,
            font=("Arial", 13, "bold"),
            bg=COLORS["connected"],
            fg="white",
            width=18,
            height=2,
            cursor="hand2"
        )
        self.connect_btn.pack(pady=15)
        
        # Botón desconectar
        self.disconnect_btn = tk.Button(
            self.window,
            text="Desconectar",
            command=self.disconnect_vpn,
            font=("Arial", 10),
            state="disabled",
            width=18
        )
        self.disconnect_btn.pack(pady=5)
    
    def start_connection(self):
        """Inicia proceso de conexión en thread separado"""
        self.connect_btn.config(state="disabled")
        self.connection_start_time = time.time()
        thread = threading.Thread(target=self.do_connection, daemon=True)
        thread.start()
    
    def do_connection(self):
        """Proceso completo: port knocking + VPN"""
        try:
            # Fase 1: Port Knocking
            self.status_bar.update(STATUS_MESSAGES["authenticating"], "connecting")
            self.progress.set_progress(30)
            
            success = self.knocker.execute_sequence(
                self.config.get_target_ip(),
                self.config.get_knock_sequence(),
                self.config.get_interval(),
                self.config.get_target_port(),
                progressive_check=False
            )
            
            if not success:
                raise VPNToolError("Port knocking falló")
            
            self.progress.set_progress(60)
            
            # Fase 2: Conectar VPN
            self.status_bar.update(STATUS_MESSAGES["connecting"], "connecting")
            
            vpn_success = self.vpn_manager.connect("profile.ovpn", "credentials.txt")
            
            if not vpn_success:
                raise VPNToolError("Conexión VPN falló")
            
            self.progress.set_progress(100)
            
            # Éxito
            duration = time.time() - self.connection_start_time
            self.metrics.record_attempt(True, duration)
            
            self.status_bar.update(STATUS_MESSAGES["connected"], "connected")
            self.connect_btn.config(state="disabled")
            self.disconnect_btn.config(state="normal")
            
            self.logger.log_info("Conexión VPN establecida exitosamente")
            
        except VPNToolError as e:
            self.handle_connection_error(str(e))
        except Exception as e:
            self.handle_connection_error(f"Error inesperado: {e}")
    
    def handle_connection_error(self, error_msg: str):
        """Maneja errores de conexión"""
        duration = time.time() - self.connection_start_time if self.connection_start_time else 0
        self.metrics.record_attempt(False, duration)
        
        self.status_bar.update(STATUS_MESSAGES["error"], "error")
        self.progress.set_progress(0)
        
        self.logger.log_error(error_msg)
        
        messagebox.showerror(
            "Error de Conexión",
            "No se pudo establecer la conexión.\n\n"
            "Contacte a Soporte IT si el problema persiste."
        )
        
        self.connect_btn.config(state="normal")
    
    def disconnect_vpn(self):
        """Desconecta VPN"""
        try:
            self.status_bar.update(STATUS_MESSAGES["disconnecting"], "idle")
            
            self.vpn_manager.disconnect()
            
            self.status_bar.update(STATUS_MESSAGES["disconnected"], "idle")
            self.progress.set_progress(0)
            
            self.connect_btn.config(state="normal")
            self.disconnect_btn.config(state="disabled")
            
            self.logger.log_info("VPN desconectada")
            
        except Exception as e:
            self.logger.log_error(f"Error desconectando: {e}")
            messagebox.showerror("Error", f"Error al desconectar: {e}")
    
    def run(self):
        """Ejecuta la aplicación"""
        self.logger.log_info("Aplicación iniciada")
        self.window.mainloop()
