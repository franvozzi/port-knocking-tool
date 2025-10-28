#!/bin/bash
# cleanup.sh - Limpia archivos innecesarios

echo "=========================================="
echo "  LIMPIEZA DE ARCHIVOS REDUNDANTES"
echo "=========================================="
echo ""

# Archivos viejos duplicados
echo "Eliminando archivos viejos duplicados..."
rm -f src/gui_main.py
rm -f src/configurador_config.py
rm -f src/importar_ovpn.py
echo "  ✓ Archivos viejos eliminados"

# Carpetas vacías
echo ""
echo "Eliminando carpetas vacías..."
[ -d "src/api" ] && [ -z "$(ls -A src/api)" ] && rmdir src/api
[ -d "src/integrations" ] && [ -z "$(ls -A src/integrations)" ] && rmdir src/integrations
[ -d "src/ml" ] && [ -z "$(ls -A src/ml)" ] && rmdir src/ml
echo "  ✓ Carpetas vacías eliminadas"

# Cache de Python
echo ""
echo "Eliminando cache de Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
echo "  ✓ Cache eliminado"

# Build artifacts
echo ""
echo "Eliminando build artifacts..."
rm -rf build/
rm -rf dist/
rm -f *.spec
echo "  ✓ Build artifacts eliminados"

# Test temporales
echo ""
echo "Eliminando archivos de test temporales..."
rm -f test_config.json
rm -f test_invalid_config.json
rm -f test_creds.enc
rm -f .test_key
rm -f test_metrics.json
echo "  ✓ Tests temporales eliminados"

# Logs antiguos (opcional)
echo ""
echo "Limpiando logs antiguos..."
find logs/ -name "*.log" -mtime +7 -delete 2>/dev/null
echo "  ✓ Logs antiguos limpiados"

echo ""
echo "=========================================="
echo "  ✓ LIMPIEZA COMPLETADA"
echo "=========================================="
