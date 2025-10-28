#!/bin/bash
# find_duplicates.sh

echo "Buscando archivos potencialmente duplicados..."
echo ""

# Buscar archivos Python duplicados por nombre
echo "=== Archivos con mismo nombre en diferentes ubicaciones ==="
find . -name "*.py" -type f | sed 's|.*/||' | sort | uniq -d | while read filename; do
    echo ""
    echo "Archivo: $filename"
    find . -name "$filename" -type f
done

echo ""
echo "=== Archivos sospechosos de ser viejos ==="
# Archivos viejos en src/ que tienen versión modularizada
if [ -f "src/gui_main.py" ] && [ -f "src/ui/gui_main.py" ]; then
    echo "⚠ src/gui_main.py (viejo, usar src/ui/gui_main.py)"
fi

if [ -f "src/configurador_config.py" ] && [ -f "src/cli/configurador_config.py" ]; then
    echo "⚠ src/configurador_config.py (viejo, usar src/cli/configurador_config.py)"
fi

if [ -f "src/importar_ovpn.py" ] && [ -f "src/cli/importar_ovpn.py" ]; then
    echo "⚠ src/importar_ovpn.py (viejo, usar src/cli/importar_ovpn.py)"
fi
