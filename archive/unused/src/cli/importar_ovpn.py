import shutil
import sys
from pathlib import Path

def buscar_archivo_ovpn():
    """Busca archivos .ovpn en la carpeta actual"""
    archivos_ovpn = list(Path.cwd().glob("*.ovpn"))
    
    if not archivos_ovpn:
        return None
    
    if len(archivos_ovpn) == 1:
        return archivos_ovpn[0]
    
    # Múltiples archivos
    print(f"Se encontraron {len(archivos_ovpn)} archivos .ovpn:")
    for i, archivo in enumerate(archivos_ovpn, 1):
        print(f"  {i}. {archivo.name}")
    
    while True:
        try:
            seleccion = input("\nSeleccione el archivo a usar (número): ").strip()
            idx = int(seleccion) - 1
            if 0 <= idx < len(archivos_ovpn):
                return archivos_ovpn[idx]
            print("✗ Opción inválida. Intente nuevamente.")
        except ValueError:
            print("✗ Debe ingresar un número.")
        except KeyboardInterrupt:
            print("\n\n✗ Operación cancelada.")
            sys.exit(1)

def solicitar_y_copiar_archivo():
    """Solicita ruta y copia archivo"""
    print("\n✗ No se encontró ningún archivo .ovpn en la carpeta actual.")
    print("\nIngrese la ruta del archivo .ovpn que desea importar:")
    
    while True:
        ruta = input("Ruta del archivo .ovpn (o 'q' para salir): ").strip()
        
        if ruta.lower() == 'q':
            print("\n✗ Operación cancelada.")
            sys.exit(0)
        
        archivo = Path(ruta).expanduser().resolve()
        
        if not archivo.exists():
            print(f"✗ El archivo '{archivo}' no existe. Intente nuevamente.")
            continue
        
        if not archivo.is_file():
            print(f"✗ '{archivo}' no es un archivo. Intente nuevamente.")
            continue
        
        if archivo.suffix.lower() != '.ovpn':
            print("⚠ Advertencia: El archivo no tiene extensión .ovpn")
            confirmar = input("  ¿Continuar de todos modos? (s/n): ").strip().lower()
            if confirmar != 's':
                continue
        
        try:
            destino = Path.cwd() / archivo.name
            shutil.copy2(archivo, destino)
            print(f"\n✓ Archivo copiado exitosamente:")
            print(f"  De: {archivo}")
            print(f"  A: {destino}")
            return destino
        except Exception as e:
            print(f"✗ Error al copiar archivo: {e}")
            continue

def renombrar_a_profile(archivo_ovpn):
    """Renombra a profile.ovpn"""
    if archivo_ovpn.name == "profile.ovpn":
        print(f"\n✓ El archivo ya se llama 'profile.ovpn'")
        return True
    
    destino = Path.cwd() / "profile.ovpn"
    
    if destino.exists():
        print(f"\n⚠ El archivo 'profile.ovpn' ya existe.")
        sobrescribir = input("  ¿Sobrescribir? (s/n): ").strip().lower()
        if sobrescribir != 's':
            print("  Manteniendo profile.ovpn existente.")
            return True
    
    try:
        archivo_ovpn.rename(destino)
        print(f"\n✓ Archivo renombrado a 'profile.ovpn'")
        return True
    except Exception as e:
        print(f"✗ Error al renombrar: {e}")
        return False

def crear_credenciales():
    """Crea archivo de credenciales"""
    print("\n¿Desea crear archivo de credenciales (credentials.txt)?")
    print("  (Permite autenticación automática)")
    
    opcion = input("Crear credentials.txt? (s/n): ").strip().lower()
    
    if opcion != 's':
        print("  Omitiendo creación de credenciales.")
        return False
    
    usuario = input("\nUsuario VPN: ").strip()
    if not usuario:
        print("✗ El usuario no puede estar vacío.")
        return False
    
    clave = input("Clave VPN: ").strip()
    if not clave:
        print("✗ La clave no puede estar vacía.")
        return False
    
    try:
        with open("credentials.txt", "w", encoding='utf-8') as f:
            f.write(f"{usuario}\n{clave}\n")
        
        print("\n✓ Archivo credentials.txt creado exitosamente.")
        print("  IMPORTANTE: Contiene credenciales sensibles.")
        return True
    except Exception as e:
        print(f"✗ Error al crear credentials.txt: {e}")
        return False

def main():
    print("=" * 60)
    print("  Configurador de Perfil OpenVPN - VPN Corporativa")
    print("=" * 60)
    
    # Paso 1: Buscar o solicitar archivo
    print("\nPaso 1: Importar archivo .ovpn")
    print("-" * 60)
    
    archivo_ovpn = buscar_archivo_ovpn()
    
    if archivo_ovpn:
        print(f"✓ Archivo encontrado: {archivo_ovpn.name}")
    else:
        archivo_ovpn = solicitar_y_copiar_archivo()
    
    # Paso 2: Renombrar
    if not renombrar_a_profile(archivo_ovpn):
        sys.exit(1)
    
    # Paso 3: Credenciales
    print("\nPaso 2: Configurar credenciales")
    print("-" * 60)
    crear_credenciales()
    
    # Resumen
    print("\n" + "=" * 60)
    print("  Resumen de archivos configurados:")
    print("=" * 60)
    
    archivos = []
    if Path("profile.ovpn").exists():
        archivos.append(("profile.ovpn", Path("profile.ovpn").stat().st_size))
    if Path("credentials.txt").exists():
        archivos.append(("credentials.txt", Path("credentials.txt").stat().st_size))
    
    for nombre, tamanio in archivos:
        print(f"  ✓ {nombre} ({tamanio} bytes)")
    
    print("\n✓ Configuración completada exitosamente.")
    print("\nPróximos pasos:")
    print("  1. Ejecutar 'python configurador_config.py'")
    print("  2. Compilar el ejecutable con PyInstaller")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Operación cancelada por el usuario.")
        sys.exit(1)
