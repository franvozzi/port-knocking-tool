# VPN Port Knocking Tool

[![CI](https://img.shields.io/badge/ci-action-blue.svg)](https://github.com/franvozzi/port-knocking-tool/actions) [![Release](https://img.shields.io/github/v/release/franvozzi/port-knocking-tool)](https://github.com/franvozzi/port-knocking-tool/releases)

Resumen
-------
Herramienta orientada a un MVP que habilita un puerto VPN mediante una secuencia de "port knocking". Esta versión mantiene:

- Interfaz gráfica mínima para disparar la secuencia y gestionar la conexión VPN.
- Motor de port-knocking configurable desde `src/config.json`.
- Manager para orquestar el cliente OpenVPN (usa `profile.ovpn` o `src/profile.ovpn`).
- Utilidades de prueba: servidor dummy `src/test_knockd_server.py` y script E2E `scripts/e2e_test_knockd.py`.

Estado actual
------------
- MVP sin 2FA/TOTP: los módulos de TOTP han sido retirados para simplificar el flujo.
- Tests: suite unitaria e integración disponible; E2E automatizado para validar el flujo.
- CI: ejecutándose en GitHub Actions (probado en Python 3.10 y 3.11).

Requisitos
----------
- Python 3.9+ (recomendado 3.10/3.11)
- Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

Uso rápido
---------

1) Ejecutar la UI (desarrollo):

```bash
python src/gui_main.py
```

2) Levantar el servidor dummy (para probar knocks):

```bash
python src/test_knockd_server.py --config src/config.json --interval 3
```

3) Ejecutar E2E localmente (arranca el servidor y realiza la secuencia):

```bash
python scripts/e2e_test_knockd.py
```

Configuración
-------------
Archivo principal: `src/config.json` — contiene `knock_sequence`, `interval`, `target_ip` y `target_port`.

Pruebas
-------
Ejecuta todas las pruebas con:

```bash
pytest -q
```

Buenas prácticas
---------------
- Formato y lint: `black` y `ruff`/`flake8`.
- Workflow: desarrollar en ramas por feature y abrir PRs.

Cambios recientes
-----------------
- Eliminado soporte 2FA/TOTP para el MVP.
- Corregido problema de duplicación de logs (`src/monitoring/logger.py`).
- Ajuste E2E para usar `sys.executable` y evitar rutas locales en CI.
- Limpieza: archivados y eliminados varios ficheros no referenciados.

Dónde mirar
-----------
- Scripts clave: `scripts/e2e_test_knockd.py`, `src/test_knockd_server.py`, `src/port_knocker.py`.
- Reportes: `reports/unused_report_src.txt`.

Contribuir
---------
Si quieres que añada guías de empaquetado, instrucciones de despliegue o un changelog más detallado, lo redacto y lo comito.

Actualizar la Wiki
------------------
La documentación destinada a la Wiki se encuentra en `docs/wiki/`.

- Regenerar el índice (TOC) localmente:

```bash
python scripts/generate_wiki_toc.py
```

- Publicar manualmente la Wiki (opcional):

```bash
tmpdir=$(mktemp -d)
git clone https://github.com/<owner>/<repo>.wiki.git "$tmpdir"
rsync -av --delete --exclude='.git' docs/wiki/ "$tmpdir/"
cd "$tmpdir"
git add -A
git commit -m "docs(wiki): sync docs/wiki/ -> GitHub Wiki"
git push origin master
rm -rf "$tmpdir"
```

- Automatizar con GitHub Actions

He añadido un workflow (`.github/workflows/wiki-sync.yml`) que se ejecuta en pushes a `main` y realiza dos tareas:

1. Ejecuta `scripts/generate_wiki_toc.py` y, si `docs/wiki/Home.md` cambia, hace commit a `main`.
2. Si el repositorio tiene configurado el secreto `WIKI_PAT` (un Personal Access Token con permiso `repo`), el workflow clona el repositorio Wiki (`<repo>.wiki.git`) y sincroniza `docs/wiki/` con la Wiki pública.

Para habilitar el push automático a la Wiki, añade el secreto `WIKI_PAT` en Settings → Secrets del repositorio con un PAT que tenga permiso `repo`.
