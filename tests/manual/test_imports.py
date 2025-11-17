#!/usr/bin/env python3
"""
Test manual de imports - Refactorizado
Verifica que todos los módulos se puedan importar correctamente
"""
import sys
from pathlib import Path
from typing import List

# Agregar src al path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


class ImportTest:
    """Clase para ejecutar tests de imports"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def test_import(self, module_name: str, imports: List[str]) -> bool:
        """
        Prueba importar módulos específicos
        
        Args:
            module_name: Nombre del módulo a importar
            imports: Lista de nombres a importar del módulo
            
        Returns:
            True si exitoso, False si falló
        """
        try:
            # Importar dinámicamente
            module = __import__(module_name, fromlist=imports)
            
            # Verificar que cada import existe
            for imp in imports:
                if not hasattr(module, imp):
                    raise AttributeError(f"{imp} no encontrado en {module_name}")
            
            return True
            
        except Exception as e:
            self.results.append({
                'module': module_name,
                'imports': imports,
                'error': str(e),
                'success': False
            })
            return False
    
    def run_test(self, test_name: str, module_name: str, imports: List[str]) -> None:
        """Ejecuta un test individual"""
        print(f"{test_name}...")
        
        if self.test_import(module_name, imports):
            self.passed += 1
            self.results.append({
                'module': module_name,
                'imports': imports,
                'success': True
            })
            
            # Mensaje especial para utils con version
            if module_name == "utils.constants":
                module = __import__("utils.constants", fromlist=["VERSION"])
                VERSION = getattr(module, "VERSION", "N/A")
                print(f"  ✓ {test_name} OK (Version: {VERSION})")
            else:
                print(f"  ✓ {test_name} OK")
        else:
            self.failed += 1
            error = self.results[-1]['error']
            print(f"  ✗ Error en {test_name}: {error}")
    
    def print_summary(self):
        """Imprime resumen de resultados"""
        print("\n" + "=" * 70)
        print(f"  Resultado: {self.passed}/{self.passed + self.failed} tests pasaron")
        print("=" * 70)
        
        if self.failed == 0:
            print("  ✓ TODOS LOS IMPORTS CORRECTOS")
            return 0
        else:
            print("  ✗ HAY ERRORES EN IMPORTS")
            print("\nDetalles de errores:")
            for result in self.results:
                if not result['success']:
                    print(f"\n  Módulo: {result['module']}")
                    print(f"  Error: {result['error']}")
            return 1


def main():
    """Función principal"""
    print("=" * 70)
    print("  TEST 1: Verificación de Imports (Refactorizado)")
    print("=" * 70)
    print()
    
    tester = ImportTest()
    
    # Definir tests a ejecutar
    tests = [
        ("Utils - Exceptions", "utils.exceptions", 
         ["VPNToolError", "ConfigurationError", "NetworkError", "PortKnockingError"]),
        
        ("Utils - Validators", "utils.validators", 
         ["ConfigValidator"]),
        
        ("Utils - Constants", "utils.constants", 
         ["VERSION", "COLORS", "STATUS_MESSAGES"]),
        
        ("Core - ConfigManager", "core.config_manager", 
         ["ConfigManager"]),
        
        ("Core - PortKnocker", "core.port_knocker", 
         ["PortKnocker"]),
        
        ("Core - VPNManager", "core.vpn_manager", 
         ["VPNManager", "get_vpn_manager"]),
        
        ("Security - Crypto", "security.crypto", 
         ["CredentialsEncryptor"]),
        
        ("Network - Diagnostics", "network.diagnostics", 
         ["NetworkDiagnostics"]),
        
        ("Network - CircuitBreaker", "network.circuit_breaker", 
         ["CircuitBreaker", "CircuitState"]),
        
        ("Monitoring - Logger", "monitoring.logger", 
         ["StructuredLogger"]),
        
        ("Monitoring - Metrics", "monitoring.metrics", 
         ["MetricsCollector"]),
        
        ("UI - Widgets StatusBar", "ui.widgets.status_bar", 
         ["StatusBar"]),
        
        ("UI - Widgets ProgressBar", "ui.widgets.progress_bar", 
         ["ConnectionProgress"]),
        
        ("UI - Themes", "ui.themes", 
         ["ThemeManager", "THEMES"]),
        
        ("UI - Main GUI", "ui.gui_main", 
         ["VPNConnectGUI"]),
        
        ("Main Entry Point", "main", 
         ["main"]),
    ]
    
    # Ejecutar tests
    for i, (name, module, imports) in enumerate(tests, 1):
        print(f"[{i}/{len(tests)}] Testing {name}...")
        tester.run_test(name, module, imports)
        print()
    
    # Mostrar resumen
    return tester.print_summary()


if __name__ == "__main__":
    sys.exit(main())
