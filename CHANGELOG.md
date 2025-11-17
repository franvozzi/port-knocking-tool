# Changelog

## v0.1.1 - 2025-11-17

- Limpieza y estabilización del MVP
  - Eliminado soporte 2FA/TOTP para simplificar el flujo MVP.
  - Corregido duplicación de mensajes en logging (`src/monitoring/logger.py`).
  - Ajuste en E2E: `scripts/e2e_test_knockd.py` usa `sys.executable` para compatibilidad CI.
  - Se archivaron y posteriormente eliminaron varios archivos no referenciados detectados por análisis heurístico.
  - Tests: suite unitaria, integración y E2E automatizados en CI; últimos resultados: 35 passed.


## 0.1.0 - (MVP)

- Primera versión mínima pública (MVP) enfocada en port-knocking + VPN.
