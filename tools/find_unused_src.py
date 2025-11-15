#!/usr/bin/env python3
"""
Versión filtrada del analizador: escanea sólo `src/`, excluye `.venv` y `*.egg-info`.
Genera `reports/unused_report_src.json` y `reports/unused_report_src.txt`.
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
EXCLUDE_DIRS = {'.venv', 'vpn_port_knocking_tool.egg-info'}
REPORT_DIR = ROOT / 'reports'
REPORT_DIR.mkdir(exist_ok=True)


def iter_py_files(base: Path):
    for p in base.rglob('*.py'):
        parts = p.relative_to(ROOT).parts
        if parts[0] in EXCLUDE_DIRS:
            continue
        yield p


def module_name_from_path(p: Path):
    rel = p.relative_to(SRC)
    parts = list(rel.with_suffix('').parts)
    if parts and parts[-1] == '__init__':
        parts = parts[:-1]
    return '.'.join(parts)


def parse_imports(p: Path):
    imports = set()
    try:
        src = p.read_text(encoding='utf-8')
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
            imports.add(mod)
            for n in node.names:
                if n.name == '*':
                    continue
                imports.add(f"{mod}.{n.name}")
    return imports


def main():
    files = []
    modules = {}
    imports_map = {}

    if not SRC.exists():
        print(f"No existe {SRC}; abortando.")
        return

    for p in iter_py_files(SRC):
        files.append(p)
        m = module_name_from_path(p)
        modules[m] = p

    for p in files:
        imports_map[str(p)] = parse_imports(p)

    imported_by = {m: set() for m in modules}

    for importer_path, imports in imports_map.items():
        for imp in imports:
            for m in list(modules.keys()):
                if not m:
                    continue
                if m == imp or m.startswith(imp + '.') or imp.startswith(m + '.'):
                    imported_by[m].add(importer_path)
                else:
                    tail = m.split('.')[-1]
                    if imp == tail:
                        imported_by[m].add(importer_path)

    # entry points to keep
    entry_files = {str(SRC / 'main.py'), str(SRC / 'server' / 'main.py'), str(SRC / 'server_knock.py'), str(SRC / 'ui' / 'gui_main.py')}
    keep_modules = set()
    for m, p in modules.items():
        if str(p) in entry_files:
            keep_modules.add(m)

    candidates = []
    for m, p in modules.items():
        if m in keep_modules:
            continue
        importers = imported_by.get(m, set())
        if not importers:
            rel = p.relative_to(ROOT)
            candidates.append({'module': m, 'path': str(p), 'reason': 'no_static_imports_found'})

    report = {
        'root': str(ROOT),
        'scanned_files_count': len(files),
        'modules_count': len(modules),
        'candidates_count': len(candidates),
        'candidates': candidates,
    }

    (REPORT_DIR / 'unused_report_src.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')

    lines = []
    lines.append(f"Root: {ROOT}")
    lines.append(f"Scanned files (src): {len(files)}")
    lines.append(f"Modules: {len(modules)}")
    lines.append(f"Candidates (no static imports): {len(candidates)}")
    lines.append("")
    if candidates:
        lines.append("Posibles archivos sin uso en src/ (revisar manualmente):")
        for c in candidates:
            lines.append(f" - {c['path']}  ({c['module']})")
    else:
        lines.append("No se detectaron candidatos claros en src/.")

    (REPORT_DIR / 'unused_report_src.txt').write_text('\n'.join(lines), encoding='utf-8')
    print(f"Reporte generado: {REPORT_DIR / 'unused_report_src.json'} and {REPORT_DIR / 'unused_report_src.txt'}")


if __name__ == '__main__':
    main()
