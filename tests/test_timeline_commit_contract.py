from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import get_type_hints

import pytest
import yaml
from astrid_runtime_client import ApiError, WorkspaceClient
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from runtime_protocol.timeline_commit import (
    CommitRejected,
    CommitRequest,
    RuntimeCommitPort,
    StaleHead,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "contract/schemas/timeline-commit.json").read_text())
DIGEST = "sha256:" + "a" * 64


def validator(name):
    registry = Registry()
    for path in (ROOT / "contract/schemas").glob("*.json"):
        schema = json.loads(path.read_text())
        if "$schema" not in schema:
            continue
        resource = Resource.from_contents(schema)
        registry = registry.with_resource(
            "https://astrid.haus/workspace/v1/schemas/" + path.name, resource
        )
        if "$id" in schema:
            registry = registry.with_resource(schema["$id"], resource)
    openapi = yaml.safe_load((ROOT / "contract/openapi/workspace-v1.yaml").read_text())
    registry = registry.with_resource(
        "https://astrid.haus/workspace/v1/openapi/workspace-v1.yaml",
        Resource.from_contents(openapi, default_specification=DRAFT202012),
    )
    return Draft202012Validator(
        {"$ref": SCHEMA["$id"] + "#/$defs/" + name}, registry=registry
    )


def command():
    return dict(
        schema_version=1,
        op="clip.move",
        version="1",
        select="parent/clip:c",
        args={"on": 2},
    )


def request():
    return dict(
        api_version=1,
        project_id="p",
        timeline_id="t",
        base_revision_id="r",
        base_publication_id="txn",
        commands=[command()],
    )


def document():
    return dict(
        schema_version=1,
        project_id="p",
        timeline_id="t",
        parent_revision=dict(
            revision_id="r",
            content_digest=DIGEST,
            payload=dict(
                config={"clips": [], "tracks": []},
                registry={},
                clips=[],
                occurrences=[],
                opaque={"null": None, "clear": {"op": "clear"}},
            ),
        ),
        shot_revisions=[],
        internal_timeline_revisions=[],
        dependency_manifest=dict(
            shots=[], internal_timelines=[], media=[], documents=[]
        ),
    )


def test_schema_pin_and_generated_dtos_are_identical():
    # Pin authority is the packaged Agent artifact after integration. The frozen
    # schema identity remains stable and the bytes are part of SCHEMA_DIGEST.
    agent = json.loads((ROOT / "contract/schemas/edit-command.json").read_text())
    assert (
        agent["$id"] == "https://astrid.local/schemas/timeline/edit-command.schema.json"
    )
    Draft202012Validator.check_schema(agent)
    Draft202012Validator.check_schema(SCHEMA)
    assert (ROOT / "runtime_protocol/timeline_commit_types.py").read_bytes() == (
        ROOT / "packages/python/astrid_runtime_client/timeline_commit_types.py"
    ).read_bytes()
    assert CommitRequest.__required_keys__ == {
        "api_version",
        "project_id",
        "timeline_id",
        "base_revision_id",
        "base_publication_id",
        "commands",
    }


def test_command_opaque_values_null_and_absence_round_trip():
    value = request()
    value["commands"] = [
        dict(
            schema_version=1,
            op="vendor.decorate",
            version="1",
            select=None,
            args={"opaque": {"op": "clear", "$absent": True, "nested": [None]}},
            expect={
                "params": {"state": "present", "value": None},
                "old": {"state": "absent"},
            },
        )
    ]
    original = copy.deepcopy(value)
    validator("CommitRequest").validate(value)
    assert json.loads(json.dumps(value, allow_nan=False)) == original
    assert "dry_run" not in value
    validator("CanonicalDocument").validate(document())


@pytest.mark.parametrize(
    "mutate",
    [
        lambda v: v.update(unknown=True),
        lambda v: v.update(api_version=True),
        lambda v: v.update(base_publication_id=None),
        lambda v: v.update(commands=[]),
        lambda v: v.update(source={"via": "gateway"}),
        lambda v: v["commands"][0].update(unknown=True),
        lambda v: v["commands"][0].pop("version"),
        lambda v: v["commands"][0].update(
            expect={"at": {"state": "absent", "value": None}}
        ),
    ],
)
def test_closed_request_rejects_unknown_missing_or_invalid_fields(mutate):
    value = request()
    mutate(value)
    assert not validator("CommitRequest").is_valid(value)


def test_restore_is_sole_command_and_requires_both_head_guards():
    value = request()
    restore = dict(
        schema_version=1,
        op="timeline.restore",
        version="1",
        select=None,
        args={"revision_id": "old", "content_digest": DIGEST},
    )
    value["commands"] = [restore]
    validator("CommitRequest").validate(value)
    value["commands"].append(command())
    assert not validator("CommitRequest").is_valid(value)
    for invalid in (
        {"expected_head": "r"},
        {"expected_head": None, "expected_publication_id": "txn"},
        {"expected_head": "r", "expected_publication_id": "txn", "document": {}},
    ):
        assert not validator("RestoreParentCompositionRevision").is_valid(invalid)
    validator("RestoreParentCompositionRevision").validate(
        {"expected_head": "r", "expected_publication_id": "txn"}
    )


def test_recorders_retain_execution_ordinal_and_all_leaf_families():
    record = dict(
        ordinal=0,
        command=command(),
        writes=[
            dict(
                ref="parent/clip:c",
                path=["at"],
                before={"state": "present", "value": 2},
                after={"state": "present", "value": 2},
            )
        ],
        reads=[],
        selections=[],
        bindings=[],
        created=[],
        dependencies=[],
        derived_writes=[],
    )
    recorder = dict(schema_version=1, commands=[record], undo_of=[], restored_from=None)
    validator("Recorder").validate(recorder)
    for invalid in (-1, True, 0.5):
        record["ordinal"] = invalid
        assert not validator("Recorder").is_valid(recorder)
    record["ordinal"] = 0
    record["derived_writes"] = [
        dict(
            ref="parent/clip:c",
            path=["compiled"],
            before={"state": "absent"},
            after={"state": "present", "value": None},
            cause=0,
        )
    ]
    validator("Recorder").validate(recorder)
    record["derived_writes"][0]["cause"] = -1
    assert not validator("Recorder").is_valid(recorder)
    # Contiguous ordinals, dependency keys and cause references require semantic
    # acceptance checks; JSON Schema cannot compare sibling array values.


def test_detached_errors_and_port_signatures():
    pin = {"revision_id": "r", "publication_id": "txn"}
    failure = dict(
        http_status=409,
        code="conflict",
        message="changed",
        details=dict(
            status="conflict", reason="overlap", base=pin, current=pin, conflicts=[]
        ),
    )
    rejected, stale = CommitRejected(failure), StaleHead(pin)
    failure["details"]["base"]["revision_id"] = "changed"
    assert rejected.failure["details"]["base"]["revision_id"] == "r"
    assert stale.current_head["revision_id"] == "r"
    for method in [
        "head",
        "revision_closure",
        "shot_closure",
        "history",
        "history_entry",
        "selected_media",
        "transcript_source",
        "config_source",
        "narration_take",
        "preview",
        "accept",
    ]:
        assert get_type_hints(getattr(RuntimeCommitPort, method))
    code = "import sys; from runtime_protocol.timeline_commit import RuntimeCommitPort, CommitRequest; assert not any(n.startswith(('astrid.', 'remotion', 'composition', 'jsonschema')) for n in sys.modules)"
    subprocess.run(
        [sys.executable, "-S", "-c", code],
        cwd=ROOT,
        env={**os.environ, "PATH": "", "PYTHONPATH": str(ROOT)},
        check=True,
    )


@pytest.mark.parametrize("preview", [False, True])
def test_generated_python_commit_preserves_exact_envelope_and_retry(preview):
    value = request()
    if preview:
        value["dry_run"] = True
    response = {
        "data": {"status": "preview" if preview else "accepted", "opaque": None},
        "receipt": None if preview else {"receipt_id": "txn"},
    }
    calls = []

    def transport(method, path, headers, body):
        calls.append((method, path, headers, body))
        return 200, {}, json.dumps(response).encode()

    client = WorkspaceClient("http://runtime", "token", transport=transport)
    assert client.commit_timeline("p", "t", value, idempotency_key="retry") == response
    assert client.commit_timeline("p", "t", value, idempotency_key="retry") == response
    assert calls[0][:2] == calls[1][:2]
    assert calls[0][3] == calls[1][3]
    assert calls[0][2]["Idempotency-Key"] == calls[1][2]["Idempotency-Key"]
    assert calls[0][0:2] == ("POST", "/v1/projects/p/timelines/t/commit")
    assert json.loads(calls[0][3]) == value
    assert calls[0][2]["Idempotency-Key"] == "retry"


@pytest.mark.parametrize("number", [float("nan"), float("inf"), -float("inf")])
def test_generated_python_refuses_nonfinite_even_in_opaque_values(number):
    value = request()
    value["commands"][0]["args"]["on"] = number

    def transport(*args):
        pytest.fail("nonfinite input reached transport")

    with pytest.raises(ValueError):
        WorkspaceClient("http://runtime", transport=transport).commit_timeline(
            "p", "t", value, idempotency_key="key"
        )


def test_generated_python_rejects_mismatched_preview_and_preserves_errors():
    def transport(*args):
        return 200, {}, b'{"data":{"status":"preview"},"receipt":null}'

    client = WorkspaceClient("http://runtime", transport=transport)
    with pytest.raises(ApiError, match="acceptance"):
        client.commit_timeline("p", "t", request(), idempotency_key="key")

    def conflict(*args):
        return (
            409,
            {},
            b'{"code":"conflict","message":"changed","details":{"reason":"overlap","conflicts":[]}}',
        )

    with pytest.raises(ApiError) as caught:
        WorkspaceClient("http://runtime", transport=conflict).commit_timeline(
            "p", "t", request(), idempotency_key="key"
        )
    assert caught.value.details["reason"] == "overlap"


def test_verified_media_public_contract_and_generated_python_adapter():
    from urllib.parse import parse_qs, urlsplit

    from astrid_runtime_client import MediaSelection, VerifiedMedia

    openapi = yaml.safe_load((ROOT / "contract/openapi/workspace-v1.yaml").read_text())
    operation = openapi["paths"]["/v1/projects/{project_id}/media-selection/verified"]["get"]
    assert operation["operationId"] == "getProjectVerifiedMedia"
    parameters = [parameter for parameter in operation["parameters"] if parameter.get("in") == "query"]
    assert {parameter["name"] for parameter in parameters} == MediaSelection.__required_keys__
    assert all(parameter["required"] for parameter in parameters)
    assert openapi["components"]["schemas"]["VerifiedMedia"] == {
        "$ref": "./schemas/timeline-commit.json#/$defs/VerifiedMedia",
    }
    assert get_type_hints(WorkspaceClient.get_project_verified_media) == {
        "project_id": str, "selection": MediaSelection, "return": VerifiedMedia,
    }
    selection = {"asset": "alias/ &", "generation_id": "g", "variant_id": "v",
                 "object_id": DIGEST, "catalog_digest": DIGEST}
    response = {"selection": selection, "media_type": "video/mp4", "size": 42, "duration_seconds": 2}
    calls = []

    def transport(method, path, headers, body):
        calls.append(path)
        assert method == "GET" and body is None
        assert headers["Authorization"] == "Bearer token"
        assert "Idempotency-Key" not in headers
        assert urlsplit(path).path == "/v1/projects/project%2Fone/media-selection/verified"
        assert parse_qs(urlsplit(path).query) == {key: [value] for key, value in selection.items()}
        return 200, {}, json.dumps(response).encode()

    assert WorkspaceClient("http://runtime", "token", transport=transport).get_project_verified_media("project/one", selection) == response
    assert len(calls) == 1
    assert validator("VerifiedMedia").is_valid(response)


def test_generated_python_history_media_and_restore_adapters():
    calls = []

    def transport(method, path, headers, body):
        calls.append((method, path, headers, body))
        if "/commits?" in path:
            value = {
                "items": [],
                "next_cursor": None,
                "head": {"revision_id": "r", "publication_id": "txn"},
            }
        elif "/media-selection?" in path:
            value = {
                "asset": "a",
                "generation_id": "g",
                "variant_id": "v",
                "object_id": DIGEST,
                "catalog_digest": DIGEST,
            }
        else:
            value = {
                "data": {"status": "accepted"},
                "receipt": {"receipt_id": "restore"},
            }
        return 200, {}, json.dumps(value).encode()

    client = WorkspaceClient("http://runtime", transport=transport)
    assert (
        client.list_timeline_commits("p", "t", cursor="a/b")["head"]["publication_id"]
        == "txn"
    )
    assert "cursor=a%2Fb" in calls[-1][1]
    assert (
        client.get_project_media_selection(
            "p", {"asset": "a", "generation_id": "g", "variant_id": "v"}
        )["asset"]
        == "a"
    )
    assert (
        client.restore_project_parent_composition_revision(
            "p",
            "t",
            "old",
            expected_head="r",
            expected_publication_id="txn",
            idempotency_key="restore",
        )["receipt"]["receipt_id"]
        == "restore"
    )
    assert json.loads(calls[-1][3]) == {
        "expected_head": "r",
        "expected_publication_id": "txn",
    }


@pytest.mark.parametrize(
    "value",
    [
        {},
        {"asset": "a"},
        {"asset": "a", "generation_id": "g", "variant_id": "v", "version": 1},
    ],
)
def test_media_selection_requires_exactly_one_selector_form(value):
    assert not validator("MediaSelectionQuery").is_valid(value)


def test_generated_typescript_commit_contract(tmp_path):
    output = tmp_path / "client"
    subprocess.run(
        [
            "tsc",
            "-p",
            str(ROOT / "packages/typescript/tsconfig.json"),
            "--outDir",
            str(output),
        ],
        check=True,
    )
    (output / "package.json").write_text('{"type":"module"}')
    script = tmp_path / "commit.mjs"
    script.write_text(
        "import { WorkspaceClient } from "
        + json.dumps((output / "generated.js").as_uri())
        + ";\n"
        + r"""
import assert from "node:assert/strict";
const request = { api_version: 1, project_id: "p", timeline_id: "t", base_revision_id: "r", base_publication_id: "txn", commands: [{ schema_version: 1, op: "vendor.decorate", version: "1", select: null, args: { opaque: [null, { op: "clear" }] } }] };
const calls = [];
let response = { data: { status: "accepted", opaque: null }, receipt: { receipt_id: "accepted" } };
const transport = async (method, path, headers, body) => {
  calls.push({ method, path, headers, body: body ? JSON.parse(new TextDecoder().decode(body)) : null });
  return { status: 200, headers: {}, body: new TextEncoder().encode(JSON.stringify(response)) };
};
const client = new WorkspaceClient("http://runtime", "token", transport);
assert.deepEqual(await client.commitTimeline("p", "t", request, "key"), response);
assert.deepEqual(calls.at(-1).body, request);
assert.equal(calls.at(-1).headers["Idempotency-Key"], "key");
response = { data: { status: "preview" }, receipt: null };
assert.deepEqual(await client.commitTimeline("p", "t", { ...request, dry_run: true }, "preview"), response);
await assert.rejects(client.commitTimeline("p", "t", request, "key"), /invalid commit/);
for (const number of [NaN, Infinity, -Infinity]) {
  const invalid = structuredClone(request);
  invalid.commands[0].args.opaque.push(number);
  const count = calls.length;
  await assert.rejects(client.commitTimeline("p", "t", invalid, "key"), /nonfinite/);
  assert.equal(calls.length, count);
}
response = { items: [], next_cursor: null, head: { revision_id: "r", publication_id: "txn" } };
assert.deepEqual(await client.listTimelineCommits("p", "t", "a/b"), response);
assert.match(calls.at(-1).path, /cursor=a%2Fb/);
response = { asset: "a", generation_id: "g", variant_id: "v", object_id: "object", catalog_digest: "digest" };
assert.deepEqual(await client.getProjectMediaSelection("p", { asset: "a", generation_id: "g", variant_id: "v" }), response);
response = { data: { status: "rebased" }, receipt: { receipt_id: "restore" } };
assert.deepEqual(await client.restoreProjectParentCompositionRevision("p", "t", "old", "r", "txn", "restore"), response);
assert.deepEqual(calls.at(-1).body, { expected_head: "r", expected_publication_id: "txn" });
"""
    )
    subprocess.run(["node", str(script)], check=True)


def test_prepared_and_response_shapes_share_closure_and_main_receipt():
    candidate = {
        "canonical_document": document(),
        "document_digest": DIGEST,
        "commands": [command()],
        "id_map": {},
        "provider_version": "1",
        "compiler_version": "1",
    }
    head = {"revision_id": "r", "publication_id": "txn"}
    accepted = {
        "status": "accepted",
        "base_revision_id": "r",
        "base_publication_id": "txn",
        "previous_revision_id": "r",
        "previous_publication_id": "txn",
        "accepted_revision_id": "next",
        "rebased_onto": None,
        "publisher": "actor",
        **candidate,
    }
    receipt = {
        "receipt_id": "accepted",
        "command_kind": "timeline.commit",
        "idempotency_key": "key",
        "request_hash": DIGEST,
        "project_id": "p",
        "project_seq": [1, 1],
        "event_ids": [],
        "result": accepted,
        "created_at": "2026-10-19T00:00:00Z",
    }
    response = {"data": accepted, "receipt": receipt}
    validator("CommitAcceptedMutation").validate(response)
    response["receipt"] = None
    assert not validator("CommitAcceptedMutation").is_valid(response)
    preview = {
        "data": {
            "status": "preview",
            "base_revision_id": "r",
            "base_publication_id": "txn",
            "evaluated_head": head,
            **candidate,
        },
        "receipt": None,
    }
    validator("CommitPreviewResponse").validate(preview)
    preview["data"]["accepted_revision_id"] = "forbidden"
    assert not validator("CommitPreviewResponse").is_valid(preview)
    prepared = {
        "expected_head": head,
        **{key: value for key, value in candidate.items() if key != "commands"},
        "records": {
            "schema_version": 1,
            "commands": [],
            "undo_of": [],
            "restored_from": None,
        },
        "semantic_events": [],
    }
    validator("PreparedCommit").validate(prepared)
    prepared["commands"] = candidate["commands"]
    assert not validator("PreparedCommit").is_valid(prepared)


def test_all_generated_dto_annotations_resolve():
    from runtime_protocol import timeline_commit_types as dto

    for name, value in vars(dto).items():
        if isinstance(value, type) and hasattr(value, "__required_keys__"):
            assert set(get_type_hints(value)) == value.__required_keys__ | value.__optional_keys__, name
    assert dto.TimelineCommitPage(items=[], next_cursor=None, head={}) == {
        "items": [],
        "next_cursor": None,
        "head": {},
    }
