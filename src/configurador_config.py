import json

def main():
    print("=== Configurador de config.json para Port Knocking ===")
    ip = input("IP pública del servidor: ").strip()
    
    knocks = []
    print("\nIngrese secuencia de knocks (Enter vacío para terminar):")
    while True:
        port = input("  Puerto: ").strip()
        if not port:
            break
        proto = input("  Protocolo (tcp/udp): ").strip().lower()
        knocks.append([int(port), proto])
    
    interval = float(input("\nIntervalo entre knocks en segundos (ej: 0.5): ").strip() or "0.5")
    target_port = int(input("Puerto final a habilitar (ej: 1194): ").strip() or "1194")

    config = {
        "target_ip": ip,
        "knock_sequence": knocks,
        "interval": interval,
        "target_port": target_port
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("\n✓ Archivo config.json guardado correctamente.")

if __name__ == "__main__":
    main()
