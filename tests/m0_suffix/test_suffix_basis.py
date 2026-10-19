"""Final dependent-suffix decision, exercised with frozen R4 semantic APIs.

The subprocess supplies isolation from main's imports. The adapter is an M0
specification, not a Runtime transaction or a browser outbox implementation.
"""

from __future__ import annotations

import io
import os
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
R4_REF = "origin/codex/handover-timeline-r4-20261019-candidate-sdk"
CASES = [
    (scenario, mode, recovery, "after_ack" if scenario == "disjoint" else "before_ack")
    for scenario in ("disjoint", "read_conflict", "selection_conflict")
    for mode in ("absolute", "relative")
    for recovery in ("ack", "retry", "reload")
] + [
    (scenario, mode, "reload", "before_ack")
    for scenario in ("aba", "same_value", "created", "basis_conflict", "rejected", "guards", "schema",
                     "retry_identity")
    for mode in ("absolute", "relative")
] + [("inverse_history", "absolute", "ack", "after_ack")]


@pytest.fixture(scope="session")
def frozen_r4(tmp_path_factory):
    root = tmp_path_factory.mktemp("suffix-r4")
    archive = subprocess.check_output(
        ["git", "archive", R4_REF, "pyproject.toml", "astrid", "banodoco_workspace_client", "schemas",
         "tests/fixtures/timeline_editing/tiny_publishable.json"],
        cwd=REPO,
    )
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        source.extractall(root, filter="data")
    return root


@pytest.mark.parametrize("scenario,mode,recovery,stage", CASES)
def test_dependent_suffix(frozen_r4, tmp_path, scenario, mode, recovery, stage):
    result = subprocess.run(
        [sys.executable, "-B", str(Path(__file__).with_name("r4_cases.py")),
         str(frozen_r4), scenario, mode, recovery, stage],
        cwd=tmp_path,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
             "BANODOCO_LOCAL_DATA_ROOT": str(tmp_path / "data")},
        text=True, capture_output=True, timeout=180,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"PASS {scenario}" in result.stdout
