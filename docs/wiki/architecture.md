# Arquitectura (detallada)

Diagrama y despiece por módulos. Resumen:
- UI: `src/ui` (Tkinter)
- Core: `src/core` (PortKnocker, VPNManager, ConfigManager)
- Network: `src/network` (diagnostics, circuit_breaker)
- Security: `src/security` (crypto, totp stubs)
- Monitoring: `src/monitoring` (logger, metrics)

Ver `docs/ARCHITECTURE.md` para el contenido original y diagramas ASCII.
