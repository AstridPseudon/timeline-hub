"""Stable user terminal launchers for the selected installed version."""

from __future__ import annotations

import os
from pathlib import Path

_RUNNER = '''from __future__ import annotations
import json, os, re, sys
from pathlib import Path

root = Path(__file__).resolve().parent
name = (root / "current").read_text(encoding="utf-8").strip()
if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", name):
    raise SystemExit("Astrid's current version pointer is invalid.")
version_root = root / "versions" / name
record = json.loads((version_root / "version.json").read_text(encoding="utf-8"))
if Path(record["root"]).resolve() != version_root.resolve():
    raise SystemExit("Astrid's current version points outside its program folder.")
python = str(Path(record["python"]))
env = dict(os.environ)
env.update({str(key): str(value) for key, value in record["env"].items()})
env["ASTRID_INSTALL_PROGRAM_ROOT"] = str(root)
if sys.argv[1:2] == ["credential"]:
    os.environ.update(env)
    from astrid.core.util.credential_store import main
    raise SystemExit(main(sys.argv[2:]))
os.execve(python, [python, "-I", "-m", "astrid.omp_agent", *sys.argv[1:]], env)
'''


def install(root: Path) -> tuple[Path, ...]:
    """Write stable launchers that follow root/current without changing PATH."""
    root = Path(root).absolute()
    runner = root / "run_astrid.py"
    runner.write_text(_RUNNER, encoding="utf-8", newline="\n")
    if os.name == "nt":
        launcher = root / "run-astrid.cmd"
        launcher.write_text(
            '@echo off\r\n'
            'set "ASTRID_PROGRAM_ROOT=%~dp0"\r\n'
            'for /f "usebackq delims=" %%V in ("%ASTRID_PROGRAM_ROOT%current") do set "ASTRID_VERSION=%%V"\r\n'
            '"%ASTRID_PROGRAM_ROOT%versions\\%ASTRID_VERSION%\\py\\Scripts\\python.exe" -I "%ASTRID_PROGRAM_ROOT%run_astrid.py" %*\r\n',
            encoding="utf-8", newline="",
        )
        return launcher, runner
    launcher = root / "run-astrid"
    launcher.write_text(
        '#!/bin/sh\n'
        'set -eu\n'
        'root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)\n'
        'version=$(cat "$root/current")\n'
        'case "$version" in *[!A-Za-z0-9._-]*|"") echo "Astrid current version pointer is invalid." >&2; exit 2;; esac\n'
        'exec "$root/versions/$version/py/bin/python" -I "$root/run_astrid.py" "$@"\n',
        encoding="utf-8", newline="\n",
    )
    launcher.chmod(0o755)
    return launcher, runner
