"""The client half of a cross-product test, against a real Runtime daemon.

``astrid.core.dev.cross_client`` is what a browser test (the App) drives next to the ``astrid`` CLI: an
identity probe and a one-shot executor host, both connected through the explicit
``ASTRID_TIMELINE_EVAL_*`` context so that neither the launcher nor a pack host starts. The variable names
are spelled out here on purpose: removing or renaming them in ``astrid/sdk/client.py`` fails this test.
"""
from __future__ import annotations

import json
import os
import struct
import subprocess
import sys
import zlib
from pathlib import Path

import pytest

from astrid_runtime_client.contract_metadata import SCHEMA_DIGEST
from tests.helpers.runtime import vendored_runtime_commit

pytestmark = pytest.mark.integration  # a real daemon from a second checkout, and short-lived subprocesses

ASTRID = Path(__file__).resolve().parents[2]
ACTOR = "owner"
# Spelled out, not imported: this is the contract the App-side harness relies on.
CONTEXT = {
    "endpoint": "ASTRID_TIMELINE_EVAL_ENDPOINT",
    "credential": "ASTRID_TIMELINE_EVAL_CREDENTIAL",
    "realm": "ASTRID_TIMELINE_EVAL_REALM_ID",
    "actor": "ASTRID_TIMELINE_EVAL_ACTOR_ID",
}


@pytest.fixture
def daemon(real_runtime, tmp_path):
    """A real daemon from the Runtime commit the vendored client was produced from, so the schema digests agree."""
    return real_runtime(support_root=tmp_path / "runtime-support", commit=vendored_runtime_commit())


@pytest.fixture
def env(daemon, tmp_path) -> dict[str, str]:
    """Built from nothing, like the App harness does: no ambient Astrid state and no ambient Runtime."""
    (tmp_path / "home").mkdir()
    return {
        "PATH": os.environ["PATH"],
        "HOME": str(tmp_path / "home"),
        "XDG_STATE_HOME": str(tmp_path / "state"),
        "ASTRID_RUNTIME_DATA_ROOT": str(tmp_path / "astrid-data"),
        "PYTHONPATH": str(ASTRID),
        "PYTHONDONTWRITEBYTECODE": "1",
        CONTEXT["endpoint"]: daemon.endpoint,
        CONTEXT["credential"]: str(daemon.credential_path),
        CONTEXT["realm"]: daemon.service.realm["id"],
        CONTEXT["actor"]: ACTOR,
    }


def run(env: dict[str, str], *argv: str, ok: bool = True) -> subprocess.CompletedProcess[str]:
    done = subprocess.run([sys.executable, *argv], env=env, capture_output=True, text=True, timeout=120, cwd=env["HOME"])
    assert (done.returncode == 0) is ok, f"{argv}: exit {done.returncode}\n{done.stdout}\n{done.stderr}"
    return done


def cross_client(env: dict[str, str], *argv: str, ok: bool = True) -> dict:
    done = run(env, "-m", "astrid.core.dev.cross_client", *argv, ok=ok)
    return json.loads(done.stdout) if ok else {"message": done.stderr}


def png_pixels(data: bytes) -> tuple[int, int, bytes]:
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    chunks, offset = {}, 8
    while offset < len(data):
        (length,) = struct.unpack(">I", data[offset:offset + 4])
        chunks[data[offset + 4:offset + 8]] = data[offset + 8:offset + 8 + length]
        offset += 12 + length
    width, height = struct.unpack(">II", chunks[b"IHDR"][:8])
    raw = zlib.decompress(chunks[b"IDAT"])
    assert len(raw) == height * (1 + 3 * width)
    return width, height, raw[1:4]


def test_identity_names_the_daemon_and_this_astrid_without_a_launcher(daemon, env, tmp_path):
    seen = cross_client(env, "identity")
    assert seen["realm_id"] == daemon.service.realm["id"]
    assert seen["actor_id"] == ACTOR
    assert seen["runtime_instance_id"] == daemon.instance_id
    assert seen["schema_digest"] == SCHEMA_DIGEST
    assert Path(seen["astrid_file"]).is_relative_to(ASTRID)
    assert seen["astrid_head"] is None or len(seen["astrid_head"]) == 40
    # Answered from the explicit context alone: the launcher would have created its support root.
    assert not (tmp_path / "astrid-data").exists()


def test_the_explicit_context_is_all_or_nothing_and_checked_against_the_daemon(daemon, env):
    for name in CONTEXT.values():
        partial = {key: value for key, value in env.items() if key != name}
        assert "incomplete" in cross_client(partial, "identity", ok=False)["message"], name
    wrong_realm = {**env, CONTEXT["realm"]: "not-this-realm"}
    assert "realm_id" in json.dumps(cross_client(wrong_realm, "identity", ok=False))


def test_marker_executor_registers_runs_once_and_settles_a_png(daemon, env, tmp_path):
    from astrid.sdk.client import AstridClient

    credential = tmp_path / "worker.token"
    credential.write_text(daemon.worker_token, encoding="utf-8")
    credential.chmod(0o600)
    host = ["host", "--pack-root", str(tmp_path / "packs"), "--worker-credential", str(credential), "--color", "336699"]

    assert cross_client(env, *host, "--register")["capability_id"] == "f2.marker"

    with AstridClient.open(
        endpoint=daemon.endpoint, credential=daemon.credential_path, realm_id=daemon.service.realm["id"],
        actor_id=ACTOR, client_name="cross-client-test", client_version="test", protocol_version="workspace.v1",
    ) as client:
        project = client.projects.create(slug="f2", name="F2", idempotency_key="project").data["project_id"]
        created = json.loads(run(
            env, "-m", "astrid", "tasks", "create", "--project", project, "--capability", "f2.marker",
            "--spec", "{}", "--idempotency-key", "task", "--json",
        ).stdout)
        assert created["ok"], created
        task_id = created["data"]["task_id"]
        assert client.tasks.show(task_id).data["state"] != "succeeded"

        settled = cross_client(env, *host, "--run-once")
        assert (settled["task_id"], settled["state"]) == (task_id, "succeeded")
        [output] = settled["outputs"]
        assert (output["name"], output["media_type"]) == ("marker", "image/png")
        assert client.tasks.show(task_id).data["state"] == "succeeded"
        width, height, pixel = png_pixels(client.media.read_bytes(output["object_id"]))
        assert (width, height, pixel.hex()) == (64, 48, "336699")

        idle = cross_client(env, *host, "--run-once")
        assert (idle["task_id"], idle["state"], idle["outputs"]) == (None, "idle", [])
