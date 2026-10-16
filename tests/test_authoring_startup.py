"""Real installed authoring startup; no service/provider doubles."""
from __future__ import annotations
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


def run_installed(source, tmp_path, script):
    runtime = Path(__file__).resolve().parents[1]
    env = dict(os.environ, PYTHONPATH=os.pathsep.join((str(runtime), source)),
               PYTHONDONTWRITEBYTECODE="1", CASE_ROOT=str(tmp_path))
    return subprocess.run([sys.executable, "-B", "-c", script], cwd=tmp_path,
                          env=env, text=True, capture_output=True, timeout=30)


def test_real_installed_authoring_registers_before_first_http(tmp_path):
    source = os.environ.get("RUNTIME_AUTHORING_ASTRID_SOURCE")
    if not source:
        pytest.skip("requires explicitly selected installed Astrid source")
    result = run_installed(source, tmp_path, r'''
import json, os, urllib.request
from pathlib import Path
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.store import RealmStore
from runtime_protocol.contract_metadata import SCHEMA_DIGEST
from astrid.sdk.timeline.commit import RuntimeCommitService
root = Path(os.environ["CASE_ROOT"])
RealmStore.initialize(root / "realm").close()
d = RuntimeDaemon(root / "realm", support_root=root / "support", authoring_profile="astrid").start()
try:
    assert type(d.service._timeline_commit_provider) is RuntimeCommitService
    assert d.service._timeline_commit_provider.contract_digest == SCHEMA_DIGEST
    with urllib.request.urlopen(d.endpoint + "/v1/health", timeout=5) as r:
        health = json.load(r)
    assert health["schema_digest"] == SCHEMA_DIGEST
    print(json.dumps({"registered": True, "http_health": health}))
finally:
    d.stop()
assert d.thread is None or not d.thread.is_alive()
''')
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["registered"] is True


def test_actual_stale_installed_provider_refused_before_persistence(tmp_path):
    source = os.environ.get("RUNTIME_AUTHORING_STALE_ASTRID_SOURCE")
    if not source:
        pytest.skip("requires immutable historical stale Astrid source")
    result = run_installed(source, tmp_path, r'''
import os
from pathlib import Path
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.errors import ValidationError
root = Path(os.environ["CASE_ROOT"])
d = RuntimeDaemon(root / "realm", support_root=root / "support", authoring_profile="astrid")
try:
    d.start()
except ValidationError as e:
    assert "interface/contract mismatch" in str(e)
else:
    d.stop()
    raise AssertionError("stale provider was accepted")
assert d.service is None and d.httpd is None and d.thread is None
assert not (root / "realm").exists() and not (root / "support").exists()
print("mismatch refused before realm, credentials, readiness, or HTTP")
''')
    assert result.returncode == 0, result.stdout + result.stderr


def test_unknown_authoring_profile_refused_without_persistence(tmp_path):
    from runtime_protocol.daemon import RuntimeDaemon
    with pytest.raises(ValueError, match="unsupported authoring profile"):
        RuntimeDaemon(tmp_path / "realm", support_root=tmp_path / "support", authoring_profile="caller.module")
    assert not (tmp_path / "realm").exists() and not (tmp_path / "support").exists()
