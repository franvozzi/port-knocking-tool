from types import SimpleNamespace
from pathlib import Path

import pytest

from src.core.vpn_manager import LinuxVPNManager


def make_subprocess_return(code=0, stdout='', stderr=''):
    return SimpleNamespace(returncode=code, stdout=stdout, stderr=stderr)


def test_linux_connect_success(monkeypatch, tmp_path):
    mgr = LinuxVPNManager()

    # Crear perfil falso
    profile = tmp_path / 'profile.ovpn'
    profile.write_text('dummy')

    # Forzar _find_profile para devolver el perfil creado
    monkeypatch.setattr(LinuxVPNManager, '_find_profile', lambda self, p: profile)

    # Mockear subprocess.run para simular éxito
    monkeypatch.setattr('src.core.vpn_manager.subprocess.run', lambda *a, **k: make_subprocess_return(0))

    assert mgr.connect('profile.ovpn') is True
    assert mgr.connected is True


def test_linux_connect_failure(monkeypatch, tmp_path):
    mgr = LinuxVPNManager()

    profile = tmp_path / 'profile.ovpn'
    profile.write_text('dummy')

    monkeypatch.setattr(LinuxVPNManager, '_find_profile', lambda self, p: profile)

    # Simular fallo en subprocess
    monkeypatch.setattr('src.core.vpn_manager.subprocess.run', lambda *a, **k: make_subprocess_return(1, stderr='error'))

    assert mgr.connect('profile.ovpn') is False
    assert mgr.connected is False


def test_linux_disconnect_and_is_connected(monkeypatch):
    mgr = LinuxVPNManager()

    # Mock subprocess.run para disconnect
    monkeypatch.setattr('src.core.vpn_manager.subprocess.run', lambda *a, **k: make_subprocess_return(0))

    # Simular desconexión
    mgr.connected = True
    assert mgr.disconnect() is True
    assert mgr.connected is False

    # Simular is_connected True/False
    monkeypatch.setattr('src.core.vpn_manager.subprocess.run', lambda *a, **k: make_subprocess_return(0))
    assert mgr.is_connected() is True

    monkeypatch.setattr('src.core.vpn_manager.subprocess.run', lambda *a, **k: make_subprocess_return(1))
    assert mgr.is_connected() is False
