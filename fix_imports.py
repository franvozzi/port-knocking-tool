#!/usr/bin/env python3
"""
Script para corregir imports relativos a absolutos en todo el proyecto
Ubicación: raíz del proyecto (mismo nivel que src/)
"""
from pathlib import Path
import re


def fix_imports(file_path):
    """Corrige imports relativos a absolutos en un archivo"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # Patrones a reemplazar (de más específico a más general)
    replacements = [
        # Imports de 3 niveles arriba (widgets)
        (r"from \.\.\.utils\.", "from src.utils."),
        # Imports de 2 niveles arriba
        (r"from \.\.utils\.", "from src.utils."),
        (r"from \.\.core\.", "from src.core."),
        (r"from \.\.monitoring\.", "from src.monitoring."),
        (r"from \.\.security\.", "from src.security."),
        (r"from \.\.network\.", "from src.network."),
        (r"from \.\.ui\.", "from src.ui."),
        # Imports de 1 nivel arriba (mismo directorio padre)
        (r"from \.widgets\.", "from src.ui.widgets."),
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    """Corrige todos los archivos Python en src/"""
    src_dir = Path("src")

    if not src_dir.exists():
        print("✗ Carpeta 'src/' no encontrada")
        print("Ejecutar desde la raíz del proyecto")
        return 1

    print("=" * 70)
    print("  CORRECCIÓN AUTOMÁTICA DE IMPORTS")
    print("=" * 70)
    print()
    print("Buscando archivos Python en src/...")
    print()

    fixed_files = []
    all_files = list(src_dir.rglob("*.py"))

    for py_file in all_files:
        # Saltar __pycache__
        if "__pycache__" in str(py_file):
            continue

        if fix_imports(py_file):
            fixed_files.append(py_file)
            print(f"  ✓ {py_file}")

    print()
    print("=" * 70)
    if fixed_files:
        print(f"  ✓ {len(fixed_files)} archivo(s) corregido(s)")
        print()
        print("Archivos modificados:")
        for f in fixed_files:
            print(f"  - {f}")
    else:
        print("  ℹ No se encontraron imports relativos para corregir")

    print()
    print("Próximo paso:")
    print("  python3 tests/manual/test_imports.py")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
