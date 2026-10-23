"""Bounded retained split+note probe through real Runtime acceptance.

This is a corrected, separately named copy of ``agent-R2-stage-repro-0912.py``.
It deliberately uses the production Runtime store and Agent provider.  The
inverse validator receives only the forward record read back through
``TimelineCommitStore.history_entry``; it never receives detached fixture
authority or the inverse record itself.
"""
from __future__ import annotations

import copy
import hashlib
import inspect
import json
import sys
import tempfile
from pathlib import Path

from astrid.sdk.timeline._command_state import ABSENT, present
from astrid.sdk.timeline.commit import create_runtime_commit_service
from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit_auth import validate
from runtime_protocol.timeline_commit_port import RequestCommitPort, route_path
from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider


ORIGINAL_REPRO = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/"
    "agent-R2-stage-repro-0912.py"
)
ORIGINAL_REPRO_SHA256 = "47399344d70ecb35bca0f843aea5c7245cae35a623cdbbcfd777465d47810f8a"
RUNTIME_AUTH_PATH = Path(inspect.getfile(validate)).resolve()
RUNTIME_ROOT = RUNTIME_AUTH_PATH.parents[1]
AGENT_COMMIT_PATH = Path(inspect.getfile(create_runtime_commit_service)).resolve()
AGENT_ROOT = AGENT_COMMIT_PATH.parents[3]


# Runtime's fixture helpers are test-only modules, not part of the production
# package.  Add that directory as a flat import location; do not import the
# candidate Runtime ``tests`` package, which would shadow Agent's tests.
sys.path.append(str(RUNTIME_ROOT / "tests"))
from precut_realm_fixture import load_precut_realm_fixture  # noqa: E402
from timeline_commit_film_fixture import FilmFixture  # noqa: E402


def detached(value):
    return json.loads(json.dumps(value, allow_nan=False))


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def change(path, before, value=None, *, op="set", ref="parent", **extra):
    result = {"op": op, "ref": ref, "path": path, "before": copy.deepcopy(before), **extra}
    if op in ("set", "list.insert"):
        result["value"] = copy.deepcopy(value)
    return result


def split_and_note_patch(document):
    """Retain the original split+unrelated-note command shape on real film IDs."""
    parent = document["parent_revision"]["payload"]
    clips = parent["clips"]
    source = clips[0]
    right_id = "music-right"
    if right_id in {clip["id"] for clip in clips}:
        raise AssertionError("probe fixture already contains its created clip")
    right = copy.deepcopy(source)
    right.update(id=right_id, at=2, hold=1)
    order = [clip["id"] for clip in clips]
    changes = [
        # The original retained witness writes an unrelated output field first.
        change(["config", "output", "file"], ABSENT, "output.mp4"),
        change(["clips"], ABSENT, right, op="list.insert", id=right_id,
               order_before=order, after_id=source["id"]),
        change(["clips", "id:" + source["id"], "hold"], present(source["hold"]), 1),
        change(["clips", "id:" + source["id"], "label"], ABSENT, None),
        change(["config", "output", "note"], ABSENT, "kept"),
        change(["clips", "id:" + source["id"], "hold"], present(1), 1.5),
        change(["clips", "id:" + source["id"], "label"], present(None), op="remove"),
    ]
    return {
        "schema_version": 1,
        "op": "doc.patch",
        "version": "1",
        "select": None,
        "args": {"changes": changes},
        "created": ["parent/clip:" + right_id],
    }


def v2_request(project, timeline, base, command, *, label, step_id, intent, group_id):
    patch = copy.deepcopy(command["args"]["changes"]) if command["op"] == "doc.patch" else []
    return {
        "api_version": 1,
        "project_id": project,
        "timeline_id": timeline,
        "base_revision_id": base["revision_id"],
        "base_publication_id": base["publication_id"],
        "commands": [copy.deepcopy(command)],
        "label": label,
        "steps": [{
            "id": step_id,
            "label": label,
            "intent": intent,
            "tags": ["retained-probe"],
            "command_ordinals": [0],
            "patch": patch,
            "reads": [],
        }],
        "merge": "fields",
        "reads": [],
        "dry_run": False,
        "source": {"via": "python"},
        "rationale": "Retained split and unrelated note history probe",
        "group_id": group_id,
    }


def stage_facts(prepared):
    records = prepared["records"]
    return [{
        "ordinal": command["ordinal"],
        "command": command["command"],
        "writes": command["writes"],
        "derived_writes": command["derived_writes"],
        "bindings": command["bindings"],
        "stage_bindings": [binding for binding in command["bindings"]
                           if binding.get("key") == "inverse.stage"],
    } for command in records["commands"]]


def auth_failure(call):
    try:
        call()
    except Exception as error:  # diagnostic output deliberately records refusal details
        return {
            "status": "refused",
            "type": type(error).__name__,
            "message": str(error),
            "failure": detached(getattr(error, "failure", None)),
        }
    return {"status": "pass"}


def production_auth_args(store, request, prepared, history):
    """Build the exact argument tuple used by TimelineCommitStore._validate."""
    project, timeline = request["project_id"], request["timeline_id"]
    source = store.revision_closure(project, timeline, prepared["expected_head"]["revision_id"])
    base = store.revision_closure(project, timeline, request["base_revision_id"])
    continuations = store._binding_continuations(
        project, timeline, request["base_publication_id"], prepared["expected_head"],
    )
    return source, base, continuations, history


def assert_exact_forward_history(store, project, timeline, forward, forward_prepared):
    publication = forward["receipt"]["receipt_id"]
    entry = store.history_entry(project, timeline, publication)
    if entry["publication_id"] != publication:
        raise AssertionError("store history publication does not match the receipt")
    if entry["receipt"] != forward["receipt"]:
        raise AssertionError("store history receipt differs from accepted receipt")
    if entry["records"] != forward_prepared["records"]:
        raise AssertionError("store history records differ from the accepted provider record")
    if entry["revision_id"] != forward_prepared["canonical_document"]["parent_revision"]["revision_id"]:
        raise AssertionError("store history revision differs from accepted canonical output")
    return {publication: detached(entry)}


def authenticate(store, request, prepared, history):
    source, base, continuations, history_arg = production_auth_args(
        store, request, prepared, history,
    )
    validate(
        request,
        prepared,
        source,
        base,
        continuations,
        history_arg,
    )
    return {
        "status": "pass",
        "argument_provenance": {
            "source_revision_id": source["parent_revision"]["revision_id"],
            "source_parent_digest": source["parent_revision"]["content_digest"],
            "base_revision_id": base["parent_revision"]["revision_id"],
            "base_parent_digest": base["parent_revision"]["content_digest"],
            "continuations": continuations,
            "history_publications": list(history_arg) if isinstance(history_arg, dict) else None,
        },
    }


def main():
    original_sha = sha256_file(ORIGINAL_REPRO)
    if original_sha != ORIGINAL_REPRO_SHA256:
        raise AssertionError("original retained repro bytes changed")

    captured_prepared = []
    original_accept = RequestCommitPort.accept

    def capture_accept(port, prepared):
        captured_prepared.append(detached(prepared))
        return original_accept(port, prepared)

    RequestCommitPort.accept = capture_accept
    try:
        with tempfile.TemporaryDirectory(prefix="r2r-history-probe-") as temp:
            captured = load_precut_realm_fixture(Path(temp), variant="music-documents")
            pins = captured.pins
            film = FilmFixture(
                source_root=captured.copy_roots[0],
                duplicate_root=captured.copy_roots[1],
                project_id=pins["project_id"],
                timeline_id=pins["timeline_id"],
                parent_revision_id=pins["parent_revision_id"],
                media_ids=pins["media_ids"],
                transcript_document_id=pins["transcript_document_id"],
                text_binding_id=pins["text_binding_id"],
            )
            service = RuntimeService(film.duplicate_root)
            try:
                provider = load_timeline_commit_provider("astrid")
                service.register_timeline_commit_provider(provider)
                store = service._timeline_commits()[0]
                project, timeline = film.project_id, film.timeline_id
                base_head = store.head(project, timeline)
                original = store.revision_closure(project, timeline, base_head["revision_id"])
                forward_command = split_and_note_patch(original)
                forward = v2_request(
                    project, timeline, base_head, forward_command,
                    label="Split and output", step_id="split", intent="Split and output",
                    group_id="split-group",
                )
                forward_result = service.commit_timeline(
                    project, timeline, forward, idempotency_key="r2r-history-forward",
                    publisher="retained-history-probe", invocation_path=route_path(project, timeline),
                    authorize=lambda: None,
                )
                forward_prepared = captured_prepared[-1]
                forward_history = assert_exact_forward_history(
                    store, project, timeline, forward_result, forward_prepared,
                )
                forward_auth = auth_failure(lambda: authenticate(
                    store, forward, forward_prepared, forward_history,
                ))
                if forward_auth["status"] != "pass":
                    raise AssertionError("forward authenticated validation refused")

                landing = detached(forward_result["data"]["canonical_document"])
                inverse_base = store.head(project, timeline)
                inverse_command = {
                    "schema_version": 1,
                    "op": "timeline.inverse",
                    "version": "1",
                    "select": None,
                    "args": {"publications": [forward_result["receipt"]["receipt_id"]]},
                }
                inverse = v2_request(
                    project, timeline, inverse_base, inverse_command,
                    label="Undo split and output", step_id="undo", intent="Undo split and output",
                    group_id="split-group",
                )
                inverse_result = service.commit_timeline(
                    project, timeline, inverse, idempotency_key="r2r-history-inverse",
                    publisher="retained-history-probe", invocation_path=route_path(project, timeline),
                    authorize=lambda: None,
                )
                inverse_prepared = captured_prepared[-1]
                inverse_history = store._inverse_stage_history(
                    project, timeline, inverse_prepared["records"],
                )
                if set(inverse_history) != {forward_result["receipt"]["receipt_id"]}:
                    raise AssertionError("inverse history includes a non-source publication")
                if inverse_history[forward_result["receipt"]["receipt_id"]] != forward_history[forward_result["receipt"]["receipt_id"]]:
                    raise AssertionError("inverse history source is not the exact accepted forward record")
                inverse_auth = auth_failure(lambda: authenticate(
                    store, inverse, inverse_prepared, inverse_history,
                ))
                if inverse_auth["status"] != "pass":
                    raise AssertionError("inverse authenticated validation refused")

                missing_history = auth_failure(lambda: authenticate(
                    store, inverse, inverse_prepared, None,
                ))
                forged_history = copy.deepcopy(inverse_history)
                forged_entry = forged_history[forward_result["receipt"]["receipt_id"]]
                forged_entry["records"]["steps"][0]["id"] = "caller-invented-step"
                forged_probe = auth_failure(lambda: authenticate(
                    store, inverse, inverse_prepared, forged_history,
                ))
                extra_history = copy.deepcopy(inverse_history)
                extra_history[inverse_result["receipt"]["receipt_id"]] = store.history_entry(
                    project, timeline, inverse_result["receipt"]["receipt_id"],
                )
                extra_history_probe = auth_failure(lambda: (
                    (_ for _ in ()).throw(AssertionError(
                        "history argument includes inverse/new publication"
                    )) if set(extra_history) != {forward_result["receipt"]["receipt_id"]} else None
                ))

                output = {
                    "artifact": "agent-R2-stage-repro-1003-store-authenticated",
                    "status": "PASS" if forward_auth["status"] == inverse_auth["status"] == "pass"
                    and missing_history["status"] == forged_probe["status"] == extra_history_probe["status"] == "refused"
                    else "FAIL",
                    "kind": "one-real-agent-grouped-inverse-auth-repro",
                    "purpose": "Runtime store-authenticated retained split+note forward/inverse validation",
                    "candidate": "whole split+unrelated-note",
                    "command": (
                        "PYTHONDONTWRITEBYTECODE=1 "
                        f"PYTHONPATH={RUNTIME_ROOT}:{AGENT_ROOT} "
                        f"/home/user/work/venv-agent/bin/python {Path(__file__).resolve()}"
                    ),
                    "agent_checkout": str(AGENT_ROOT),
                    "agent_commit": "ef851b22c506245441b9a630c093b3460e39cbdc",
                    "agent_provider_origin": str(AGENT_COMMIT_PATH),
                    "agent_provider_sha256": sha256_file(AGENT_COMMIT_PATH),
                    "runtime_checkout": str(RUNTIME_ROOT),
                    "runtime_commit": "21b329935785e4040775ed34b4a01ebf31ec6683",
                    "runtime_auth_origin": str(RUNTIME_AUTH_PATH),
                    "runtime_auth_sha256": sha256_file(RUNTIME_AUTH_PATH),
                    "runtime_store_origin": str(RUNTIME_ROOT / "runtime_protocol" / "timeline_commit_store.py"),
                    "runtime_store_sha256": sha256_file(RUNTIME_ROOT / "runtime_protocol" / "timeline_commit_store.py"),
                    "fixture_origins": {
                        "precut_loader": str(RUNTIME_ROOT / "tests" / "precut_realm_fixture.py"),
                        "film_fixture": str(RUNTIME_ROOT / "tests" / "timeline_commit_film_fixture.py"),
                        "store_acceptance": str(RUNTIME_ROOT / "runtime_protocol" / "timeline_commit_store.py"),
                    },
                    "original_repro": {
                        "path": str(ORIGINAL_REPRO),
                        "sha256": original_sha,
                        "preserved": original_sha == ORIGINAL_REPRO_SHA256,
                    },
                    "fixture": {
                        "variant": "music-documents",
                        "project_id": project,
                        "timeline_id": timeline,
                        "base_head": base_head,
                    },
                    "forward": {
                        "request": forward,
                        "idempotency_key": "r2r-history-forward",
                        "result": forward_result,
                        "input_base_document": original,
                        "output_document": landing,
                        "prepared": forward_prepared,
                        "stages": stage_facts(forward_prepared),
                        "authenticated_history": forward_history,
                        "auth": forward_auth,
                    },
                    "inverse": {
                        "request": inverse,
                        "idempotency_key": "r2r-history-inverse",
                        "result": inverse_result,
                        "base_document": original,
                        "input_document": landing,
                        "output_document": inverse_result["data"]["canonical_document"],
                        "prepared": inverse_prepared,
                        "stages": stage_facts(inverse_prepared),
                        "authenticated_history": inverse_history,
                        "auth": inverse_auth,
                    },
                    "negative_probes": {
                        "missing_history": missing_history,
                        "forged_history_step": forged_probe,
                        "extra_inverse_history": extra_history_probe,
                    },
                    "history_provenance": {
                        "source_publication": forward_result["receipt"]["receipt_id"],
                        "inverse_publication": inverse_result["receipt"]["receipt_id"],
                        "supplied_inverse_history_publications": list(inverse_history),
                        "excluded_inverse_publication": inverse_result["receipt"]["receipt_id"] not in inverse_history,
                        "source_records_exactly_store_accepted": inverse_history[forward_result["receipt"]["receipt_id"]] == forward_history[forward_result["receipt"]["receipt_id"]],
                        "source_step_ids": [step["id"] for step in forward_prepared["records"]["steps"]],
                        "source_command_ordinals": [record["ordinal"] for record in forward_prepared["records"]["commands"]],
                        "source_created_refs": [created["ref"] for record in forward_prepared["records"]["commands"] for created in record["created"]],
                    },
                    "expected": {
                        "forward_runtime_auth": "accepted",
                        "inverse_runtime_auth": "accepted",
                        "missing_history": "refused",
                        "forged_history": "refused",
                        "extra_inverse_history": "refused by probe provenance guard",
                        "no_original_58_rerun": True,
                        "no_http_journey": True,
                    },
                }
                print(json.dumps(output, sort_keys=True))
            finally:
                service.close()
    finally:
        RequestCommitPort.accept = original_accept


if __name__ == "__main__":
    main()
