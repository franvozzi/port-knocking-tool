#!/bin/bash
# Script para migrar de estructura vieja a nueva

echo "=========================================="
echo "  Migración a Estructura Modular"
echo "=========================================="
echo ""

# Crear estructura de carpetas
mkdir -p src/{core,ui/widgets,security,network,monitoring,utils,cli}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p logs
mkdir -p config
mkdir -p resources/icons

# Backup de archivos viejos
echo "Creando backup..."
mkdir -p backup
cp -r src/*.py backup/ 2>/dev/null || true

echo "✓ Estructura de carpetas creada"
echo "✓ Backup realizado en carpeta 'backup/'"
echo ""
echo "Próximos pasos:"
echo "1. Copiar los nuevos archivos modulares a sus carpetas"
echo "2. Probar con: python src/main.py"
echo "3. Si funciona, eliminar backup: rm -rf backup/"
echo ""
echo "=========================================="
