"""Run small, explicit development journeys against an existing Runtime.

This is a current-contract runner, not the historical real-film checkpoint
suite. It never provisions a workspace or creates project/timeline inputs.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from typing import Any


def _ok(result: Any) -> bool:
    return bool(getattr(result, "ok", False))


def _data(result: Any) -> Any:
    return getattr(result, "data", None)


def _head(result: Any) -> str | None:
    data = _data(result)
    if not isinstance(data, Mapping):
        return None
    summary = data.get("summary")
    if not isinstance(summary, Mapping):
        return None
    value = summary.get("head_revision_id") or summary.get("revision_id")
    return str(value) if value not in (None, "") else None


def _error(result: Any) -> str:
    error = getattr(result, "error", None)
    if isinstance(error, Mapping):
        return str(error.get("message") or error.get("code") or "Runtime request failed")
    return str(error or "Runtime request failed")


def _emit(payload: Mapping[str, Any], *, as_json: bool) -> int:
    if as_json:
        print(json.dumps(dict(payload), indent=2, sort_keys=True, default=str))
    elif payload.get("ok"):
        print("Astrid dev journey: render")
        print(f"state: {payload.get('state')}")
        print(f"timeline: {payload.get('project')}/{payload.get('timeline')}")
        print(f"head before: {payload.get('head_before')}")
        print(f"head after: {payload.get('head_after')}")
        print(f"head unchanged: {payload.get('head_unchanged')}")
        for label in ("run_id", "task_id", "attempt_id"):
            if payload.get(label):
                print(f"{label.replace('_', ' ')}: {payload[label]}")
        outputs = payload.get("outputs")
        if outputs:
            print("outputs:")
            print(json.dumps(outputs, indent=2, sort_keys=True, default=str))
    else:
        print(f"Astrid dev journey: {payload.get('error', 'failed')}", file=sys.stderr)
    return 0 if payload.get("ok") else 1


def run_render(
    *,
    project: str,
    timeline: str | None,
    range_value: str | None = None,
    timeout_seconds: float = 1800.0,
    client_opener: Any = None,
) -> dict[str, Any]:
    """Render one existing canonical timeline and report its observed head.

    The expected timeline version is sent when the current listing exposes it,
    so a concurrent edit fails before admission. The before/after revision
    reads remain visible in the result even when an older Runtime omits that
    CAS version field.
    """
    if client_opener is None:
        from astrid.sdk.client import AstridClient

        client_opener = AstridClient.open_existing_from_launcher

    try:
        context = client_opener()
        with context as client:
            resolved = client.timelines.resolve_scope(project, timeline)
            if not _ok(resolved) or not isinstance(_data(resolved), Mapping):
                return {"ok": False, "state": "refused", "error": _error(resolved)}
            scope = _data(resolved)
            project_ref = str(scope.get("project_ref") or project)
            resolved_ref = scope.get("timeline_ref") or timeline or scope.get("timeline_id")
            if resolved_ref in (None, ""):
                return {"ok": False, "state": "refused", "error": "Runtime timeline resolution omitted the canonical timeline id"}
            timeline_ref = str(resolved_ref)
            version = scope.get("version", scope.get("config_version"))
            expected_version = (
                int(version) if isinstance(version, int) and not isinstance(version, bool) and version > 0
                else None
            )

            before = client.timelines.show(project_ref, timeline_ref)
            head_before = _head(before)
            if not _ok(before) or head_before is None:
                return {
                    "ok": False,
                    "state": "refused",
                    "project": project_ref,
                    "timeline": timeline_ref,
                    "error": _error(before) if not _ok(before) else "Runtime inspection omitted the canonical current head",
                }

            inputs: dict[str, Any] = {"timeline_ref": timeline_ref}
            if expected_version is not None:
                inputs["expected_version"] = expected_version
            if range_value is not None:
                inputs["range"] = range_value
            render = client.invoke_result(
                "rendering.render",
                kind="executor",
                project=project_ref,
                inputs=inputs,
                wait=True,
                timeout_seconds=timeout_seconds,
            )
            after = client.timelines.show(project_ref, timeline_ref)
            head_after = _head(after) if _ok(after) else None
            raw = getattr(render, "raw_result", None)
            raw = raw if isinstance(raw, Mapping) else {}
            outputs = getattr(render, "outputs", None)
            payload = {
                "ok": _ok(render),
                "state": str(raw.get("state") or ("completed" if _ok(render) else "failed")),
                "project": project_ref,
                "timeline": timeline_ref,
                "head_before": head_before,
                "head_after": head_after,
                "head_unchanged": head_after == head_before if head_after is not None else None,
                "expected_version": expected_version,
                "range": range_value,
                "run_id": getattr(render, "kernel_run_id", None) or getattr(render, "run_id", None),
                "task_id": getattr(render, "kernel_task_id", None),
                "attempt_id": getattr(render, "kernel_attempt_id", None),
                "outputs": outputs,
            }
            if not _ok(render):
                payload["error"] = _error(render)
            elif head_after is None:
                payload["readback_error"] = _error(after)
            return payload
    except Exception as exc:  # a refused selected Runtime is a normal CLI outcome
        return {"ok": False, "state": "unavailable", "error": str(exc)}


def main(args: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="astrid dev journey",
        description="Run an explicit development journey against an already-running Runtime; this command never starts services or creates inputs.",
    )
    sub = parser.add_subparsers(dest="journey", required=True)
    render = sub.add_parser("render", help="render an existing canonical project timeline")
    render.add_argument("--project", required=True, help="existing Runtime project id or slug")
    render.add_argument("timeline", nargs="?", default=None, help="existing timeline id or slug (default: the project's configured timeline)")
    render.add_argument("--range", dest="range_value", metavar="START..END", help="optional half-open render interval in seconds")
    render.add_argument("--timeout-seconds", type=float, default=1800.0, help="bounded render wait (default: 1800)")
    render.add_argument("--json", action="store_true", help="print a machine-readable result")
    parsed = parser.parse_args(args)
    if parsed.timeout_seconds <= 0:
        parser.error("--timeout-seconds must be positive")
    payload = run_render(
        project=parsed.project,
        timeline=parsed.timeline,
        range_value=parsed.range_value,
        timeout_seconds=parsed.timeout_seconds,
    )
    return _emit(payload, as_json=parsed.json)
