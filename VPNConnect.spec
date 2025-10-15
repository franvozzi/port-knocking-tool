# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/gui_main.py'],
    pathex=[],
    binaries=[],
    datas=[('src/config.json', '.'), ('src/profile.ovpn', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VPNConnect',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources/icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VPNConnect',
)
app = BUNDLE(
    coll,
    name='VPNConnect.app',
    icon='resources/icon.ico',
    bundle_identifier=None,
)
