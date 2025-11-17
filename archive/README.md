# Archivos archivados

Esta carpeta contiene archivos que fueron movidos desde `src/` a `archive/unused/src/` como parte de una limpieza segura y reversible.

Motivo:
- Los archivos fueron identificados por el analizador heurístico `tools/find_unused_src.py` como candidatos a no usados. Se trasladaron a `archive/unused/` para revisión manual antes de una eliminación definitiva.

Listado de archivos movidos:
- `archive/unused/src/ui/themes.py`  — Estilos/temas de la UI.
- `archive/unused/src/security/totp_manager.py` — Gestor TOTP (marcado como retirado para MVP).
- `archive/unused/src/network/mikrotik_api_client.py` — Cliente API MikroTik (no referenciado en código actual).
- `archive/unused/src/cli/importar_ovpn.py` — CLI para importar archivos OVPN.
- `archive/unused/src/cli/configurador_config.py` — CLI para configurar el `config.json`.

Notas:
- Estos archivos están disponibles en la historia Git y se pueden restaurar si es necesario.
- Recomendación: dejar en `archive/` durante al menos una semana y luego, si no hay dependencia, eliminar definitivamente.

Creado por el operador de limpieza automático.
