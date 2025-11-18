#!/usr/bin/env python3
"""Generador simple de índice para `docs/wiki/Home.md`.

Escanea `docs/wiki/*.md`, obtiene el primer encabezado de nivel 1 o usa el
nombre de archivo como título, y reemplaza la sección "Índice automático"
en `Home.md` (entre marcadores) con la lista actualizada.

Uso:
  python3 scripts/generate_wiki_toc.py

Se puede ejecutar desde la raíz del repositorio.
"""
from pathlib import Path
import re

WIKI_DIR = Path("docs/wiki")
HOME = WIKI_DIR / "Home.md"


def title_from_md(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    # Buscar el primer encabezado de nivel 1 o 2
    m = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    m = re.search(r"^##\s+(.+)$", text, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    return path.stem


def make_toc(entries):
    lines = [
        "## Índice automático",
        "",
        "Accede rápidamente a las páginas principales de la Wiki:",
        "",
    ]
    for name, title in entries:
        lines.append(f"- [{title}]({name})")
    lines.append("")
    lines.append(
        "Si añades nuevas páginas a `docs/wiki/` puedes regenerar este índice automáticamente ejecutando `scripts/generate_wiki_toc.py`."
    )
    return "\n".join(lines)


def replace_index(home_text: str, toc_markdown: str) -> str:
    # Buscamos la sección que inicia con '## Índice automático' y la reemplazamos.
    pattern = re.compile(r"^## Índice automático[\s\S]*?(?=^## |\Z)", flags=re.MULTILINE)
    if pattern.search(home_text):
        new = pattern.sub(toc_markdown + "\n", home_text)
    else:
        # Si no existe, insertamos el TOC antes de la primera ocurrencia de '## ' después del bloque de navegación
        m = re.search(r"(## Navegación[\s\S]*?\n)", home_text)
        if m:
            insert_at = m.end()
            new = home_text[:insert_at] + "\n" + toc_markdown + "\n" + home_text[insert_at:]
        else:
            new = home_text + "\n" + toc_markdown + "\n"
    return new


def main():
    if not WIKI_DIR.exists():
        print("No se encontró el directorio docs/wiki/. Ejecuta desde la raíz del repo.")
        return 2
    md_files = sorted(
        [p for p in WIKI_DIR.glob("*.md") if p.name.lower() != "home.md"],
        key=lambda p: p.name.lower(),
    )
    entries = []
    for p in md_files:
        title = title_from_md(p)
        entries.append((p.name, title))

    toc = make_toc(entries)

    if not HOME.exists():
        print("No existe docs/wiki/Home.md, creando uno mínimo con el índice.")
        HOME.write_text("# Home\n\n" + toc + "\n", encoding="utf-8")
        return 0

    text = HOME.read_text(encoding="utf-8")
    new_text = replace_index(text, toc)
    if new_text != text:
        HOME.write_text(new_text, encoding="utf-8")
        print("Home.md actualizado con el índice automático.")
    else:
        print("Home.md ya está actualizado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
