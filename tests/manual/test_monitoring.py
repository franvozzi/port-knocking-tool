import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from monitoring.logger import StructuredLogger
from monitoring.metrics import MetricsCollector

print("=" * 60)
print("  TEST 6: Monitoring (Logger & Metrics)")
print("=" * 60)
print()

# Test Logger
print("[1/3] Testing logger...")
logger = StructuredLogger()
logger.log_info("Test de log INFO")
logger.log_warning("Test de log WARNING")
logger.log_error("Test de log ERROR")
logger.log_connection_attempt("127.0.0.1", True, 1.5)
print("  ✓ Logger funciona")

# Test Metrics
print("\n[2/3] Testing metrics...")
metrics = MetricsCollector("test_metrics.json")
metrics.record_attempt(True, 1.2)
metrics.record_attempt(True, 1.5)
metrics.record_attempt(False, 0.0)
print(f"  ✓ Métricas: {metrics.get_success_rate():.1f}% éxito")

# Test Report
print("\n[3/3] Testing reporte...")
report = metrics.export_report()
print(f"  ✓ Total intentos: {report['total_attempts']}")
print(f"  ✓ Exitosos: {report['successful_connections']}")
print(f"  ✓ Fallidos: {report['failed_attempts']}")

# Cleanup
Path("test_metrics.json").unlink()

print("\n" + "=" * 60)
print("  ✓ TEST MONITORING COMPLETADO")
print("=" * 60)
