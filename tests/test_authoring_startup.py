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
from runtime_protocol.cli import _parser
from runtime_protocol.store import RealmStore
from runtime_protocol.contract_metadata import SCHEMA_DIGEST
from astrid.sdk.timeline.commit import RuntimeCommitService
from banodoco_local.bootstrap import SourceProfile
from banodoco_local.runtime_boundary import LocalRuntimeBoundary
root = Path(os.environ["CASE_ROOT"])
RealmStore.initialize(root / "realm").close()
profile = SourceProfile.from_mapping({
    "profile": "astrid", "runtime_checkout": str(Path(__import__("runtime_protocol").__file__).parent.parent),
    "source_checkout": str(Path(__import__("astrid").__file__).parent.parent),
})
argv = LocalRuntimeBoundary()._argv(
    profile, realm_id="realm", realm_root=root / "realm", support_root=root / "support",
    display_name="Astrid Workspace", owner_lock=root / "support" / "instance.lock",
    token_file=root / "support" / "bootstrap-token",
)
args = _parser().parse_args(argv[3:])
d = RuntimeDaemon(args.root, support_root=args.support_root, authoring_profile=args.authoring_profile).start()
try:
    assert type(d.service._timeline_commit_provider) is RuntimeCommitService
    assert d.service._timeline_commit_provider.contract_digest == SCHEMA_DIGEST
    request = urllib.request.Request(d.endpoint + "/v1/projects", headers={"Authorization": "Bearer " + d.token})
    with urllib.request.urlopen(request, timeout=5) as r:
        assert r.status == 200
        json.load(r)
    with urllib.request.urlopen(d.endpoint + "/v1/health", timeout=5) as r:
        health = json.load(r)
    assert health["schema_digest"] == SCHEMA_DIGEST
finally:
    d.stop()
assert d.thread is None or not d.thread.is_alive()
assert d.httpd is None and d.service is None
assert not (root / "support" / "discovery.json").exists()
print(json.dumps({"registered": True, "first_authenticated_request": 200,
                  "http_health": health, "argv": argv[:6], "pid": os.getpid(), "settled": True}))
''')
    assert result.returncode == 0, result.stdout + result.stderr
    proof = json.loads(result.stdout)
    assert proof["registered"] is True
    assert proof["first_authenticated_request"] == 200
    assert proof["settled"] is True
    assert proof["argv"][4:] == ["--authoring-profile", "astrid"]
    print(result.stdout.strip())


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
