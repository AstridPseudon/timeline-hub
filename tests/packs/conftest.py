"""Fixtures shared by the pack tests that run a real Remotion or Three.js render.

A real render needs the provisioned ``remotion/`` install (``make remotion-install``) and, because the
Remotion runtime refuses an unvalidated launch (``remotion_runtime._validated_runtime``), the launch-owned
validation that the host bootstrap normally issues. Tests that call ``RenderService`` or a backend directly
bypass the host, so they request ``remotion_launch_validation`` and are marked ``integration`` (testing plan
R-2). A missing install is a broken integration lane and fails; it is never a skip (R-6).
"""

from __future__ import annotations

import os
import secrets
import shutil
import sys
from pathlib import Path

import pytest

from astrid.core.env_vars import (
    ASTRID_NODE_EXECUTABLE,
    ASTRID_REMOTION_PROJECT_DIR,
    ASTRID_REMOTION_VALIDATION_LAUNCH,
    ASTRID_REMOTION_VALIDATION_PATH,
    ASTRID_REMOTION_VALIDATION_ROLE,
    ASTRID_REMOTION_VALIDATION_SHA256,
)
from astrid.core.rendering.remotion_runtime import prepare_remotion_validation
from tests.packs.rendering._helpers import _execution_env

REMOTION = Path(__file__).resolve().parents[2] / "remotion"
REQUIRED_BINARIES = ("node", "npx", "ffmpeg", "ffprobe")
REQUIRED_PACKAGES = (
    "@banodoco/timeline-composition",
    "@banodoco/timeline-schema",
    "@banodoco/timeline-theme-2rp",
    "@remotion/cli",
    "@remotion/three",
    "@react-three/fiber",
    "three",
)


def remotion_install_problems() -> list[str]:
    """What a real render needs that this machine does not provide; empty when it is provisioned."""
    problems = [f"{binary} is not on PATH" for binary in REQUIRED_BINARIES if shutil.which(binary) is None]
    modules = REMOTION / "node_modules"
    problems.extend(
        f"remotion/node_modules/{package} is missing" for package in REQUIRED_PACKAGES if not (modules / package).is_dir()
    )
    return problems


@pytest.fixture
def renderer_execution_environment():
    """Keep nested backend commands on the test process runtime.

    Renderer manifests use ``python3`` and ``node`` from PATH, so relying on the shell's ambient PATH can
    select a different interpreter that lacks the canonical timeline-schema package.
    """

    with _execution_env():
        yield


@pytest.fixture
def remotion_launch_validation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    renderer_execution_environment: None,
) -> None:
    """Issue the launch proof a provisioned Remotion worker needs, for this test's exact environment.

    There is no GenericPackHost bootstrap here to issue its normal launch artifact. Qualify the canonical
    child environment with the production transaction; the backend child inherits these parent-owned
    references through ``CommandTransport``, and an in-process render reads them from this process.
    """

    problems = remotion_install_problems()
    if problems:
        pytest.fail(
            "a real render needs the provisioned Remotion install (run `make remotion-install`): " + "; ".join(problems),
            pytrace=False,
        )
    for name in (
        ASTRID_REMOTION_VALIDATION_PATH,
        ASTRID_REMOTION_VALIDATION_SHA256,
        ASTRID_REMOTION_VALIDATION_LAUNCH,
        ASTRID_REMOTION_VALIDATION_ROLE,
    ):
        monkeypatch.delenv(name, raising=False)

    monkeypatch.setenv(ASTRID_REMOTION_PROJECT_DIR, str(REMOTION.resolve()))
    node_value = os.environ.get(ASTRID_NODE_EXECUTABLE) or shutil.which("node")
    assert node_value, "the provisioned Remotion environment must provide Node"
    node = Path(node_value).expanduser().resolve(strict=True)
    monkeypatch.setenv(ASTRID_NODE_EXECUTABLE, str(node))

    # The transaction qualifies this process's environment (what an in-process render validates) and its
    # allowlist projection (what the transport hands the backend child). The process must therefore carry no
    # loader, interpreter-startup or Git-redirect overrides: the runtime refuses those and so does this fixture.
    reference = prepare_remotion_validation(
        artifact_directory=tmp_path / "remotion-validation",
        host_environment=dict(os.environ),
        python_executable=sys.executable,
        launch_id=secrets.token_hex(16),
        contexts={"standalone": dict(os.environ)},
    )
    for name, value in reference.items():
        monkeypatch.setenv(name, value)
