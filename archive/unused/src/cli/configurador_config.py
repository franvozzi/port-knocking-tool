import json
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.validators import ConfigValidator

def main():
    print("=" * 60)
    print("  Configurador de config.json - VPN Port Knocking")
    print("=" * 60)
    print()
    
    # IP del servidor
    ip = input("IP pública del servidor: ").strip()
    
    # Secuencia de knocks
    knocks = []
    print("\nIngrese secuencia de knocks (Enter vacío para terminar):")
    while True:
        port = input("  Puerto: ").strip()
        if not port:
            break
        
        try:
            port = int(port)
            if not (1 <= port <= 65535):
                print("  ⚠ Puerto debe estar entre 1 y 65535")
                continue
        except ValueError:
            print("  ⚠ Puerto inválido")
            continue
        
        proto = input("  Protocolo (tcp/udp): ").strip().lower()
        if proto not in ['tcp', 'udp']:
            print("  ⚠ Protocolo debe ser 'tcp' o 'udp'")
            continue
        
        knocks.append([port, proto])
    
    if not knocks:
        print("\n✗ Debe ingresar al menos un knock")
        sys.exit(1)
    
    # Intervalo
    interval_str = input("\nIntervalo entre knocks en segundos (ej: 0.5): ").strip()
    try:
        interval = float(interval_str or "0.5")
        if not (0.1 <= interval <= 5.0):
            print("⚠ Intervalo recomendado: 0.1 - 5.0 segundos. Usando 0.5")
            interval = 0.5
    except ValueError:
        print("⚠ Valor inválido. Usando 0.5 segundos")
        interval = 0.5
    
    # Puerto final
    target_port_str = input("Puerto final a habilitar (ej: 1194): ").strip()
    try:
        target_port = int(target_port_str or "1194")
        if not (1 <= target_port <= 65535):
            print("⚠ Puerto inválido. Usando 1194")
            target_port = 1194
    except ValueError:
        print("⚠ Valor inválido. Usando 1194")
        target_port = 1194
    
    # Crear configuración
    config = {
        "target_ip": ip,
        "knock_sequence": knocks,
        "interval": interval,
        "target_port": target_port
    }
    
    # Validar
    validator = ConfigValidator()
    if not validator.validate(config):
        print("\n✗ Configuración inválida:")
        for error in validator.errors:
            print(f"  - {error}")
        sys.exit(1)
    
    # Guardar
    output_file = "config.json"
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Archivo {output_file} guardado correctamente.")
    print("\nContenido:")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Operación cancelada por el usuario.")
        sys.exit(1)
