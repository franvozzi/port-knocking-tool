import subprocess
import sys
from pathlib import Path


def test_e2e_knockd():
    repo_root = Path(__file__).resolve().parents[2]
    script = repo_root / "scripts" / "e2e_test_knockd.py"
    assert script.exists(), f"E2E script not found at {script}"

    env = dict(**dict())
    # Use the same python interpreter running the tests
    py = sys.executable
    cmd = [py, str(script)]
    proc = subprocess.run(
        cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=60
    )
    print(proc.stdout)
    assert proc.returncode == 0, "E2E script failed; check output above"
