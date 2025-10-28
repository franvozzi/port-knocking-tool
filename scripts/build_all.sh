#!/bin/bash
# Compila para todas las plataformas

echo "=========================================="
echo "  Build Multiplataforma"
echo "=========================================="
echo ""

# Detectar plataforma
OS=$(uname -s)

case "$OS" in
    Darwin)
        echo "Compilando para macOS..."
        pyinstaller --clean --onedir --windowed \
          --name "VPNConnect" \
          --icon="resources/icon.icns" \
          --add-data "config.json:." \
          --add-data "profile.ovpn:." \
          src/main.py
        
        if [ $? -eq 0 ]; then
            echo "✓ Compilación macOS exitosa"
            echo "  Ejecutable: dist/VPNConnect.app"
        else
            echo "✗ Error en compilación"
            exit 1
        fi
        ;;
    
    Linux)
        echo "Compilando para Linux..."
        pyinstaller --clean --onedir --windowed \
          --name "VPNConnect" \
          --add-data "config.json:." \
          --add-data "profile.ovpn:." \
          src/main.py
        
        if [ $? -eq 0 ]; then
            echo "✓ Compilación Linux exitosa"
            echo "  Ejecutable: dist/VPNConnect"
        else
            echo "✗ Error en compilación"
            exit 1
        fi
        ;;
    
    *)
        echo "✗ Plataforma no soportada: $OS"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
