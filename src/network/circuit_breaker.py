import time
from enum import Enum
from typing import Callable, Any


class CircuitState(Enum):
    """Estados del circuit breaker"""

    CLOSED = "closed"  # Normal, todo funciona
    OPEN = "open"  # Circuito abierto, no intentar
    HALF_OPEN = "half_open"  # Probando si se recuperó


class CircuitBreaker:
    """Implementación de Circuit Breaker pattern"""

    def __init__(self, failure_threshold: int = 3, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Ejecuta función con protección de circuit breaker"""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                self.failure_count = 0
            else:
                raise Exception(f"Circuit breaker is OPEN. Wait {self.timeout}s before retry.")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e

    def on_success(self):
        """Llamado cuando operación es exitosa"""
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def on_failure(self):
        """Llamado cuando operación falla"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def reset(self):
        """Resetea circuit breaker"""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None
