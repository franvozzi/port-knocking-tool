import socket
import time
from datetime import datetime
import sys
import json
import os
import errno


class PortKnocker:
    def __init__(self, target_ip: str, verbose: bool = True):
        self.target_ip = target_ip
        self.verbose = verbose
        self.log_history = []
    
    def log(self, message: str, level: str = "INFO"):
        """Registra mensajes con timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.log_history.append(log_entry)
        
        if self.verbose:
            print(log_entry)
    
    def tcp_ping(self, port: int, timeout: float = 2.0, attempts: int = 3) -> dict:
        """
        Verifica conectividad TCP a un puerto específico
        Retorna diccionario con resultados
        """
        results = {
            'port': port,
            'successful': 0,
            'failed': 0,
            'latencies': [],
            'status': 'closed'
        }
        
        for attempt in range(attempts):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            try:
                start_time = time.time()
                result = sock.connect_ex((self.target_ip, port))
                end_time = time.time()
                
                if result == 0:
                    latency = (end_time - start_time) * 1000
                    results['latencies'].append(latency)
                    results['successful'] += 1
                    results['status'] = 'open'
                else:
                    results['failed'] += 1
                    
            except socket.timeout:
                results['failed'] += 1
            except Exception as e:
                results['failed'] += 1
                self.log(f"Error en tcping puerto {port}: {e}", "ERROR")
            finally:
                sock.close()
            
            if attempt < attempts - 1:
                time.sleep(0.5)
        
        return results
    
    def tcp_knock_syn(self, port: int, timeout: float = 0.5) -> bool:
        """
        Realiza un knock TCP enviando solo SYN (primer handshake)
        No completa la conexion - ideal para port knocking
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.setblocking(False)
            
            start_time = time.time()
            
            try:
                # connect en modo non-blocking envia SYN y retorna inmediatamente
                sock.connect((self.target_ip, port))
            except socket.error as e:
                # errno 115 (EINPROGRESS Linux), 36 (macOS), 10035 (Windows) son esperados
                if e.errno not in (errno.EINPROGRESS, 36, 10035):
                    pass
            
            # Cerrar sin completar handshake - solo enviamos SYN
            time.sleep(0.1)
            sock.close()
            
            elapsed = (time.time() - start_time) * 1000
            self.log(f"Knock TCP SYN puerto {port} - Tiempo: {elapsed:.2f}ms", "DEBUG")
            
            return True
        except Exception as e:
            self.log(f"Error en knock TCP SYN puerto {port}: {e}", "ERROR")
            return False
    
    def udp_knock(self, port: int) -> bool:
        """
        Realiza un knock UDP usando socket
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            start_time = time.time()
            sock.sendto(b'KNOCK', (self.target_ip, port))
            
            time.sleep(0.1)
            sock.close()
            
            elapsed = (time.time() - start_time) * 1000
            self.log(f"Knock UDP puerto {port} - Tiempo: {elapsed:.2f}ms", "DEBUG")
            
            return True
        except Exception as e:
            self.log(f"Error en knock UDP puerto {port}: {e}", "ERROR")
            return False
    
    def verify_knock_received(self, target_port: int, check_delays: list = None) -> bool:
        """
        Hace multiples intentos de verificacion con delays progresivos
        para dar tiempo al firewall a procesar la address list
        """
        if check_delays is None:
            check_delays = [2, 5, 10]  # Intentar a los 2s, 5s y 10s
        
        print(f"\n[*] Verificando apertura del puerto {target_port} con delays progresivos...")
        
        for i, delay in enumerate(check_delays, 1):
            print(f"\n[{i}/{len(check_delays)}] Esperando {delay}s antes de verificar...")
            time.sleep(delay)
            
            result = self.tcp_ping(target_port, timeout=2.0, attempts=2)
            
            print(f"{'-'*70}")
            print(f"Verificacion #{i}:")
            print(f"Puerto: {target_port}")
            print(f"Estado: {'[+] ABIERTO' if result['status'] == 'open' else '[-] CERRADO'}")
            print(f"Intentos exitosos: {result['successful']}/{result['successful'] + result['failed']}")
            
            if result['latencies']:
                avg_latency = sum(result['latencies']) / len(result['latencies'])
                print(f"Latencia promedio: {avg_latency:.2f}ms")
            
            print(f"{'-'*70}")
            
            if result['status'] == 'open':
                print(f"\n[SUCCESS] Puerto abierto despues de {delay}s de delay acumulado")
                return True
            else:
                if i < len(check_delays):
                    print(f"[-] Todavia cerrado - continuando con siguiente verificacion...")
        
        return False
    
    def execute_sequence(self, knock_sequence: list, interval: float, target_port: int = None, 
                        progressive_check: bool = True):
        """
        Ejecuta la secuencia de port knocking con verificacion
        knock_sequence: lista de tuplas (puerto, protocolo)
        target_port: puerto que deberia abrirse despues del knocking (opcional)
        progressive_check: usar verificacion progresiva con delays
        """
        print(f"\n{'='*70}")
        print(f"INICIANDO PORT KNOCKING A {self.target_ip}")
        print(f"Knocks: {len(knock_sequence)} | Intervalo: {interval}s")
        print(f"Modo: TCP SYN-only (primer handshake solamente)")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        
        # Verificacion pre-knocking del puerto objetivo si se especifico
        if target_port:
            print(f"[?] Verificando estado inicial del puerto {target_port}...")
            pre_check = self.tcp_ping(target_port, timeout=1.0, attempts=2)
            
            if pre_check['status'] == 'open':
                print(f"[!] ADVERTENCIA: El puerto {target_port} ya esta abierto")
            else:
                print(f"[+] Puerto {target_port} cerrado (esperado)")
            print()
        
        # Ejecutar secuencia de knocking
        print("[>>] Ejecutando secuencia de knocks:\n")
        success_count = 0
        
        for i, (port, protocol) in enumerate(knock_sequence, 1):
            protocol_upper = protocol.upper()
            print(f"[{i}/{len(knock_sequence)}] Knock {protocol_upper} -> Puerto {port}...", end=" ")
            
            if protocol.lower() == 'tcp':
                success = self.tcp_knock_syn(port)
            else:
                success = self.udp_knock(port)
            
            if success:
                print("[+]")
                success_count += 1
            else:
                print("[X] FALLIDO")
            
            if i < len(knock_sequence):
                time.sleep(interval)
        
        print(f"\n{'='*70}")
        print(f"SECUENCIA COMPLETADA: {success_count}/{len(knock_sequence)} knocks exitosos")
        print(f"{'='*70}\n")
        
        # Verificacion post-knocking del puerto objetivo
        if target_port:
            if progressive_check:
                # Verificacion progresiva con multiples delays
                success = self.verify_knock_received(target_port)
                
                print(f"\n{'='*70}")
                if success:
                    print("[SUCCESS] PORT KNOCKING EXITOSO - Puerto accesible")
                    print("La IP fue agregada correctamente a la address list")
                else:
                    print("[FAILED] PORT KNOCKING FALLO - Puerto sigue cerrado")
                    print("\nPosibles causas:")
                    print("  1. Orden incorrecto de reglas en el firewall")
                    print("  2. Interface incorrecta en la regla del MikroTik")
                    print("  3. Puerto de knock incorrecto")
                    print("  4. Regla de connection-state bloqueando antes")
                    print("  5. Timeout de address-list muy corto")
                    print("\nVerifica con: /ip firewall address-list print")
                print(f"{'='*70}\n")
            else:
                # Verificacion simple con delay fijo
                print(f"[*] Esperando 5s que el firewall procese la address list...")
                time.sleep(5)
                
                post_check = self.tcp_ping(target_port, timeout=2.0, attempts=3)
                
                print(f"\n{'-'*70}")
                print("RESULTADO DE VERIFICACION:")
                print(f"{'-'*70}")
                print(f"Puerto: {target_port}")
                print(f"Estado: {'[+] ABIERTO' if post_check['status'] == 'open' else '[-] CERRADO'}")
                print(f"Intentos exitosos: {post_check['successful']}/{post_check['successful'] + post_check['failed']}")
                
                if post_check['latencies']:
                    avg_latency = sum(post_check['latencies']) / len(post_check['latencies'])
                    print(f"Latencia promedio: {avg_latency:.2f}ms")
                
                print(f"{'-'*70}\n")
                
                if post_check['status'] == 'open':
                    print("[SUCCESS] PORT KNOCKING EXITOSO - Puerto accesible")
                else:
                    print("[FAILED] PORT KNOCKING FALLO - Puerto sigue cerrado")
                    print("   Verifica la secuencia y configuracion del servidor")
        else:
            print("[+] Secuencia enviada - Verifica manualmente el acceso al servicio")
        
        print()
    
    def save_log(self, filename: str = None):
        """Guarda el log de operaciones"""
        if not filename:
            filename = f"portknock_{self.target_ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.log_history))
            print(f"[LOG] Log guardado en: {filename}")
        except Exception as e:
            print(f"Error guardando log: {e}")


def validate_ip(ip: str) -> bool:
    """Valida formato de direccion IP"""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            num = int(part)
            if num < 0 or num > 255:
                return False
        return True
    except:
        return False


def validate_port(port: int) -> bool:
    """Valida rango de puerto"""
    return 1 <= port <= 65535


def save_config(config: dict, filename: str = "portknock_config.json"):
    """Guarda configuracion para reutilizar"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        print(f"\n[SAVE] Configuracion guardada en: {filename}")
    except Exception as e:
        print(f"Error guardando configuracion: {e}")


def load_config(filename: str = "portknock_config.json") -> dict:
    """Carga configuracion guardada"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error cargando configuracion: {e}")
    return None


def main():
    print("\n" + "="*70)
    print("HERRAMIENTA DE PORT KNOCKING - MIKROTIK")
    print("Modo: TCP SYN-only (primer handshake)")
    print("="*70 + "\n")
    
    # Opcion de cargar configuracion
    if os.path.exists("portknock_config.json"):
        usar_config = input("Cargar configuracion guardada? (s/n): ").strip().lower()
        if usar_config == 's':
            config = load_config()
            if config:
                print("\n[+] Configuracion cargada")
                print(f"  IP: {config['target_ip']}")
                print(f"  Secuencia: {len(config['knock_sequence'])} knocks")
                
                confirmar = input("\nUsar esta configuracion? (s/n): ").strip().lower()
                if confirmar == 's':
                    prog_check = input("Usar verificacion progresiva? (s/n) [s]: ").strip().lower() or "s"
                    progressive = (prog_check == 's')
                    
                    knocker = PortKnocker(config['target_ip'])
                    knocker.execute_sequence(
                        config['knock_sequence'],
                        config['interval'],
                        config.get('target_port'),
                        progressive_check=progressive
                    )
                    knocker.save_log()
                    return
    
    # Input y validacion de IP
    while True:
        target_ip = input("Ingrese la IP del MikroTik: ").strip()
        if validate_ip(target_ip):
            break
        print("[X] IP invalida. Formato correcto: 192.168.1.1\n")
    
    # Verificar conectividad basica
    print(f"\n[?] Verificando conectividad con {target_ip}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((target_ip, 80))
        sock.close()
        print("[+] Host alcanzable\n")
    except:
        print("[!] Advertencia: No se pudo verificar conectividad\n")
    
    # Cantidad de knocks
    while True:
        try:
            knock_count = int(input("Cantidad de knocks: "))
            if knock_count > 0:
                break
            print("[X] Debe ser mayor a 0\n")
        except ValueError:
            print("[X] Ingrese un numero valido\n")
    
    # Configurar cada knock
    knock_sequence = []
    print(f"\n{'-'*70}")
    print(f"CONFIGURACION DE {knock_count} KNOCKS")
    print(f"{'-'*70}\n")
    
    for i in range(knock_count):
        print(f"Knock #{i+1}:")
        
        while True:
            try:
                port = int(input("  Puerto: "))
                if validate_port(port):
                    break
                print("  [X] Puerto debe estar entre 1-65535")
            except ValueError:
                print("  [X] Ingrese un numero valido")
        
        while True:
            protocol = input("  Protocolo (TCP/UDP): ").strip().lower()
            if protocol in ['tcp', 'udp']:
                break
            print("  [X] Ingrese TCP o UDP")
        
        knock_sequence.append((port, protocol))
        print(f"  [+] {protocol.upper()} -> Puerto {port}\n")
    
    # Tiempo entre knocks
    while True:
        try:
            interval = float(input("Tiempo entre knocks (segundos): "))
            if interval >= 0:
                break
            print("[X] Debe ser mayor o igual a 0\n")
        except ValueError:
            print("[X] Ingrese un numero valido\n")
    
    # Puerto objetivo (opcional)
    print()
    verificar_puerto = input("Verificar apertura de puerto despues del knocking? (s/n): ").strip().lower()
    target_port = None
    progressive_check = False
    
    if verificar_puerto == 's':
        while True:
            try:
                target_port = int(input("Puerto que deberia abrirse (ej: 22 para SSH, 8291 para Winbox): "))
                if validate_port(target_port):
                    break
                print("[X] Puerto debe estar entre 1-65535\n")
            except ValueError:
                print("[X] Ingrese un numero valido\n")
        
        print()
        print("Tipo de verificacion:")
        print("  1. Progresiva con delays (2s, 5s, 10s) - Recomendado")
        print("  2. Simple con delay fijo (5s)")
        tipo_verif = input("Seleccione tipo (1/2) [1]: ").strip() or "1"
        progressive_check = (tipo_verif == "1")
    
    # Resumen
    print(f"\n{'='*70}")
    print("RESUMEN DE LA CONFIGURACION")
    print(f"{'='*70}")
    print(f"Destino: {target_ip}")
    print(f"Intervalo: {interval}s")
    print(f"Modo: TCP SYN-only (primer handshake)")
    if target_port:
        print(f"Puerto objetivo: {target_port}")
        print(f"Verificacion: {'Progresiva (2s, 5s, 10s)' if progressive_check else 'Simple (5s)'}")
    print("\nSecuencia de knocks:")
    for i, (port, protocol) in enumerate(knock_sequence, 1):
        print(f"  {i}. {protocol.upper()} -> Puerto {port}")
    print(f"{'='*70}\n")
    
    # Confirmacion
    confirmar = input("Ejecutar secuencia? (s/n): ").strip().lower()
    
    if confirmar != 's':
        print("\n[X] Operacion cancelada.")
        return
    
    # Guardar configuracion
    guardar = input("Guardar configuracion para uso futuro? (s/n): ").strip().lower()
    if guardar == 's':
        config = {
            'target_ip': target_ip,
            'knock_sequence': knock_sequence,
            'interval': interval,
            'target_port': target_port
        }
        save_config(config)
    
    # Ejecutar
    print()
    knocker = PortKnocker(target_ip, verbose=True)
    knocker.execute_sequence(knock_sequence, interval, target_port, progressive_check)
    
    # Guardar log
    guardar_log = input("Guardar log de operaciones? (s/n): ").strip().lower()
    if guardar_log == 's':
        knocker.save_log()
    
    print("\n[OK] Proceso finalizado\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Operacion interrumpida por el usuario\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}\n")
        sys.exit(1)
