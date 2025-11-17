#!/usr/bin/env python3
"""
Herramienta heurística para detectar módulos/archivos Python sin referencias estáticas.
Genera `reports/unused_report.json` y `reports/unused_report.txt`.

Limitaciones: análisis estático (no detecta imports dinámicos ni usos por subprocess).
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
EXCLUDE_DIRS = {
    "tests",
    "dummies",
    "manual_tests",
    "scripts",
    "docs",
    "vpn_port_knocking_tool.egg-info",
}
REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)


def iter_py_files(base: Path):
    for p in base.rglob("*.py"):
        # skip files in excluded top-level dirs
        parts = p.relative_to(ROOT).parts
        if parts[0] in EXCLUDE_DIRS:
            continue
        yield p


def module_name_from_path(p: Path):
    # compute module name relative to src
    try:
        rel = p.relative_to(SRC)
    except Exception:
        rel = p.relative_to(ROOT)
    parts = list(rel.with_suffix("").parts)
    # drop __init__ at end
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def parse_imports(p: Path):
    imports = set()
    try:
        src = p.read_text(encoding="utf-8")
    except Exception:
        return imports
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module
            if mod is None:
                continue
            # record module and module.name for each alias
            imports.add(mod)
            for n in node.names:
                if n.name == "*":
                    continue
                imports.add(f"{mod}.{n.name}")
    return imports


def main():
    files = []
    modules = {}  # module_name -> path
    imports_map = {}  # path -> set(imported module names)

    for p in iter_py_files(ROOT):
        files.append(p)
        m = module_name_from_path(p)
        modules[m] = p

    # parse imports per file
    for p in files:
        imports_map[str(p)] = parse_imports(p)

    # build reverse map: for each module, who imports it?
    imported_by = {m: set() for m in modules}

    for importer_path, imports in imports_map.items():
        for imp in imports:
            # heuristic matching: if any module name startswith imp or imp startswith module
            for m in list(modules.keys()):
                if m == "":
                    continue
                if m == imp or m.startswith(imp + ".") or imp.startswith(m + "."):
                    imported_by[m].add(importer_path)
                else:
                    # also match by tail name: e.g., import core -> core.config_manager
                    tail = m.split(".")[-1]
                    if imp == tail:
                        imported_by[m].add(importer_path)

    # entry points and explicit keep list
    entry_files = {
        str(SRC / "main.py"),
        str(SRC / "server" / "main.py"),
        str(SRC / "server_knock.py"),
        str(SRC / "ui" / "gui_main.py"),
    }
    keep_modules = set()
    for m, p in modules.items():
        if str(p) in entry_files:
            keep_modules.add(m)

    # gather candidates: modules with zero importers and not in keep_modules and not __init__ only packages
    candidates = []
    for m, p in modules.items():
        # skip package-only __init__ handled earlier by module_name_from_path
        if m in keep_modules:
            continue
        importers = imported_by.get(m, set())
        if not importers:
            # skip tests and scripts in src/ that are intended
            rel = p.relative_to(ROOT)
            if rel.parts[0] in EXCLUDE_DIRS:
                continue
            candidates.append({"module": m, "path": str(p), "reason": "no_static_imports_found"})

    report = {
        "root": str(ROOT),
        "scanned_files_count": len(files),
        "modules_count": len(modules),
        "candidates_count": len(candidates),
        "candidates": candidates,
    }

    (REPORT_DIR / "unused_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # human friendly report
    lines = []
    lines.append(f"Root: {ROOT}")
    lines.append(f"Scanned files: {len(files)}")
    lines.append(f"Modules: {len(modules)}")
    lines.append(f"Candidates (no static imports): {len(candidates)}")
    lines.append("")
    if candidates:
        lines.append("Posibles archivos sin uso (revisar manualmente):")
        for c in candidates:
            lines.append(f" - {c['path']}  ({c['module']})")
    else:
        lines.append("No se detectaron candidatos claros a archivos sin uso.")

    (REPORT_DIR / "unused_report.txt").write_text("\n".join(lines), encoding="utf-8")
    print(
        f"Reporte generado: {REPORT_DIR / 'unused_report.json'} and {REPORT_DIR / 'unused_report.txt'}"
    )


if __name__ == "__main__":
    main()
