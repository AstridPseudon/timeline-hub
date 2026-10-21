"""What the test bootstrap leaves in os.environ must stay valid for the Remotion runtime validation."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from astrid.core.rendering.remotion_runtime import probe_context

REPO = Path(__file__).resolve().parents[1]


def test_bootstrap_environment_is_accepted_by_the_remotion_probe_context(tmp_path: Path) -> None:
    """In-process renders validate os.environ; a bootstrap-exported PYTHONPYCACHEPREFIX makes them refuse.

    The bootstrap runs in a child with no PYTHON* variables of its own, so a developer's shell cannot
    change the result.
    """
    clean = {"PATH": os.environ["PATH"], "HOME": str(tmp_path), "PYTHONPATH": str(REPO)}
    result = subprocess.run(
        [sys.executable, "-c", "import json, os, tests.conftest; print(json.dumps(dict(os.environ)))"],
        cwd=REPO, env=clean, capture_output=True, text=True, timeout=120, check=True,
    )
    bootstrapped = json.loads(result.stdout.splitlines()[-1])
    bootstrapped.pop("PYTHONPATH")
    assert bootstrapped["PYTHONDONTWRITEBYTECODE"] == "1"
    probe_context(environment=bootstrapped, python_executable=sys.executable)
