"""Official producer/historical types and unchanged commit transport boundary."""
from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path
from typing import get_type_hints

import astrid_runtime_client as client
import pytest
import test_timeline_commit_port as support
from astrid_runtime_client import timeline_commit_types as dto

from runtime_protocol import timeline_commit as abi
from runtime_protocol import timeline_commit_producer as producer
from runtime_protocol.errors import ValidationError
from runtime_protocol.timeline_commit_validation import validate_commit_value

service = support.service
ROOT = Path(__file__).resolve().parents[1]
DIGEST = "sha256:" + "a" * 64
NAMES = (
    "ProducerAdmittedTarget", "ProducerAttemptPin", "ProducerGuardArgs",
    "ProducerIdentity", "SettledProducerProposal", "CanonicalRenderRevision",
    "RenderTimelineAuthority",
)


def guarded_request(service):
    body = support.request(service)
    target = {key: body[key] for key in (
        "project_id", "timeline_id", "base_revision_id", "base_publication_id",
    )}
    pin = {"task_id": "task", "attempt_id": "attempt", "executor_id": "worker",
           "fence": 1, "runtime_epoch": 1, "admitted_target": target,
           "proposal_digest": DIGEST}
    body["commands"].insert(0, {"schema_version": 1, "op": "producer.guard",
        "version": "1", "select": None, "args": {"pin": pin}})
    return body


def test_packaged_guard_preserves_exact_pin_and_original_command(service):
    body = guarded_request(service)
    before = copy.deepcopy(body)
    validate_commit_value(body, "CommitRequest")
    assert body == before
    assert body["commands"][1:] == support.request(service)["commands"]


@pytest.mark.parametrize("damage", [
    "proposal_copy", "unknown_pin", "missing_target", "boolean_fence",
    "zero_epoch", "bad_digest", "blank_identity", "wrong_select", "outer_pin",
])
def test_malformed_guard_or_outer_envelope_refuses_422_before_provider_or_writes(service, damage):
    body = guarded_request(service)
    guard = body["commands"][0]
    pin = guard["args"]["pin"]
    if damage == "proposal_copy":
        guard["args"]["proposal"] = {"commands": body["commands"][1:]}
    elif damage == "unknown_pin":
        pin["lease_id"] = "not-authority"
    elif damage == "missing_target":
        del pin["admitted_target"]["base_publication_id"]
    elif damage == "boolean_fence":
        pin["fence"] = True
    elif damage == "zero_epoch":
        pin["runtime_epoch"] = 0
    elif damage == "bad_digest":
        pin["proposal_digest"] = "sha256:" + "A" * 64
    elif damage == "blank_identity":
        pin["task_id"] = " "
    elif damage == "wrong_select":
        guard["select"] = "parent"
    else:
        body["producer_pin"] = pin
    before = tuple(service.store.conn.iterdump())
    with pytest.raises(ValidationError) as caught:
        support.commit(service, body)
    assert caught.value.status == 422
    assert service.test_provider.calls == 0
    assert tuple(service.store.conn.iterdump()) == before


def test_root_exports_and_protocol_share_generated_canonical_types():
    for name in NAMES:
        assert getattr(client, name) is getattr(dto, name)
        assert name in client.__all__
    assert producer.ProducerAttemptPin is abi.ProducerAttemptPin
    assert producer.ProducerAdmittedTarget is abi.ProducerAdmittedTarget
    method = get_type_hints(abi.RuntimeCommitPort.producer_attempt)
    assert method["pin"] is abi.ProducerAttemptPin
    assert get_type_hints(method["return"])["pin"] is abi.ProducerAttemptPin
    assert not hasattr(client, "VerifiedProducerAttempt")
    task = json.loads((ROOT / "contract/schemas/task.json").read_text())["definitions"]
    for name in ("CanonicalRenderRevision", "RenderTimelineAuthority"):
        typed = getattr(dto, name)
        assert set(get_type_hints(typed)) == set(task[name]["properties"])
        assert typed.__required_keys__ == set(task[name].get("required", []))


def test_offline_python_wheel_exports_old_and_new_types_without_runtime_dependencies(tmp_path):
    source = tmp_path / "source"
    shutil.copytree(ROOT / "packages/python", source,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "build", "*.egg-info"))
    builder = None
    for candidate in (sys.executable, "python3.11", "python3.12", "python3.13", "python3"):
        try:
            probe = subprocess.run([candidate, "-c", "import setuptools.build_meta, wheel, pip"],
                                   capture_output=True, check=False)
        except OSError:
            continue
        if probe.returncode == 0:
            builder = candidate
            break
    assert builder is not None, "offline wheel probe needs an existing setuptools/wheel/pip environment"
    subprocess.run([builder, "-m", "pip", "wheel", "--no-index", "--no-cache-dir",
        "--no-build-isolation", "--no-deps", "--wheel-dir", str(tmp_path / "wheels"), str(source)],
        env={**os.environ, "SETUPTOOLS_USE_DISTUTILS": "stdlib"}, check=True)
    wheel, = (tmp_path / "wheels").glob("*.whl")
    installed = tmp_path / "installed"
    with zipfile.ZipFile(wheel) as archive:
        archive.extractall(installed)
    shutil.rmtree(source)
    shutil.copyfile(ROOT / "tests/fixtures/timeline_producer_types.py", tmp_path / "consumer.py")
    shutil.copyfile(ROOT / "tests/fixtures/timeline_bundle2_types.py", tmp_path / "old_consumer.py")
    subprocess.run([builder, "-S", "-c", """
import pathlib, runpy, sys
from typing import get_type_hints, is_typeddict
import astrid_runtime_client as client
from astrid_runtime_client import timeline_commit_types as dto
assert pathlib.Path(client.__file__).is_relative_to(pathlib.Path(sys.path[1]))
runpy.run_path('consumer.py')
runpy.run_path('old_consumer.py')
for name, value in vars(dto).items():
    if is_typeddict(value):
        assert set(get_type_hints(value)) == value.__required_keys__ | value.__optional_keys__, name
assert not any(n.startswith(('astrid.', 'runtime_protocol', 'jsonschema', 'referencing', 'yaml', 'remotion', 'composition')) for n in sys.modules)
"""], cwd=tmp_path,
        env={**os.environ, "PYTHONPATH": str(installed), "PYTHONDONTWRITEBYTECODE": "1"}, check=True)


def test_offline_packed_typescript_root_types_and_exact_transport(tmp_path):
    source = tmp_path / "source"
    shutil.copytree(ROOT / "packages/typescript", source,
                    ignore=shutil.ignore_patterns("node_modules", "dist"))
    subprocess.run(["tsc", "-p", str(source / "tsconfig.json")], check=True)
    result = subprocess.run(["npm", "pack", "--ignore-scripts", "--offline", "--json",
        "--cache", str(tmp_path / "npm-cache"), "--pack-destination", str(tmp_path)],
        cwd=source, check=True, capture_output=True, text=True)
    tarball = tmp_path / json.loads(result.stdout)[0]["filename"]
    unpacked = tmp_path / "unpacked"
    with tarfile.open(tarball) as archive:
        archive.extractall(unpacked, filter="data")
    package = tmp_path / "node_modules/@astrid/runtime-client"
    package.parent.mkdir(parents=True)
    shutil.move(unpacked / "package", package)
    shutil.rmtree(source)
    shutil.copyfile(ROOT / "tests/fixtures/timeline-producer-types.mts", tmp_path / "consumer.mts")
    old = (ROOT / "tests/fixtures/timeline-bundle2-types.mts").read_text().replace(
        "../../packages/typescript/src/index.js", "@astrid/runtime-client")
    (tmp_path / "old-consumer.mts").write_text(old)
    subprocess.run(["tsc", "--noEmit", "--strict", "--module", "NodeNext", "--target", "ES2022",
        "consumer.mts", "old-consumer.mts"], cwd=tmp_path, check=True)
    (tmp_path / "consumer.mjs").write_text('''
import assert from "node:assert/strict";
import { WorkspaceClient } from "@astrid/runtime-client";
const digest = "sha256:" + "a".repeat(64);
const target = { project_id: "p", timeline_id: "t", base_revision_id: "r", base_publication_id: "receipt" };
const pin = { task_id: "task", attempt_id: "attempt", executor_id: "worker", fence: 1, runtime_epoch: 1, admitted_target: target, proposal_digest: digest };
const request = { api_version: 1, ...target, commands: [{ schema_version: 1, op: "producer.guard", version: "1", select: null, args: { pin } }, { schema_version: 1, op: "clip.move", version: "1", select: "parent/clip:c", args: { on: 1.0 }, expect: { opaque: { state: "present", value: [null, 1.5] } } }], rationale: "Reviewed — 🎬" };
const accepted = { data: { status: "accepted" }, receipt: { receipt_id: "accepted" } };
const calls = [];
const transport = async (method, path, headers, body) => {
  calls.push({ method, path, headers, body: JSON.parse(new TextDecoder().decode(body)) });
  return { status: 200, headers: {}, body: new TextEncoder().encode(JSON.stringify(accepted)) };
};
const client = new WorkspaceClient("http://runtime", "token", transport);
assert.deepEqual(await client.commitTimeline("p", "t", request, "original-key"), accepted);
assert.deepEqual(calls.at(-1).body, request);
assert.equal(calls.at(-1).headers["Idempotency-Key"], "original-key");
''')
    subprocess.run(["node", "consumer.mjs"], cwd=tmp_path, check=True)
