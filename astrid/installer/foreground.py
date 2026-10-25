"""Pinokio's foreground owner, using the login service's Runtime command."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from .core import absolute, current, read_json
from .service import LABEL, command


def launch(root: Path, argv: list[str], *, system: str | None = None) -> None:
    root = absolute(root)
    record = read_json(root / "install.json")
    if record.get("owner") != LABEL or record.get("managed_by") != "pinokio":
        raise ValueError("This is not a Pinokio-managed Astrid installation.")
    version = current(root)
    if version is None:
        raise ValueError("Astrid has no installed version. Install Astrid in Pinokio first.")
    data = absolute(record["data_root"])
    env = {key: value for key, value in os.environ.items() if key not in {
        "PYTHONPATH", "PYTHONHOME", "ASTRID_WORKSPACE_ENDPOINT",
        "ASTRID_WORKSPACE_CREDENTIAL", "ASTRID_RUNTIME_SOURCE_MANIFEST",
        "ASTRID_RUNTIME_DATA_ROOT", "ASTRID_PACKS_PATH",
    }}
    env.update(version.env)
    env["ASTRID_INSTALL_MANAGED_BY"] = "pinokio"
    # Use the console interpreter on Windows. pythonw is specific to the
    # hidden Scheduled Task; the same Runtime command/settings run here in
    # the console owner so Ctrl+Break and console-close reach its handlers.
    arguments = command(version, data, env_file=root / "service-env.json", extra_args=argv)
    if (system or sys.platform) != "win32":
        os.execvpe(arguments[0], arguments, env)
    else:
        os.environ.clear()
        os.environ.update(env)
        os.chdir(version.root)
        # os.exec on Windows creates another process. Evaluate the canonical
        # -c command in this interpreter instead, with no waiting shim/child.
        exec(compile(arguments[3], "<astrid-runtime run>", "exec"), {"__name__": "__main__"})


if __name__ == "__main__":
    launch(Path(sys.argv[1]), sys.argv[2:])
