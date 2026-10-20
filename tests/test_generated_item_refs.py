from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import get_type_hints

import pytest

from runtime_protocol.errors import ValidationError
from runtime_protocol.timeline_commit_validation import validate_commit_value
from test_timeline_commit_validation import prepared, request

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = "10c1610b61ad151259149c97061493d9e36ae0a9220ba4983b45f22e8ac7e3b1"


def item_request():
    value = request()
    value["commands"][0].update(
        resolved=["occurrence:O/clip:C", "shot:S/item:I"],
        created=["shot:D", "shot:D/item:J"],
        bindings={
            "materialization.owner:shot:D": "occurrence:O",
            "materialization.source:shot:D": "shot:S/item:I",
        },
        expect={"shot:S/item:I::metadata": {"state": "absent"}},
        authorship={"shot:D/item:J::": "consequence"},
    )
    return value


def test_frozen_schema_bytes_and_installed_projection():
    raw = (ROOT / "contract/schemas/edit-command.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256
    bundle = json.loads(
        (ROOT / "runtime_protocol/schemas/timeline-commit-bundle.json").read_text()
    )
    assert bundle["resources"][
        "https://astrid.haus/workspace/v1/schemas/edit-command.json"
    ] == json.loads(raw)


def test_item_claims_and_flat_allocation_map_preserve_wire_shape():
    value = item_request()
    before = copy.deepcopy(value)
    validate_commit_value(value, "CommitRequest")
    assert value == before == json.loads(json.dumps(value))
    candidate = prepared()
    candidate["records"]["commands"][0]["command"] = value["commands"][0]
    candidate["id_map"] = {"shot:D": "D", "shot:D/item:J": "J"}
    validate_commit_value(candidate, "PreparedCommit")
    assert candidate["id_map"] == {"shot:D": "D", "shot:D/item:J": "J"}


@pytest.mark.parametrize(
    "field, value",
    [
        ("resolved", ["shot:S/item:"]),
        ("resolved", ["shot:/item:I"]),
        ("resolved", ["shot:S/item:I/extra"]),
        ("resolved", ["shot:S::other/item:I"]),
        ("created", ["shot:D/item:"]),
        ("created", [True]),
        ("bindings", {"source": "shot:S/item:"}),
        ("bindings", {"source": "shot:S/item:I::bad"}),
        ("bindings", {"source": True}),
        ("expect", {"shot:S/item:::at": {"state": "absent"}}),
        ("authorship", {"shot:D/item:::at": "direct"}),
        ("schema_version", True),
        ("unknown", None),
    ],
)
def test_malformed_item_claims_are_refused(field, value):
    body = item_request()
    body["commands"][0][field] = value
    with pytest.raises(ValidationError):
        validate_commit_value(body, "CommitRequest")


@pytest.mark.parametrize("field", ["on", "ordinal", "cause"])
def test_boolean_numbers_are_refused_with_item_claims(field):
    value = prepared()
    record = value["records"]["commands"][0]
    record["command"] = item_request()["commands"][0]
    if field == "on":
        record["command"]["args"]["on"] = True
    elif field == "ordinal":
        record["ordinal"] = True
    else:
        record["derived_writes"] = [{
            "ref": "shot:D/item:J", "path": [],
            "before": {"state": "absent"},
            "after": {"state": "present", "value": None}, "cause": True,
        }]
    with pytest.raises(ValidationError):
        validate_commit_value(value, "PreparedCommit")


def test_generated_nested_arguments_have_resolvable_types():
    from astrid_runtime_client import ClipAddArgs, ClipDeleteArgs, TrackSetArgs
    from astrid_runtime_client import timeline_commit_types as dto

    assert get_type_hints(ClipAddArgs)["row"] is dto.ClipAddArgsRow
    assert dto.ClipAddArgsRow.__required_keys__ == {"id", "clipType", "track", "at", "hold"}
    assert ClipDeleteArgs.__annotations__ == {}
    for variant in TrackSetArgs.__args__:
        # Forward references are resolved by the containing generated DTO.
        assert get_type_hints(getattr(dto, variant.__forward_arg__))["clear"]


def test_isolated_client_wheel_imports_and_preserves_item_claims(tmp_path):
    source = tmp_path / "source"
    shutil.copytree(ROOT / "packages/python", source,
                    ignore=shutil.ignore_patterns("__pycache__", "*.egg-info", "build"))
    wheels = tmp_path / "wheels"
    subprocess.run([
        sys.executable, "-m", "pip", "wheel", "--no-index", "--no-deps",
        "--no-build-isolation", "--no-cache-dir", "--wheel-dir", str(wheels), str(source),
    ], check=True, capture_output=True)
    (wheel,) = wheels.glob("astrid_runtime_client-*.whl")
    target = tmp_path / "installed"
    subprocess.run([
        sys.executable, "-m", "pip", "install", "--no-index", "--no-deps",
        "--no-compile", "--target", str(target), str(wheel),
    ], check=True, capture_output=True)
    shutil.rmtree(source)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "request.json").write_text(json.dumps(item_request()))
    probe = """
import json, pathlib
from astrid_runtime_client import (
    CONTRACT_VERSION, WorkspaceClient, Health, MutationResult, EditCommand,
    ScopedId, EntityRef, TargetKey, AnchorIdentity, AgentBinding, AgentCreatedID,
    ClipAddArgs, ClipDeleteArgs, TrackSetArgs, CommitRequest,
)
import astrid_runtime_client
assert pathlib.Path(astrid_runtime_client.__file__).is_relative_to(pathlib.Path('..') / 'installed')
assert CONTRACT_VERSION == '0.2.5'
body = json.loads(pathlib.Path('request.json').read_text())
calls = []
def transport(method, path, headers, data):
    calls.append(json.loads(data))
    return 200, {}, b'{"data":{"status":"accepted"},"receipt":{"receipt_id":"txn"}}'
client = WorkspaceClient('http://runtime.invalid', transport=transport)
client.commit_timeline('p', 't', body, idempotency_key='key')
assert calls == [body]
assert body['commands'][0]['created'] == ['shot:D', 'shot:D/item:J']
""".replace("pathlib.Path('..') / 'installed'", "pathlib.Path(" + repr(str(target)) + ")")
    subprocess.run([sys.executable, "-c", probe], cwd=outside, check=True,
                   env={**os.environ, "PYTHONPATH": str(target), "PYTHONDONTWRITEBYTECODE": "1"},
                   capture_output=True)


def test_offline_packed_typescript_root_imports(tmp_path):
    source = tmp_path / "source"
    shutil.copytree(ROOT / "packages/typescript", source,
                    ignore=shutil.ignore_patterns("dist", "node_modules"))
    subprocess.run(["tsc", "-p", str(source / "tsconfig.json")], check=True)
    packed = subprocess.run(["npm", "pack", "--ignore-scripts", "--json"],
                            cwd=source, check=True, text=True, capture_output=True)
    tarball = source / json.loads(packed.stdout)[0]["filename"]
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    (consumer / "package.json").write_text('{"private":true,"type":"module"}')
    subprocess.run(["npm", "install", "--offline", "--ignore-scripts", "--no-audit",
                    "--no-fund", str(tarball)], cwd=consumer, check=True, capture_output=True)
    shutil.rmtree(source)
    (consumer / "consumer.mts").write_text('''
import { CONTRACT_VERSION, WorkspaceClient, type Health, type MutationResult,
  type EditCommand, type CommitRequest, type ScopedId, type AnchorIdentity,
  type TargetKey, type EntityRef, type AgentBinding, type AgentCreatedID,
  type ClipAddArgs, type ClipDeleteArgs, type TrackSetArgs,
} from "@astrid/runtime-client";
const version: "0.2.5" = CONTRACT_VERSION;
const ref: ScopedId = "shot:D/item:J";
const source: AnchorIdentity = "shot:S/item:I";
const entity: EntityRef = source;
const path: TargetKey = `${source}::metadata`;
const binding: AgentBinding = { key: "source", ref: source, policy: "fixed", dependencies: [] };
const created: AgentCreatedID = { ref, kind: "item", owner: "shot:D" };
const row: ClipAddArgs = { row: { id: "c", clipType: "text", track: "v", at: 0, hold: 1, opaque: null } };
const label: TrackSetArgs = { values: { label: "Video" }, clear: [] };
const empty: ClipDeleteArgs = {};
// @ts-expect-error closed empty args reject unknown fields
const invalid: ClipDeleteArgs = { unknown: true };
const command: EditCommand = { schema_version: 1, op: "clip.move", version: "1",
  select: "parent/clip:c", args: { on: 1 }, created: [ref],
  resolved: [source], bindings: { source }, expect: { [path]: { state: "absent" } } };
const request: CommitRequest = { api_version: 1, project_id: "p", timeline_id: "t",
  base_revision_id: "r", base_publication_id: "txn", commands: [command] };
const client = new WorkspaceClient("http://runtime.invalid");
const health: Promise<Health> = client.health();
const old: Promise<MutationResult<unknown>> = client.createProject("old", "key");
void [version, entity, binding, created, row, label, empty, invalid, request, health, old];
''')
    subprocess.run(["tsc", "--noEmit", "--strict", "--module", "NodeNext",
                    "--target", "ES2022", "consumer.mts"], cwd=consumer, check=True)
    subprocess.run(["node", "--input-type=module", "-e",
                    'import { CONTRACT_VERSION, WorkspaceClient } from "@astrid/runtime-client"; '
                    'if (CONTRACT_VERSION !== "0.2.5" || typeof WorkspaceClient !== "function") throw Error("exports");'],
                   cwd=consumer, check=True)
