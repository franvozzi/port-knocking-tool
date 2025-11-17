#!/usr/bin/env python3
"""E2E test: arranca el servidor dummy, realiza knocks y verifica apertura de puerto VPN."""
import subprocess
import sys
import time
import socket
import os
from pathlib import Path

# Config
REPO_ROOT = Path(__file__).parent
PY = sys.executable
SERVER_SCRIPT = REPO_ROOT.parent / "src" / "test_knockd_server.py"
INTERVAL = 3.0
KNOCK_PORTS = [7000, 8000]
VPN_PORT = 1194
STARTUP_TIMEOUT = 8


def start_server():
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    cmd = [PY, str(SERVER_SCRIPT), "--interval", str(INTERVAL)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    # wait for startup banner or timeout
    start = time.time()
    out_lines = []
    while time.time() - start < STARTUP_TIMEOUT:
        line = p.stdout.readline()
        if not line:
            time.sleep(0.1)
            continue
        out_lines.append(line)
        sys.stdout.write(line)
        sys.stdout.flush()
        if "Servidor de Port Knocking (dummy) iniciado" in line:
            break
    else:
        p.kill()
        raise RuntimeError("Server startup timeout")
    return p, out_lines


def do_knocks(delay_between=1.0):
    for port in KNOCK_PORTS:
        try:
            s = socket.socket()
            s.settimeout(2)
            s.connect(("127.0.0.1", port))
            s.close()
            print(f"client: knock {port} ok")
        except Exception as e:
            print(f"client: error knocking {port}: {e}")
        time.sleep(delay_between)


def capture_until(p, keyword, timeout=10):
    start = time.time()
    buf = []
    while time.time() - start < timeout:
        line = p.stdout.readline()
        if not line:
            time.sleep(0.1)
            continue
        buf.append(line)
        sys.stdout.write(line)
        sys.stdout.flush()
        if keyword in line:
            return True, buf
    return False, buf


def main():
    print("Starting server...")
    p, banner = start_server()

    try:
        # Realizar knocks con delay menor que INTERVAL
        print("Performing knocks with delay 1s (< interval)")
        do_knocks(delay_between=1.0)

        ok, lines = capture_until(p, "SECUENCIA CORRECTA", timeout=10)
        if not ok:
            print("FAIL: did not observe SECUENCIA CORRECTA")
            return 1

        # Verificar que el puerto VPN fue abierto
        ok2, lines2 = capture_until(p, "Puerto 1194 ABIERTO", timeout=5)
        if not ok2:
            print("FAIL: did not observe VPN port open message")
            return 1

        print("PASS: sequence accepted and VPN port opened")
        return 0
    finally:
        try:
            p.terminate()
            p.wait(timeout=2)
        except Exception:
            try:
                p.kill()
            except Exception:
                pass


if __name__ == "__main__":
    sys.exit(main())
