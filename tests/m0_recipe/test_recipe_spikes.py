"""M0 observations of real frozen R4 APIs, isolated from main's module cache.

These assert current behaviour, including identified gaps; they are not claims
that R4 meets the proposed recipe. See README.md and the shared edit recipe.
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
CASES = (
    "clears_and_unchanged_writes",
    "ripple_concurrent_membership",
    "transition_endpoints",
    "track_dependencies",
    "stable_ids_and_collision",
    "music_authored_and_derived",
    "transcript_identity",
    "inverse_aba_and_ancestry",
    "immutable_media",
)


@pytest.fixture(scope="session")
def frozen_r4(tmp_path_factory):
    # An explicit read-only port-spike path can replace extraction. No editable
    # installs, changes to another worker's tree, or product ports happen here.
    supplied = os.environ.get("ASTRID_RECIPE_R4_ROOT")
    if supplied:
        root = Path(supplied).resolve()
        assert (root / "astrid/sdk/timeline/commands.py").is_file()
        return root
    root = tmp_path_factory.mktemp("recipe-r4")
    archive = subprocess.check_output(
        ["git", "archive", R4_REF, "pyproject.toml", "astrid", "banodoco_workspace_client",
         "schemas", "tests/sdk", "tests/fixtures/timeline_editing"],
        cwd=REPO,
    )
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        source.extractall(root, filter="data")
    return root


@pytest.mark.parametrize("case", CASES)
def test_real_r4_observation(frozen_r4, tmp_path, case):
    result = subprocess.run(
        [sys.executable, "-B", str(Path(__file__).with_name("r4_cases.py")),
         str(frozen_r4), case],
        cwd=tmp_path,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
             "BANODOCO_LOCAL_DATA_ROOT": str(tmp_path / "data")},
        text=True, capture_output=True, timeout=180,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"PASS {case}" in result.stdout
    print(result.stdout.strip())
