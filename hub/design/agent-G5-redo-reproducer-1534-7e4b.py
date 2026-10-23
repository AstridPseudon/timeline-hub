#!/usr/bin/env python3
"""Bounded public redo diagnostic for G5.

This is a source-only diagnostic.  It deliberately reuses the public fixture
and calls the public forward/undo/redo APIs.  The wrappers retain observations
and re-raise every return value and exception; they are not alternate history,
provider, cache, or guard implementations.
"""
from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import importlib
import json
import os
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Any


AGENT_HEAD = "91ac58a9fc6f1f752be16c0e4b8a1bf17095acee"
RUNTIME_HEAD = "9ce4242bc01f100bab9efc51032a73985cefb2b2"
TARGET = "test_restructure_whole_inverse_redo_and_intervening_overlap_refusal"
TARGET_BODY_SHA256 = "c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d"
TARGET_BODY_BYTES = 6798

REQUIRED_REQUEST_KEYS = {
    "api_version",
    "project_id",
    "timeline_id",
    "base_revision_id",
    "base_publication_id",
    "commands",
    "label",
    "steps",
    "merge",
    "reads",
    "dry_run",
    "source",
}
STEP_KEYS = {"id", "label", "intent", "tags", "command_ordinals", "patch"}
PORT_METHODS = (
    "head",
    "history",
    "history_entry",
    "revision_closure",
    "source_revision_closure",
    "shot_closure",
    "selected_media",
    "raw_media_info",
    "text_selection",
    "narration_take",
    "transcript_source",
    "config_source",
    "document_object",
    "producer_attempt",
    "preview",
    "accept",
)
GUARD_MODULES = (
    "astrid.sdk.timeline._recording",
    "astrid.sdk.timeline.commands",
    "astrid.sdk.timeline.inverse",
    "astrid.sdk.timeline._root_inverse",
    "astrid.sdk.timeline.checkout",
)
TRACEBACK_LOCAL_KEYS = (
    "request",
    "base",
    "current",
    "calls",
    "execution_calls",
    "undo_of",
    "undo_steps",
    "inverse_records",
    "inverse_intervening",
    "inverse_sources",
    "closures",
    "restored_from",
    "schema_inputs",
    "resolve_inputs",
    "original",
    "plan",
    "bindings",
    "prepared",
    "records",
)


def clone(value: Any) -> Any:
    """Copy JSON-shaped evidence, retaining a readable fallback for odd values."""
    try:
        return copy.deepcopy(value)
    except Exception:
        return repr(value)


def exception_record(exc: BaseException) -> dict[str, Any]:
    result: dict[str, Any] = {
        "type": type(exc).__name__,
        "message": str(exc),
        "status": getattr(exc, "status", None),
        "code": getattr(exc, "code", None),
        "details": clone(getattr(exc, "details", None)),
        "failure": clone(getattr(exc, "failure", None)),
        "to_json": None,
    }
    to_json = getattr(exc, "to_json", None)
    if callable(to_json):
        try:
            result["to_json"] = clone(to_json())
        except Exception as to_json_exc:
            result["to_json_error"] = exception_record(to_json_exc)
    return result


def traceback_locals(exc: BaseException) -> list[dict[str, Any]]:
    """Capture selected locals only after a provider exception is caught.

    This is intentionally not ``sys.settrace``: there is no line/call tracing
    of the service or Runtime.  The selected names are the provider's request,
    inverse, prepared, and stage boundaries needed to identify a throw site.
    """
    frames: list[dict[str, Any]] = []
    cursor = exc.__traceback__
    while cursor is not None:
        frame = cursor.tb_frame
        filename = str(Path(frame.f_code.co_filename).resolve())
        if "/astrid/sdk/timeline/" in filename:
            frames.append(
                {
                    "file": filename,
                    "function": frame.f_code.co_name,
                    "line": cursor.tb_lineno,
                    "locals": {
                        key: clone(frame.f_locals[key])
                        for key in TRACEBACK_LOCAL_KEYS
                        if key in frame.f_locals
                    },
                }
            )
        cursor = cursor.tb_next
    return frames


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head(path: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def target_body(path: Path) -> tuple[str, int]:
    text = path.read_text()
    tree = ast.parse(text)
    node = next(
        item
        for item in tree.body
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == TARGET
    )
    data = "\n".join(text.splitlines()[node.lineno - 1 : node.end_lineno]) + "\n"
    return hashlib.sha256(data.encode()).hexdigest(), len(data.encode())


def module_origins() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for name, module in tuple(sys.modules.items()):
        if not (
            name.startswith("astrid.sdk.timeline")
            or name.startswith("runtime_protocol.timeline_commit")
            or name in {"runtime_protocol", "tests.sdk.test_timeline_restructure_guarded_runtime"}
        ):
            continue
        filename = getattr(module, "__file__", None)
        if filename:
            path = Path(filename).resolve()
            if path.is_file():
                result[name] = {"path": str(path), "sha256": source_hash(path)}
    return result


def sql_snapshot(env: Any) -> list[str]:
    return list(env.service.store.conn.iterdump())


def state_snapshot(env: Any, *, history: Any | None = None) -> dict[str, Any]:
    return {
        "document": clone(env.document()),
        "head": clone(env.service.get_project_timeline(env.project, "t")),
        "history": clone(
            history
            if history is not None
            else env.client.timelines.history(env.project, "t", limit=200).data
        ),
        "sql": sql_snapshot(env),
        "calls": clone(env.calls),
        "replies": clone(env.replies),
    }


def verify_current_closure(env: Any, label: str) -> dict[str, Any]:
    head = env.service.get_project_timeline(env.project, "t")
    opened = env.client.timelines.open_bundle(
        env.project,
        "t",
        revision_id=head["head_revision_id"],
        publication_id=head["head_publication_id"],
    )
    if not opened.ok:
        raise AssertionError(f"{label}: exact current closure did not open: {opened.as_dict()}")
    bundle = opened.data["bundle"]
    runtime_document = bundle["source_mapping"]["_runtime_document"]
    if runtime_document != env.document():
        raise AssertionError(f"{label}: public closure differs from current document")
    if bundle["base_parent"]["revision_id"] != head["head_revision_id"]:
        raise AssertionError(f"{label}: closure revision pin differs from head")
    if bundle["base_parent"].get("publication_id") != head["head_publication_id"]:
        raise AssertionError(f"{label}: closure publication pin differs from head")
    return {
        "label": label,
        "head": clone(head),
        "bundle_base_parent": clone(bundle["base_parent"]),
        "runtime_document": clone(runtime_document),
        "opened": clone(opened.as_dict()),
    }


def audit_request(body: Any) -> dict[str, Any]:
    if not isinstance(body, dict):
        return {"valid": False, "reason": "request is not an object", "raw": clone(body)}
    missing = sorted(REQUIRED_REQUEST_KEYS - set(body))
    steps = body.get("steps")
    step_missing = []
    if isinstance(steps, list):
        for index, step in enumerate(steps):
            if isinstance(step, dict):
                missing_keys = sorted(STEP_KEYS - set(step))
                if missing_keys:
                    step_missing.append({"index": index, "missing": missing_keys})
            else:
                step_missing.append({"index": index, "missing": "step is not an object"})
    else:
        step_missing.append({"missing": "steps is not an array"})
    return {
        "valid": not missing and not step_missing and body.get("merge") in {"fields", "atomic"},
        "missing": missing,
        "step_missing": step_missing,
        "keys": sorted(body),
        "optional_c0_fields": {
            key: clone(body[key])
            for key in ("rationale", "group_id")
            if key in body
        },
        "request": clone(body),
    }


def audit_reply(value: Any) -> dict[str, Any]:
    """Audit without normalizing or dropping any accepted/error envelope."""
    if not isinstance(value, dict):
        return {"kind": "non_object", "value": clone(value)}
    data = value.get("data")
    result = {
        "kind": "reply",
        "top_level_keys": sorted(value),
        "status": data.get("status") if isinstance(data, dict) else None,
        "data_keys": sorted(data) if isinstance(data, dict) else [],
        "has_receipt": isinstance(value.get("receipt"), dict),
        "canonical_document": isinstance(data, dict) and isinstance(data.get("canonical_document"), dict),
        "records": clone(data.get("records")) if isinstance(data, dict) else None,
        "steps": clone(data.get("steps")) if isinstance(data, dict) else None,
        "undo_steps": clone(data.get("undo_steps")) if isinstance(data, dict) else None,
        "reply": clone(value),
    }
    if result["status"] == "preview":
        result["would_status"] = data.get("would_status") if isinstance(data, dict) else None
    return result


def install_wrappers(env: Any, report: dict[str, Any], phase: dict[str, str]) -> list[tuple[Any, str, Any, bool]]:
    restores: list[tuple[Any, str, Any, bool]] = []

    def replace(owner: Any, name: str, wrapper: Any) -> None:
        existed = name in getattr(owner, "__dict__", {})
        old = getattr(owner, name)
        restores.append((owner, name, old, existed))
        setattr(owner, name, wrapper)

    old_generated = env.generated.commit_timeline

    def generated_commit(project: Any, timeline: Any, body: Any, *, idempotency_key: str):
        event: dict[str, Any] = {
            "phase": phase["name"],
            "project": project,
            "timeline": timeline,
            "idempotency_key": idempotency_key,
            "request": clone(body),
            "request_audit": audit_request(body),
        }
        report["transport_calls"].append(event)
        try:
            result = old_generated(project, timeline, body, idempotency_key=idempotency_key)
        except BaseException as exc:
            event["exception"] = exception_record(exc)
            raise
        event["reply"] = clone(result)
        event["reply_audit"] = audit_reply(result)
        return result

    replace(env.generated, "commit_timeline", generated_commit)

    provider = env.service._timeline_commit_provider
    if provider is None:
        raise AssertionError("faithful fixture did not install the astrid provider")
    old_provider_commit = provider.commit

    def provider_commit(context: Any, port: Any):
        event: dict[str, Any] = {
            "phase": phase["name"],
            "context": clone(context),
            "request": clone(context.get("request")),
            "port_calls": [],
        }
        report["provider_calls"].append(event)
        port_restores: list[tuple[str, Any, bool]] = []
        for method_name in PORT_METHODS:
            if not hasattr(port, method_name):
                continue
            existed = method_name in getattr(port, "__dict__", {})
            old_method = getattr(port, method_name)
            port_restores.append((method_name, old_method, existed))

            def port_method(*args: Any, _name=method_name, _old=old_method, **kwargs: Any):
                port_event: dict[str, Any] = {
                    "phase": phase["name"],
                    "method": _name,
                    "args": clone(args),
                    "kwargs": clone(kwargs),
                }
                event["port_calls"].append(port_event)
                try:
                    value = _old(*args, **kwargs)
                except BaseException as exc:
                    port_event["exception"] = exception_record(exc)
                    raise
                port_event["return"] = clone(value)
                if _name in {"accept", "preview"} and args and isinstance(args[0], dict):
                    port_event["prepared"] = clone(args[0])
                return value

            setattr(port, method_name, port_method)
        try:
            value = old_provider_commit(context, port)
        except BaseException as exc:
            event["exception"] = exception_record(exc)
            event["provider_traceback_locals"] = traceback_locals(exc)
            raise
        else:
            event["outcome"] = clone(value)
            return value
        finally:
            for method_name, old_method, existed in reversed(port_restores):
                if existed:
                    setattr(port, method_name, old_method)
                else:
                    delattr(port, method_name)

    replace(provider, "commit", provider_commit)

    for module_name in GUARD_MODULES:
        module = importlib.import_module(module_name)
        if not hasattr(module, "guard"):
            continue
        old_guard = module.guard

        def guard_wrapper(state: Any, ref: Any, path: Any, expected: Any, *, _module=module_name,
                          _old=old_guard, **kwargs: Any):
            event: dict[str, Any] = {
                "phase": phase["name"],
                "module": _module,
                "ref": clone(ref),
                "path": clone(path),
                "expected": clone(expected),
                "kwargs": clone(kwargs),
            }
            report["guard_calls"].append(event)
            try:
                event["actual_before"] = clone(state.get(ref, path))
            except BaseException as exc:
                event["actual_before_error"] = exception_record(exc)
            try:
                value = _old(state, ref, path, expected, **kwargs)
            except BaseException as exc:
                event["exception"] = exception_record(exc)
                try:
                    event["actual_after"] = clone(state.get(ref, path))
                except BaseException:
                    pass
                raise
            event["return"] = clone(value)
            return value

        replace(module, "guard", guard_wrapper)

    return restores


def run_scenario(env: Any, report: dict[str, Any], phase: dict[str, str], tmp_path: Path) -> None:
    from astrid.sdk import timeline
    from astrid.sdk.timeline._common import TimelineEditError
    from astrid.sdk.timeline.checkout import Checkout
    from astrid.sdk.timeline.sync import CommitConflict

    env.calls.clear()
    env.replies.clear()
    phase["name"] = "genesis-name"
    source = timeline.open(env.project, "t", client=env.client, outbox_path=tmp_path / "name.json")
    source.bundle["shots"][source._shot_ids()[0]]["payload"]["name"] = "02 TWO"
    named = source.commit("Name source chapter", idempotency_key="inverse-name")
    report["genesis_name"] = {"reply": clone(named), "reply_audit": audit_reply(named)}
    env.calls.clear()
    env.replies.clear()

    report["closure_checks"] = [verify_current_closure(env, "before-forward")]
    before = clone(env.document())
    before_history = clone(env.client.timelines.history(env.project, "t", limit=200).data)
    report["before_forward"] = state_snapshot(env, history=before_history)

    def no_narration_media(**_kwargs: Any):
        raise TimelineEditError("qualification keeps the restructure as one publication")

    old_import = env.client.media.import_bytes
    env.client.media.import_bytes = no_narration_media
    try:
        phase["name"] = "forward"
        cut = Checkout.open(env.project, "t", client=env.client).publish(
            "Restructure", restructure=True, client=env.client, idempotency_key="inverse-cut"
        )
    finally:
        env.client.media.import_bytes = old_import
    report["forward"] = {"result": clone(cut), "reply": clone(env.replies[-1])}
    if not cut.get("narration_error"):
        raise AssertionError("forward did not retain the one-publication narration boundary")
    forward_reply = env.replies[-1]
    if forward_reply.get("data", {}).get("status") not in {"accepted", "merged"}:
        raise AssertionError(f"forward was not accepted/merged: {forward_reply}")
    after = clone(env.document())
    report["forward"]["canonical_document"] = after
    report["closure_checks"].append(verify_current_closure(env, "after-forward"))

    reopened = timeline.open(env.project, "t", client=env.client, outbox_path=tmp_path / "inverse.json")
    phase["name"] = "whole-undo"
    undone = reopened.session.undo(
        [forward_reply["receipt"]["receipt_id"]], idempotency_key="inverse-undo"
    )
    report["whole_undo"] = {"result": clone(undone), "reply": clone(env.replies[-1])}
    undo_document = undone["data"]["canonical_document"]
    if undo_document["parent_revision"]["payload"] != before["parent_revision"]["payload"]:
        raise AssertionError("whole undo did not restore the original parent payload")
    if [row["payload"] for row in undo_document["shot_revisions"]] != [
        row["payload"] for row in before["shot_revisions"]
    ]:
        raise AssertionError("whole undo did not restore shot payloads")
    if [row["payload"] for row in undo_document["internal_timeline_revisions"]] != [
        row["payload"] for row in before["internal_timeline_revisions"]
    ]:
        raise AssertionError("whole undo did not restore internal timeline payloads")
    if undo_document["dependency_manifest"] != before["dependency_manifest"]:
        raise AssertionError("whole undo did not restore dependency pins")
    report["closure_checks"].append(verify_current_closure(env, "after-whole-undo"))

    redo_before = state_snapshot(env)
    report["redo_before"] = clone(redo_before)
    phase["name"] = "public-redo"
    redo_exception: BaseException | None = None
    redone = None
    try:
        redone = reopened.session.undo(
            [undone["receipt"]["receipt_id"]], idempotency_key="inverse-redo"
        )
    except BaseException as exc:
        redo_exception = exc
        report["redo"] = {"exception": exception_record(exc), "reached": False}
    else:
        report["redo"] = {"result": clone(redone), "reply": clone(env.replies[-1]), "reached": True}
        redo_document = redone["data"]["canonical_document"]
        if redo_document["parent_revision"]["payload"] != after["parent_revision"]["payload"]:
            raise AssertionError("redo did not restore the forward parent payload")
        if [row["payload"] for row in redo_document["shot_revisions"]] != [
            row["payload"] for row in after["shot_revisions"]
        ]:
            raise AssertionError("redo did not restore forward shot payloads")
        if [row["payload"] for row in redo_document["internal_timeline_revisions"]] != [
            row["payload"] for row in after["internal_timeline_revisions"]
        ]:
            raise AssertionError("redo did not restore forward internal timeline payloads")
        if redo_document["dependency_manifest"] != after["dependency_manifest"]:
            raise AssertionError("redo did not restore forward dependency pins")
        report["closure_checks"].append(verify_current_closure(env, "after-redo"))
    finally:
        report["redo_after"] = state_snapshot(env)
        report["redo_no_write_on_refusal"] = (
            redo_exception is not None
            and report["redo_after"]["document"] == redo_before["document"]
            and report["redo_after"]["history"] == redo_before["history"]
            and report["redo_after"]["sql"] == redo_before["sql"]
        )

    if redo_exception is not None:
        report["later_overlap"] = {
            "reached": False,
            "reason": "public redo refused before the original later-overlap assertions",
        }
        report["verdict"] = "FAIL: public redo refused; diagnostic retained"
        return

    later = timeline.open(env.project, "t", client=env.client, outbox_path=tmp_path / "later.json")
    bed = next(clip for clip in later.bundle["parent"]["clips"] if clip["id"] == "bed")
    bed["volume"] = 0.25
    phase["name"] = "later-overlap-accepted"
    overlap = later.commit(
        "Later authored overlap", merge="fields", reads=[], idempotency_key="inverse-overlap"
    )
    if overlap["data"]["status"] not in {"accepted", "merged"}:
        raise AssertionError("later authored overlap was not accepted/merged")
    refusing = timeline.open(env.project, "t", client=env.client, outbox_path=tmp_path / "refusing.json")
    phase["name"] = "later-overlap-refusal"
    refusal_before = state_snapshot(env)
    try:
        refusing.session.undo([redone["receipt"]["receipt_id"]], idempotency_key="inverse-refuse")
    except CommitConflict as exc:
        report["later_overlap"] = {
            "reached": True,
            "exception": exception_record(exc),
            "message_contains_intervening": "intervening" in str(exc),
            "after": state_snapshot(env),
            "no_write": state_snapshot(env)["head"] == refusal_before["head"]
            and state_snapshot(env)["history"] == refusal_before["history"]
            and state_snapshot(env)["document"] == refusal_before["document"]
            and state_snapshot(env)["sql"] == refusal_before["sql"],
        }
        if not report["later_overlap"]["message_contains_intervening"]:
            raise AssertionError("later overlap refusal lacked its expected conflict reason")
    else:
        raise AssertionError("the overlapping authored write must refuse the guarded inverse")
    report["verdict"] = "PASS: public redo and later-overlap refusal completed"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="directory for the one JSON evidence artifact")
    parser.add_argument("--agent-root", type=Path, default=None)
    parser.add_argument("--runtime-root", type=Path, default=None)
    parser.add_argument("--tmpdir", type=Path, default=None)
    parser.add_argument("--net", action="store_true", help="required explicit live-service qualification acknowledgement")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    agent_root = (args.agent_root or Path.cwd()).resolve()
    runtime_root = (args.runtime_root or Path(os.environ.get("ASTRID_RUNTIME_CHECKOUT", ""))).resolve()
    output_dir = args.out.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "task": "agt-G5-redo-reproducer-source-1534",
        "source_only_authoring": False,
        "net_flag": args.net,
        "agent_root": str(agent_root),
        "runtime_root": str(runtime_root),
        "expected_source": {"agent_head": AGENT_HEAD, "runtime_head": RUNTIME_HEAD},
        "transport_calls": [],
        "provider_calls": [],
        "guard_calls": [],
        "closure_checks": [],
    }
    base_generator = None
    monkeypatch = None
    restores: list[tuple[Any, str, Any, bool]] = []
    phase = {"name": "bootstrap"}
    try:
        if not args.net:
            raise RuntimeError("refusing to run without explicit --net")
        if git_head(agent_root) != AGENT_HEAD:
            raise RuntimeError(f"Agent source head is not {AGENT_HEAD}")
        if git_head(runtime_root) != RUNTIME_HEAD:
            raise RuntimeError(f"Runtime source head is not {RUNTIME_HEAD}")
        sys.path[:0] = [str(agent_root), str(runtime_root), str(runtime_root / "packages/python")]
        target_module = importlib.import_module("tests.sdk.test_timeline_restructure_guarded_runtime")
        target_path = Path(target_module.__file__).resolve()
        body_hash, body_bytes = target_body(target_path)
        report["source"] = {
            "target_test": str(target_path),
            "target_test_sha256": source_hash(target_path),
            "target_body_sha256": body_hash,
            "target_body_bytes": body_bytes,
            "target_body_expected": TARGET_BODY_SHA256,
            "target_body_expected_bytes": TARGET_BODY_BYTES,
            "module_origins_boot": module_origins(),
        }
        if (body_hash, body_bytes) != (TARGET_BODY_SHA256, TARGET_BODY_BYTES):
            raise RuntimeError("the unchanged original public body hash/size does not match c271")

        import pytest

        monkeypatch = pytest.MonkeyPatch()
        tmp_context = tempfile.TemporaryDirectory(prefix="g5-redo-", dir=args.tmpdir)
        tmp_path = Path(tmp_context.name)
        base_factory = target_module.restructure_runtime.__wrapped__
        base_generator = base_factory(tmp_path, monkeypatch)
        env = next(base_generator)
        env = target_module.restructure_inverse_runtime.__wrapped__(env, monkeypatch)
        report["boot"] = {
            "realm": clone(env.service.realm),
            "admission": clone(getattr(env.service.store, "admission_report", None)),
            "provider": {
                "class": f"{type(env.service._timeline_commit_provider).__module__}.{type(env.service._timeline_commit_provider).__qualname__}",
                "provider_id": getattr(env.service._timeline_commit_provider, "provider_id", None),
                "interface_version": getattr(env.service._timeline_commit_provider, "interface_version", None),
                "contract_digest": getattr(env.service._timeline_commit_provider, "contract_digest", None),
            },
            "origins": module_origins(),
        }
        restores = install_wrappers(env, report, phase)
        run_scenario(env, report, phase, tmp_path)
        report["source"]["module_origins_after"] = module_origins()
        report["source_only_authoring"] = True
    except BaseException as exc:
        report["fatal"] = {
            "exception": exception_record(exc),
            "traceback": traceback.format_exc(),
        }
        report["verdict"] = "BLOCKED: reproducer did not reach its scenario"
    finally:
        for owner, name, old, existed in reversed(restores):
            if existed:
                setattr(owner, name, old)
            elif name in getattr(owner, "__dict__", {}):
                delattr(owner, name)
        if base_generator is not None:
            base_generator.close()
        if monkeypatch is not None:
            monkeypatch.undo()
        if "source" in report:
            report["source"]["module_origins_final"] = module_origins()
        artifact = output_dir / "g5-redo-diagnostic.json"
        artifact.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
        report["artifact"] = str(artifact)
        (output_dir / "g5-redo-diagnostic.sha256").write_text(source_hash(artifact) + "  " + artifact.name + "\n")
        tmp_context.cleanup() if "tmp_context" in locals() else None
    print(json.dumps({key: report[key] for key in ("verdict", "artifact") if key in report}, sort_keys=True))
    return 0 if report.get("verdict", "").startswith("PASS:") else 1


if __name__ == "__main__":
    raise SystemExit(main())
