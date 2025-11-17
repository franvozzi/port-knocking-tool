#!/usr/bin/env python3
"""
Servidor dummy de port knocking para pruebas locales
Escucha en los puertos configurados y simula apertura de puerto VPN
"""

import socket
import threading
import time
import json
import argparse
from datetime import datetime
from pathlib import Path


class KnockServer:
    def __init__(self, knock_ports, target_port, config_path=None, override_interval=None):
        self.knock_ports = knock_ports
        self.target_port = target_port
        self.knock_attempts = {}
        self.knock_timestamps = {}
        self.vpn_port_open = False
        self.vpn_socket = None

        # Cargar configuración (desde ruta proporcionada o local)
        try:
            if config_path:
                cfg_path = Path(config_path)
            else:
                cfg_path = Path(__file__).parent / "config.json"

            if cfg_path.exists():
                cfg = json.load(open(cfg_path, "r", encoding="utf-8"))
            else:
                cfg = {}
        except Exception:
            cfg = {}

        # Timeout general para expirar secuencias (en segundos)
        self.SEQUENCE_TIMEOUT = float(cfg.get("sequence_timeout", 5))

        # Cálculo de INTERVAL_MAX (más robusto): prioridad
        # 1) override_interval (argumento de línea de comandos)
        # 2) valor explícito en config.json -> 'interval'
        # 3) si no existe, se calcula como SEQUENCE_TIMEOUT / (n_steps)
        #    para distribuir el timeout entre los pasos de la secuencia
        if override_interval is not None:
            self.INTERVAL_MAX = float(override_interval)
            self._interval_source = f"override ({self.INTERVAL_MAX}s)"
        elif "interval" in cfg:
            self.INTERVAL_MAX = float(cfg.get("interval"))
            self._interval_source = "config.json"
        else:
            steps = max(1, (len(self.knock_ports) - 1))
            # evitar división por cero; si sólo hay un puerto, permitimos SEQUENCE_TIMEOUT
            if steps == 0:
                allowed = self.SEQUENCE_TIMEOUT
            else:
                allowed = float(self.SEQUENCE_TIMEOUT) / steps
            self.INTERVAL_MAX = allowed
            self._interval_source = f"computed (SEQUENCE_TIMEOUT/{steps} = {self.INTERVAL_MAX}s)"

    def listen_knock(self, port):
        """Escucha intentos de conexión en un puerto de knock"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", port))
        sock.listen(5)

        print(f"[knockd] Escuchando knocks en puerto {port}")

        while True:
            try:
                conn, addr = sock.accept()
                ip = addr[0]
                now = time.time()

                # Limpiar knocks antiguos (timeout)
                if ip in self.knock_timestamps:
                    # Si ha pasado demasiado tiempo desde el último knock, reiniciar
                    if now - self.knock_timestamps[ip] > self.SEQUENCE_TIMEOUT:
                        self.knock_attempts[ip] = []
                        print(
                            f"[knockd] Secuencia de {ip} expiró por timeout general. Reiniciando."
                        )

                    # Validación por intervalo entre knocks: si el delta supera
                    # el intervalo configurado, reiniciamos la secuencia.
                    time_delta = now - self.knock_timestamps[ip]
                    if time_delta > self.INTERVAL_MAX:
                        self.knock_attempts[ip] = []
                        print(
                            f"[knockd] Intervalo entre knocks ({time_delta:.3f}s) excede interval_max ({self.INTERVAL_MAX}s). Reiniciando secuencia de {ip}."
                        )

                if ip not in self.knock_attempts:
                    self.knock_attempts[ip] = []

                self.knock_attempts[ip].append(port)
                self.knock_timestamps[ip] = now

                timestamp = datetime.now().strftime("%H:%M:%S")
                print(
                    f"[{timestamp}] Knock recibido de {ip} en puerto {port} | Secuencia actual: {self.knock_attempts[ip]}"
                )

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
            self.vpn_socket.bind(("127.0.0.1", self.target_port))
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

        print("\n" + "=" * 60)
        print("  Servidor de Port Knocking (dummy) iniciado")
        print("=" * 60)
        print(f"  Puertos de knock: {self.knock_ports}")
        print(f"  Puerto VPN: {self.target_port}")
        print(f"  Timeout de secuencia: {self.SEQUENCE_TIMEOUT}s")
        print(f"  Intervalo máximo permitido entre knocks (interval_max): {self.INTERVAL_MAX}s")
        print(f"  Interval source: {getattr(self, '_interval_source', 'unknown')}")
        print("\n  Presiona Ctrl+C para detener")
        print("=" * 60 + "\n")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nServidor detenido.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Servidor dummy de port knocking para pruebas locales"
    )
    parser.add_argument("--config", "-c", help="Ruta al config.json a usar (opcional)")
    parser.add_argument("--interval", "-i", type=float, help="Forzar interval_max (segundos)")
    parser.add_argument(
        "--ports", "-p", nargs="+", type=int, help="Lista de puertos knock (ej: -p 7000 8000)"
    )
    parser.add_argument("--vpn-port", "-v", type=int, default=1194, help="Puerto VPN a abrir")
    args = parser.parse_args()

    # Configuración (por defecto coincide con config.json del repo)
    KNOCK_PORTS = args.ports if args.ports else [7000, 8000]
    VPN_PORT = args.vpn_port

    server = KnockServer(
        KNOCK_PORTS, VPN_PORT, config_path=args.config, override_interval=args.interval
    )
    server.start()
