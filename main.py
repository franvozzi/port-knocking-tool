import socket
import time

class PortKnocker:
    def __init__(self, target_ip: str):
        self.target_ip = target_ip
    
    def tcp_knock(self, port: int, timeout: float = 1.0) -> bool:
        """
        Realiza un knock TCP usando socket
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((self.target_ip, port))
            sock.close()
            return True
        except Exception as e:
            print(f"Error en knock TCP puerto {port}: {e}")
            return False
    
    def udp_knock(self, port: int) -> bool:
        """
        Realiza un knock UDP usando socket
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b'', (self.target_ip, port))
            sock.close()
            return True
        except Exception as e:
            print(f"Error en knock UDP puerto {port}: {e}")
            return False
    
    def execute_sequence(self, knock_sequence: list, interval: float):
        """
        Ejecuta la secuencia de port knocking
        knock_sequence: lista de tuplas (puerto, protocolo)
        """
        print(f"\n{'='*60}")
        print(f"INICIANDO PORT KNOCKING A {self.target_ip}")
        print(f"Total de knocks: {len(knock_sequence)} | Intervalo: {interval}s")
        print(f"{'='*60}\n")
        
        for i, (port, protocol) in enumerate(knock_sequence, 1):
            protocol_upper = protocol.upper()
            print(f"[{i}/{len(knock_sequence)}] Knock {protocol_upper} en puerto {port}...", end=" ")
            
            if protocol.lower() == 'tcp':
                success = self.tcp_knock(port)
            else:
                success = self.udp_knock(port)
            
            if success:
                print("✓")
            else:
                print("✗")
            
            # Esperar entre knocks (excepto el último)
            if i < len(knock_sequence):
                time.sleep(interval)
        
        print(f"\n{'='*60}")
        print("SECUENCIA COMPLETADA - Ahora podés conectarte al servicio")
        print(f"{'='*60}\n")


def main():
    print("\n" + "="*60)
    print("HERRAMIENTA DE PORT KNOCKING - MIKROTIK")
    print("="*60 + "\n")
    
    # 1. Input IP
    target_ip = input("Ingrese la IP del MikroTik: ").strip()
    
    # 2. Cantidad de knocks
    knock_count = int(input("Cantidad de knocks: "))
    
    # 3. Configurar cada knock con su protocolo
    knock_sequence = []
    print(f"\nConfiguración de {knock_count} knocks:")
    print("-" * 60)
    
    for i in range(knock_count):
        print(f"\nKnock #{i+1}:")
        port = int(input(f"  Puerto: "))
        protocol = input(f"  Protocolo (TCP/UDP): ").strip().lower()
        
        while protocol not in ['tcp', 'udp']:
            print("  ⚠ Protocolo inválido. Use TCP o UDP.")
            protocol = input(f"  Protocolo (TCP/UDP): ").strip().lower()
        
        knock_sequence.append((port, protocol))
        print(f"  ✓ Configurado: {protocol.upper()} -> Puerto {port}")
    
    # Tiempo entre knocks
    print()
    interval = float(input("Tiempo entre knocks (segundos): "))
    
    # Mostrar resumen
    print(f"\n{'='*60}")
    print("RESUMEN DE LA SECUENCIA")
    print(f"{'='*60}")
    print(f"Destino: {target_ip}")
    print(f"Intervalo: {interval}s")
    print("\nSecuencia de knocks:")
    for i, (port, protocol) in enumerate(knock_sequence, 1):
        print(f"  {i}. {protocol.upper()} → Puerto {port}")
    print(f"{'='*60}\n")
    
    # Confirmación
    confirmar = input("¿Ejecutar secuencia? (s/n): ").strip().lower()
    
    if confirmar == 's':
        # 4. Ejecutar
        knocker = PortKnocker(target_ip)
        knocker.execute_sequence(knock_sequence, interval)
    else:
        print("\nOperación cancelada.")


if __name__ == "__main__":
    main()
