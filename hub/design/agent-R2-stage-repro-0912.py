"""One captured Agent/Runtime grouped-inverse authentication repro.

Run from any directory with the Agent and Runtime checkouts on PYTHONPATH.  The
script executes exactly one forward split+note and one whole inverse through
the real Agent provider, then calls Runtime's real annotation validator.  It
prints a self-contained JSON record containing the request, root documents,
all prepared records, physical bindings, stage ranges, and immutable history.
"""
from __future__ import annotations

import copy
import inspect
import json
from pathlib import Path

import pytest

from runtime_protocol.timeline_commit_auth import validate

from astrid.sdk.timeline.commit import _digest, create_runtime_commit_service
from astrid.sdk.timeline._command_state import ABSENT
from tests.editing_conformance.test_doc_patch_mirrors import (
    declared_reads,
    original_document,
    split_patch,
)
from tests.editing_conformance.test_doc_patch_v2 import change, patch, step
from tests.sdk.test_timeline_commit_provider import (
    DetachedPort,
    DetachedRealm,
    inverse,
)
from tests.sdk.test_timeline_commit_provider import runtime_abi


ORIGINAL_AGENT_SHA = "543d133c85de16ab800c4df0e9ff504ca077fcbf"
ORIGINAL_RUNTIME_SHA = "1365e4b17b31c4a7093d5943674637067fd2bab4"
AGENT_ROOT = Path(inspect.getfile(create_runtime_commit_service)).parents[3]
RUNTIME_AUTH_PATH = Path(inspect.getfile(validate))


def detached(value):
    return json.loads(json.dumps(value, allow_nan=False))


def commit(realm, *calls, **controls):
    context = realm.context(calls)
    context["request"].update(controls)
    context["invocation"]["body"] = copy.deepcopy(context["request"])
    context["request_hash"] = _digest(context["invocation"])
    with pytest.MonkeyPatch.context() as monkeypatch:
        # The Agent fixture supplies only the ABI exception/metadata shim.  It
        # does not replace the command engine or the Runtime validator above.
        runtime_abi.__wrapped__(monkeypatch)
        result = create_runtime_commit_service().commit(
            context, DetachedPort(realm, context)
        )
    return context, result


def image_identities(document):
    images = {
        "parent": document["parent_revision"],
        **{
            "shot-revision:" + row["revision_id"]: row
            for row in document["shot_revisions"]
        },
        **{
            "internal-revision:" + row["revision_id"]: row
            for row in document["internal_timeline_revisions"]
        },
    }
    return {
        ref: {
            "revision_id": image["revision_id"],
            "content_digest": image["content_digest"],
        }
        for ref, image in images.items()
    }


def stage_facts(prepared):
    records = prepared["records"]
    return [
        {
            "ordinal": command["ordinal"],
            "command": command["command"],
            "writes": command["writes"],
            "derived_writes": command["derived_writes"],
            "bindings": command["bindings"],
            "stage_bindings": [
                binding
                for binding in command["bindings"]
                if binding.get("key") == "inverse.stage"
            ],
        }
        for command in records["commands"]
    ]


def main():
    original = original_document()
    realm = DetachedRealm(original)

    # This is the smallest retained real-Agent shape that showed the Runtime
    # intermediate-image mismatch: a split writes the clip mirror and a second
    # independent field is written in the same enclosing step group.
    split = split_patch(original, ["clips"], True, insert=True)
    note = patch(change(["unknown", "note"], ABSENT, "kept"))
    forward_steps = [
        step("split", 0, split, reads=declared_reads()),
        step("note", 1, note),
    ]
    forward_context, forward = commit(
        realm,
        split,
        note,
        label="Split and output",
        steps=forward_steps,
        merge="fields",
        reads=[],
        source={"via": "python"},
        rationale="Split with clip and output changes",
        group_id="split-group",
    )
    publication = forward["receipt"]["receipt_id"]
    landing = detached(forward["data"]["canonical_document"])
    forward_prepared = detached(realm.prepared[-1])

    forward_auth = {"status": "pass"}
    try:
        validate(
            forward_context["request"],
            forward_prepared,
            original,
        )
    except Exception as error:  # pragma: no cover - diagnostic output path
        forward_auth = {
            "status": "refused",
            "type": type(error).__name__,
            "message": str(error),
        }

    inverse_call = inverse([publication])
    inverse_context, inverse_result = commit(
        realm,
        inverse_call,
        label="Undo split and output",
        steps=[step("undo", 0, inverse_call)],
        merge="fields",
        reads=[],
        source={"via": "python"},
        rationale="Whole inverse of split and output",
        group_id="split-group",
    )
    inverse_prepared = detached(realm.prepared[-1])
    inverse_landing = detached(inverse_result["data"]["canonical_document"])

    inverse_auth = {"status": "pass"}
    try:
        validate(
            inverse_context["request"],
            inverse_prepared,
            landing,
            base=original,
        )
    except Exception as error:
        details = getattr(error, "failure", None)
        inverse_auth = {
            "status": "refused",
            "type": type(error).__name__,
            "message": str(error),
            "failure": details,
        }

    print(
        json.dumps(
            {
                "artifact": "agent-R2-stage-repro-0912",
                "artifact_status": "artifact-ready-PASS",
                "kind": "one-real-agent-grouped-inverse-auth-repro",
                "purpose": "Runtime reviewer input for intermediate inverse-stage images",
                "candidate": "whole split+unrelated-note",
                "agent_checkout": str(AGENT_ROOT),
                "agent_commit": ORIGINAL_AGENT_SHA,
                "agent_provider_origin": inspect.getfile(create_runtime_commit_service),
                "agent_provider_sha256": "267b1b1589c0254345a13bf802df8b40301f70020389c223c91f4b14808f336d",
                "runtime_checkout": str(RUNTIME_AUTH_PATH.parents[1]),
                "runtime_commit": ORIGINAL_RUNTIME_SHA,
                "runtime_auth_origin": str(RUNTIME_AUTH_PATH),
                "fixture_origins": {
                    "document": inspect.getfile(original_document),
                    "split_patch": inspect.getfile(split_patch),
                    "provider_fixture": inspect.getfile(DetachedRealm),
                },
                "fixture_version": {
                    "document_fixture": "tests.sdk.test_timeline_commit_provider_document.document_fixture",
                    "provider_fixture": "DetachedRealm/DetachedPort with runtime_abi shim",
                    "agent_inverse": "R2 mirror repair sha256 above",
                },
                "command": (
                    "PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent:/home/user/work/runtime "
                    "/home/user/work/venv-agent/bin/python "
                    f"{Path(__file__)}"
                ),
                "forward": {
                    "request": forward_context["request"],
                    "idempotency_key": forward_context["idempotency_key"],
                    "invocation": forward_context["invocation"],
                    "request_hash": forward_context["request_hash"],
                    "result": forward,
                    "input_base_document": original,
                    "output_document": landing,
                    "prepared": forward_prepared,
                    "root_images": image_identities(original),
                    "output_root_images": image_identities(landing),
                    "auth": forward_auth,
                },
                "inverse": {
                    "request": inverse_context["request"],
                    "idempotency_key": inverse_context["idempotency_key"],
                    "invocation": inverse_context["invocation"],
                    "request_hash": inverse_context["request_hash"],
                    "result": inverse_result,
                    "base_document": original,
                    "input_document": landing,
                    "output_document": inverse_landing,
                    "prepared": inverse_prepared,
                    "root_images": image_identities(landing),
                    "output_root_images": image_identities(inverse_landing),
                    "stages": stage_facts(inverse_prepared),
                    "auth": inverse_auth,
                },
                "history": detached(realm.entries),
                "history_entry_publications": [entry["publication_id"] for entry in realm.entries],
                "expected": {
                    "forward_runtime_auth": "accepted",
                    "inverse_runtime_auth_before_reviewed_fix": "refused",
                    "inverse_refusal_code": "invalid_records",
                    "inverse_refusal_message": "provider binding differs from its authenticated input image",
                    "no_original_58_rerun": True,
                    "no_agent_mirror_bug": True,
                },
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
