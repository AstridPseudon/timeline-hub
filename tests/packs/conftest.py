"""Fixtures shared by the pack tests that run a real Remotion or Three.js render.

A real render needs the provisioned ``remotion/`` install (``make remotion-install``) and, because the
Remotion runtime refuses an unvalidated launch (``remotion_runtime._validated_runtime``), the launch-owned
validation that the host bootstrap normally issues. Tests that call ``RenderService`` or a backend directly
bypass the host, so they request ``remotion_launch_validation`` and are marked ``integration`` (testing plan
R-2). A missing install is a broken integration lane and fails; it is never a skip (R-6).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.helpers.remotion_validation import issue_remotion_launch_validation, remotion_install_problems
from tests.packs.rendering._helpers import _execution_env

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
    issue_remotion_launch_validation(tmp_path, monkeypatch)
