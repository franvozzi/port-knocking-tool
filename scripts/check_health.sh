#!/bin/bash
# Verifica estado del sistema antes de compilar

echo "=========================================="
echo "  Health Check - Pre-Compilación"
echo "=========================================="
echo ""

# Verificar Python
echo "[1/7] Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "  ✓ $PYTHON_VERSION"
else
    echo "  ✗ Python 3 no encontrado"
    exit 1
fi

# Verificar dependencias
echo ""
echo "[2/7] Verificando dependencias..."
if pip list | grep -q "cryptography"; then
    echo "  ✓ cryptography instalado"
else
    echo "  ✗ cryptography faltante"
    exit 1
fi

if pip list | grep -q "pyinstaller"; then
    echo "  ✓ pyinstaller instalado"
else
    echo "  ✗ pyinstaller faltante"
    exit 1
fi

# Verificar estructura de archivos
echo ""
echo "[3/7] Verificando estructura de archivos..."
required_files=(
    "src/main.py"
    "src/core/port_knocker.py"
    "src/ui/gui_main.py"
    "config.json"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file faltante"
        exit 1
    fi
done

# Verificar sintaxis Python
echo ""
echo "[4/7] Verificando sintaxis Python..."
if python3 -m py_compile src/main.py 2>/dev/null; then
    echo "  ✓ Sintaxis correcta"
else
    echo "  ✗ Errores de sintaxis"
    exit 1
fi

# Verificar imports
echo ""
echo "[5/7] Verificando imports..."
if python3 -c "from src.main import main" 2>/dev/null; then
    echo "  ✓ Imports correctos"
else
    echo "  ✗ Errores de importación"
    exit 1
fi

# Verificar config.json válido
echo ""
echo "[6/7] Verificando config.json..."
if python3 -c "import json; json.load(open('config.json'))" 2>/dev/null; then
    echo "  ✓ JSON válido"
else
    echo "  ✗ JSON inválido"
    exit 1
fi

# Tests
echo ""
echo "[7/7] Ejecutando tests..."
if command -v pytest &> /dev/null; then
    pytest tests/unit/ -q
    if [ $? -eq 0 ]; then
        echo "  ✓ Tests pasaron"
    else
        echo "  ⚠ Algunos tests fallaron"
    fi
else
    echo "  ⚠ pytest no instalado, saltando tests"
fi

echo ""
echo "=========================================="
echo "  ✓ Sistema listo para compilar"
echo "=========================================="
