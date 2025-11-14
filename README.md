# VPN Port Knocking Tool — Resumen y Guía Rápida

Versión: MVP (sin 2FA/TOTP)

Quick Start (Usuario)
- Si tienes el ejecutable empaquetado: abre la aplicación `VPNConnect` desde tu sistema.
- En desarrollo o para probar localmente: activa el entorno virtual y ejecuta `python src/gui_main.py`.

Descripción
- Herramienta para abrir un puerto VPN mediante secuencia de "port knocking" y conectar un cliente OpenVPN.
- Incluye: UI (GUI), port-knocker, manager para OpenVPN y scripts de pruebas (E2E).

Requisitos
- Python 3.9+
- Dependencias: `pip install -r requirements.txt` (y opcionalmente `-r requirements-dev.txt` para desarrollo)

Quick start (desarrollador)
1. Clonar repo y crear virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Ejecutar GUI (modo desarrollo)

```bash
python src/gui_main.py
```

3. Ejecutar servidor de prueba (dummy) que valida la secuencia

```bash
python src/test_knockd_server.py --config src/config.json --interval 3
```

4. Ejecutar E2E (script de pruebas que arranca server y realiza knocks)

```bash
python scripts/e2e_test_knockd.py
```

Archivo de configuración
- `src/config.json` contiene:
  - `target_ip`: IP pública del servidor
  - `knock_sequence`: lista de pares `[port, "tcp"|"udp"]`
  - `interval`: valor (seg) máximo entre knocks aceptado por el servidor dummy
  - `target_port`: puerto final que se habilita (ej. 1194)

Notas importantes
- 2FA/TOTP: el soporte para 2FA/TOTP fue removido para esta versión MVP. Los módulos relacionados fueron eliminados o sustituidos por stubs (ej. `src/security/totp_manager.py`).
- Logger: se corrigió la duplicación de mensajes (handler deduplication) en `src/monitoring/logger.py`.

Pruebas
- Unit + Integration: `pytest` desde la raíz del repo

```bash
pytest -q
```

- E2E: ejecutar `scripts/e2e_test_knockd.py` (requiere `python` y permisos de red locales)

Desarrollo y Contribución
- Sugerido: usar `pre-commit`, `black` y `flake8` para consistencia. Puedo añadir configuración si quieres.
- Workflow: crear rama por feature, abrir PR para revisión.

Análisis de archivos sin uso
- Se generó un primer reporte heurístico en `reports/unused_report.*`. El análisis incluye muchos ficheros del entorno virtual (`.venv`) y paquetes instalados — debemos excluir `.venv` y otros directorios para obtener candidatos más relevantes.

Siguientes pasos sugeridos
1. Revisar `reports/unused_report.txt` y marcar archivos que se quieran inspeccionar manualmente.
2. Re-ejecutar el analizador excluyendo `.venv` y otros paths irrelevantes (p. ej. `vpn_port_knocking_tool.egg-info`).
3. Preparar branch y commits para eliminar/archivar archivos aprobados tras revisión.

Contacto
- Para continuar: dime si quieres que aplique el `README` directamente a `README.md`, que cree una rama y commitee los cambios, o que haga una nueva pasada al analizador filtrando `.venv` y mostrando sólo `src/`.
