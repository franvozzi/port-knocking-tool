#!/usr/bin/env python3
"""
Fix definitivo de imports - Convierte TODO a imports sin prefijo src
"""
from pathlib import Path
import re

def fix_file(file_path):
    """Arregla imports en un archivo"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Remover TODOS los prefijos src.
    patterns = [
        # Imports absolutos con src
        (r'from src\.utils\.', 'from utils.'),
        (r'from src\.core\.', 'from core.'),
        (r'from src\.monitoring\.', 'from monitoring.'),
        (r'from src\.security\.', 'from security.'),
        (r'from src\.network\.', 'from network.'),
        (r'from src\.ui\.widgets\.', 'from ui.widgets.'),
        (r'from src\.ui\.', 'from ui.'),
        
        # Imports relativos (de . a nada)
        (r'from \.\.\.utils\.', 'from utils.'),
        (r'from \.\.utils\.', 'from utils.'),
        (r'from \.\.core\.', 'from core.'),
        (r'from \.\.monitoring\.', 'from monitoring.'),
        (r'from \.\.security\.', 'from security.'),
        (r'from \.\.network\.', 'from network.'),
        (r'from \.\.ui\.', 'from ui.'),
        (r'from \.widgets\.', 'from ui.widgets.'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

print("=" * 70)
print("  CORRECCIÓN DEFINITIVA DE IMPORTS")
print("=" * 70)
print()

src_dir = Path("src")
fixed = []

for py_file in src_dir.rglob("*.py"):
    if '__pycache__' in str(py_file):
        continue
    
    if fix_file(py_file):
        fixed.append(py_file)
        print(f"✓ {py_file}")

print()
print("=" * 70)
print(f"  ✓ {len(fixed)} archivos corregidos")
print("=" * 70)
print()
print("Verificar con:")
print("  python3 tests/manual/test_imports.py")
print()
