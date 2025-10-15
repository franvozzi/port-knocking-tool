import tkinter as tk
from tkinter import messagebox
import threading
import time
import subprocess
import platform
import json
import sys
from pathlib import Path
from main import PortKnocker

class VPNConnectGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Conexión VPN Corporativa")
        self.window.geometry("450x250")
        self.window.resizable(False, False)
        
        # Detectar sistema operativo
        self.os_type = platform.system()
        
        # Cargar configuración
        self.config = self.load_config()
        
        # UI
        title = tk.Label(self.window, text="VPN Corporativa", 
                        font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        self.status_label = tk.Label(self.window, text="Listo para conectar", 
                                     font=("Arial", 11), fg="#666")
        self.status_label.pack(pady=10)
        
        self.connect_btn = tk.Button(self.window, text="Conectar", 
                                     command=self.start_connection,
                                     font=("Arial", 13, "bold"), 
                                     bg="#4CAF50", fg="white",
                                     width=18, height=2, cursor="hand2")
        self.connect_btn.pack(pady=15)
        
        self.disconnect_btn = tk.Button(self.window, text="Desconectar",
                                       command=self.disconnect_vpn,
                                       font=("Arial", 10),
                                       state="disabled", width=18)
        self.disconnect_btn.pack(pady=5)
        
    def load_config(self):
        """Carga configuración desde config.json o .config.json"""
        # Busca en la carpeta actual (desarrollo)
        local_path = Path(__file__).parent / 'config.json'
        if local_path.exists():
            with open(local_path) as f:
                return json.load(f)
        
        # Busca config oculto
        hidden_path = Path(__file__).parent / '.config.json'
        if hidden_path.exists():
            with open(hidden_path) as f:
                return json.load(f)
        
        # Si está empaquetado con PyInstaller
        if getattr(sys, 'frozen', False):
            bundle_dir = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path('.')
            bundle_path = bundle_dir / 'config.json'
            if bundle_path.exists():
                with open(bundle_path) as f:
                    return json.load(f)
        
        raise FileNotFoundError("No se encontró config.json. Contacte a Soporte IT.")
    
    def update_status(self, message, color="#666"):
        """Actualiza estado visual"""
        self.status_label.config(text=message, fg=color)
        self.window.update()
    
    def start_connection(self):
        """Inicia proceso de conexión en thread separado"""
        self.connect_btn.config(state="disabled")
        thread = threading.Thread(target=self.do_connection, daemon=True)
        thread.start()
    
    def do_connection(self):
        """Proceso completo: port knocking + VPN"""
        try:
            # Fase 1: Port Knocking
            self.update_status("Autenticando...", "#FF9800")
            
            knocker = PortKnocker(self.config['target_ip'], verbose=False)
            result = knocker.execute_sequence(
                self.config['knock_sequence'],
                self.config['interval'],
                self.config.get('target_port', 1194),
                progressive_check=False
            )
            
            if not result:
                raise Exception("Autenticación fallida")
            
            # Fase 2: Conectar VPN
            self.update_status("Estableciendo conexión VPN...", "#2196F3")
            self.connect_openvpn()
            
            self.update_status("✓ Conectado exitosamente", "#4CAF50")
            self.connect_btn.config(state="disabled")
            self.disconnect_btn.config(state="normal")
            
        except Exception as e:
            self.update_status("✗ Error de conexión", "#F44336")
            messagebox.showerror("Error de Conexión", 
                "No se pudo establecer la conexión.\n\n"
                "Contacte a Soporte IT si el problema persiste.")
            self.connect_btn.config(state="normal")
    
    def connect_openvpn(self):
        """Conecta OpenVPN según sistema operativo"""
        ovpn_file = Path(__file__).parent / 'profile.ovpn'
        
        if self.os_type == 'Windows':
            openvpn_path = r"C:\Program Files\OpenVPN\bin\openvpn-gui.exe"
            cmd = [openvpn_path, "--connect", str(ovpn_file)]
            
        elif self.os_type == 'Darwin':  # macOS
            cmd = ['sudo', 'openvpn', '--config', str(ovpn_file), '--daemon']
            
        else:  # Linux
            cmd = ['pkexec', 'openvpn', '--config', str(ovpn_file), 
                   '--daemon', '--log', '/tmp/openvpn.log']
        
        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    def disconnect_vpn(self):
        """Desconecta VPN según sistema operativo"""
        try:
            if self.os_type == 'Windows':
                subprocess.run(['taskkill', '/F', '/IM', 'openvpn-gui.exe'], 
                             capture_output=True)
                
            elif self.os_type == 'Darwin':
                subprocess.run(['pkill', '-9', 'openvpn'], capture_output=True)
                
            else:  # Linux
                subprocess.run(['pkexec', 'killall', 'openvpn'], 
                             capture_output=True)
            
            self.update_status("Desconectado", "#666")
            self.connect_btn.config(state="normal")
            self.disconnect_btn.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al desconectar: {str(e)}")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = VPNConnectGUI()
    app.run()
