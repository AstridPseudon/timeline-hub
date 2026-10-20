"""Already-admitted M1 captures must not gain canonical authority on upgrade.

Archive both producers: a fresh admission on today's Runtime cannot exercise
this boundary. Old and current Runtime always run in separate interpreters.
"""
from __future__ import annotations

import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

import pytest

from tests.astrid_checkout import astrid_checkout

pytestmark = pytest.mark.integration
RUNTIME_M1 = "4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136"
AGENT_CAPTURE = "321cef4b8c89a4a938cb9ede41ba6a5444cf1b62"
ROOT = Path(__file__).resolve().parents[1]


class LegacyCertificationFailure(AssertionError):
    """Only a fully exercised forged canonical binding is an expected failure."""


class LegacyRetryFailure(AssertionError):
    """Only the documented semantic refusal of an exact retry is expected."""


LEGACY_GAP = pytest.mark.xfail(
    strict=True, raises=LegacyCertificationFailure,
    reason="02:42(b): legacy canonical capture claim is not content-verified",
)


def _archive(repo, revision, target, *paths):
    archive = subprocess.run(
        ["git", "-C", str(repo), "archive", revision, *paths],
        check=True, capture_output=True,
    )
    target.mkdir()
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as source:
        source.extractall(target, filter="data")
    return target


@pytest.fixture(scope="module")
def archived_capture(tmp_path_factory):
    root = tmp_path_factory.mktemp("legacy-capture-sources")
    runtime = _archive(ROOT, RUNTIME_M1, root / "runtime")
    agent = _archive(astrid_checkout(), AGENT_CAPTURE, root / "agent",
                     "astrid", "astrid_runtime_client", "tests", "schemas",
                     "config", "runtime.lock.json", "pyproject.toml")
    return runtime, agent


@pytest.fixture(scope="module", params=[
    (field, inline) for field in ("genuine", "native", "config", "registry", "expansion")
    for inline in (False, True)
], ids=lambda case: case[0] + ("-inline" if case[1] else "-ref"))
def upgraded_capture(archived_capture, tmp_path_factory, request):
    field, inline = request.param
    tmp_path = tmp_path_factory.mktemp("legacy-capture-realm")
    old_runtime, agent = archived_capture
    helper = Path(__file__).with_name("snapshot_legacy_fixture.py")
    for stage, runtime in (("admit", old_runtime), ("reopen", ROOT)):
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
               "ASTRID_RUNTIME_CHECKOUT": str(runtime)}
        result = subprocess.run(
            [sys.executable, str(helper), stage, str(runtime), str(agent),
             str(tmp_path), field, str(int(inline))],
            cwd=tmp_path, env=env, text=True, capture_output=True, timeout=90,
        )
        assert result.returncode == 0, result.stdout + result.stderr
    return field, json.loads(result.stdout)


def test_already_admitted_capture_after_upgrade(upgraded_capture, request):
    field, binding = upgraded_capture
    # 02:42(b): restore when claim verifies recorded canonical content or
    # returns an explicitly uncertified legacy execution view.
    if field in {"config", "registry", "expansion"}:
        request.node.add_marker(LEGACY_GAP)
    if field in {"config", "registry", "expansion"} and binding["canonical_source"]:
        raise LegacyCertificationFailure(
            f"legacy {field} minted {binding['canonical_source']} from current claim without canonical verification"
        )


def test_exact_legacy_capture_retry_after_upgrade(upgraded_capture, request):
    field, binding = upgraded_capture
    if field != "native":
        # Exact accepted identity must be recoverable without re-admission.
        request.node.add_marker(pytest.mark.xfail(
            strict=True, raises=LegacyRetryFailure,
            reason="legacy canonical exact retry re-runs admission before receipt replay",
        ))
    if binding["retry_refusal"]:
        raise LegacyRetryFailure(binding["retry_refusal"])
