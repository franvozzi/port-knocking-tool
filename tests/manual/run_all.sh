#!/bin/bash

echo "=========================================="
echo "  EJECUTANDO TODOS LOS TESTS"
echo "=========================================="
echo ""

tests=(
    "test_imports.py"
    "test_validators.py"
    "test_config_manager.py"
    "test_crypto.py"
    "test_diagnostics.py"
    "test_monitoring.py"
)

passed=0
failed=0

for test in "${tests[@]}"; do
    echo ""
    echo "▶ Ejecutando $test..."
    echo "----------------------------------------"
    
    if python3 "tests/manual/$test"; then
        ((passed++))
        echo "✓ $test PASÓ"
    else
        ((failed++))
        echo "✗ $test FALLÓ"
    fi
done

echo ""
echo "=========================================="
echo "  RESUMEN FINAL"
echo "=========================================="
echo "  Pasados: $passed/${#tests[@]}"
echo "  Fallidos: $failed"
echo ""

if [ $failed -eq 0 ]; then
    echo "  🎉 TODOS LOS TESTS PASARON"
    echo "  ✓ Sistema listo para compilar"
else
    echo "  ⚠ HAY TESTS FALLIDOS"
fi

echo "=========================================="
