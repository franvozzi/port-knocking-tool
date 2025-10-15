#!/usr/bin/env python3
"""
Servidor dummy de port knocking para pruebas locales
Escucha en los puertos configurados y simula apertura de puerto VPN
"""

import socket
import threading
import time
from datetime import datetime

class KnockServer:
    def __init__(self, knock_ports, target_port):
        self.knock_ports = knock_ports
        self.target_port = target_port
        self.knock_attempts = {}
        self.knock_timestamps = {}
        self.vpn_port_open = False
        self.vpn_socket = None
        self.SEQUENCE_TIMEOUT = 5  # segundos
        
    def listen_knock(self, port):
        """Escucha intentos de conexión en un puerto de knock"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1', port))
        sock.listen(5)
        
        print(f"[knockd] Escuchando knocks en puerto {port}")
        
        while True:
            try:
                conn, addr = sock.accept()
                ip = addr[0]
                now = time.time()
                
                # Limpiar knocks antiguos (timeout)
                if ip in self.knock_timestamps:
                    if now - self.knock_timestamps[ip] > self.SEQUENCE_TIMEOUT:
                        self.knock_attempts[ip] = []
                        print(f"[knockd] Secuencia de {ip} expiró. Reiniciando.")
                
                if ip not in self.knock_attempts:
                    self.knock_attempts[ip] = []
                
                self.knock_attempts[ip].append(port)
                self.knock_timestamps[ip] = now
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] Knock recibido de {ip} en puerto {port} | Secuencia actual: {self.knock_attempts[ip]}")
                
                # Verificar secuencia
                if self.knock_attempts[ip] == self.knock_ports:
                    print(f"\n{'='*60}")
                    print(f"[knockd] ✓ SECUENCIA CORRECTA de {ip}!")
                    print(f"        Abriendo puerto {self.target_port} para VPN")
                    print(f"{'='*60}\n")
                    
                    self.open_vpn_port()
                    self.knock_attempts[ip] = []  # Reset
                elif len(self.knock_attempts[ip]) >= len(self.knock_ports):
                    # Secuencia incorrecta, reiniciar
                    print(f"[knockd] ✗ Secuencia incorrecta de {ip}. Reiniciando.")
                    self.knock_attempts[ip] = []
                
                conn.close()
            except Exception as e:
                print(f"Error en puerto {port}: {e}")
    
    def open_vpn_port(self):
        """Abre el puerto VPN inmediatamente"""
        if not self.vpn_port_open:
            self.vpn_port_open = True
            t = threading.Thread(target=self._maintain_vpn_port, daemon=True)
            t.start()
    
    def _maintain_vpn_port(self):
        """Mantiene el puerto VPN abierto durante 30 segundos"""
        try:
            self.vpn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.vpn_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.vpn_socket.bind(('127.0.0.1', self.target_port))
            self.vpn_socket.listen(5)
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [VPN] Puerto {self.target_port} ABIERTO ✓")
            
            # Mantener abierto por 30 segundos
            time.sleep(30)
            
            self.vpn_socket.close()
            self.vpn_port_open = False
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [VPN] Puerto {self.target_port} cerrado (timeout 30s)")
            
        except Exception as e:
            print(f"[VPN] Error: {e}")
            self.vpn_port_open = False
    
    def start(self):
        """Inicia todos los listeners"""
        # Thread para cada puerto de knock
        for port in self.knock_ports:
            t = threading.Thread(target=self.listen_knock, args=(port,), daemon=True)
            t.start()
        
        print("\n" + "="*60)
        print("  Servidor de Port Knocking (dummy) iniciado")
        print("="*60)
        print(f"  Puertos de knock: {self.knock_ports}")
        print(f"  Puerto VPN: {self.target_port}")
        print(f"  Timeout de secuencia: {self.SEQUENCE_TIMEOUT}s")
        print("\n  Presiona Ctrl+C para detener")
        print("="*60 + "\n")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nServidor detenido.")

if __name__ == "__main__":
    # Configuración (debe coincidir con config.json)
    KNOCK_PORTS = [7000, 8000]
    VPN_PORT = 1194
    
    server = KnockServer(KNOCK_PORTS, VPN_PORT)
    server.start()
