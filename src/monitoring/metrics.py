import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class MetricsCollector:
    """Recolector de métricas de conexión"""

    def __init__(self, metrics_file: str = "logs/metrics.json"):
        self.metrics_file = Path(metrics_file)
        self.metrics_file.parent.mkdir(exist_ok=True)
        self.metrics = self._load_metrics()

    def _load_metrics(self) -> Dict[str, Any]:
        """Carga métricas existentes"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, "r") as f:
                    return json.load(f)
            except:
                pass

        return {
            "total_attempts": 0,
            "successful_connections": 0,
            "failed_attempts": 0,
            "total_duration": 0.0,
            "average_duration": 0.0,
            "last_updated": None,
        }

    def record_attempt(self, success: bool, duration: float):
        """Registra intento de conexión"""
        self.metrics["total_attempts"] += 1

        if success:
            self.metrics["successful_connections"] += 1
            self.metrics["total_duration"] += duration
            self._update_average()
        else:
            self.metrics["failed_attempts"] += 1

        self.metrics["last_updated"] = datetime.now().isoformat()
        self._save_metrics()

    def _update_average(self):
        """Actualiza duración promedio"""
        if self.metrics["successful_connections"] > 0:
            self.metrics["average_duration"] = (
                self.metrics["total_duration"] / self.metrics["successful_connections"]
            )

    def _save_metrics(self):
        """Guarda métricas"""
        with open(self.metrics_file, "w") as f:
            json.dump(self.metrics, f, indent=2, ensure_ascii=False)

    def get_success_rate(self) -> float:
        """Calcula tasa de éxito"""
        if self.metrics["total_attempts"] == 0:
            return 0.0
        return (self.metrics["successful_connections"] / self.metrics["total_attempts"]) * 100

    def export_report(self) -> Dict[str, Any]:
        """Exporta reporte de métricas"""
        return {**self.metrics, "success_rate": round(self.get_success_rate(), 2)}
