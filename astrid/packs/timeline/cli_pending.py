"""CLI adapters for saved timeline edits and their conflict recovery."""
from __future__ import annotations

import argparse
import sys
from collections.abc import Mapping

from astrid.core.cli.domain_output import DomainResult, print_result
from astrid.packs.timeline.cli_common import need_project


def _open(parsed):
    from astrid.sdk.timeline.commit_session import Timeline

    return Timeline.open(need_project(parsed), parsed.ref, client=parsed.client)


def _error(exc):
    from astrid.sdk.contracts import ErrorObject

    details = dict(getattr(exc, "details", {}) or {})
    failure = getattr(exc, "failure", None)
    if isinstance(failure, Mapping):
        details.update(failure.get("details") or {})
    clash = getattr(exc, "clash", None)
    pending_id = getattr(exc, "pending_id", None)
    if isinstance(clash, Mapping):
        details["clash"] = dict(clash)
    if pending_id:
        details["pending_id"] = pending_id
    return DomainResult.failure(ErrorObject(
        getattr(exc, "code", None) or "timeline_edit_error", str(exc), details,
    ))


def _cmd_list(parsed):
    timeline = _open(parsed)
    records = timeline.pending_list(
        all=parsed.all, actors="all" if parsed.all_actors else "self",
    )
    return print_result(DomainResult.success({"pending_changes": records}), as_json=parsed.json)


def _cmd_show(parsed):
    timeline = _open(parsed)
    return print_result(DomainResult.success(timeline.pending_show(parsed.ref_id)), as_json=parsed.json)


def _cmd_drop(parsed):
    timeline = _open(parsed)
    record = timeline.pending_drop(parsed.ref_id, reason=parsed.reason)
    return print_result(DomainResult.success(record), as_json=parsed.json)


def _retry_data(result):
    data = result.get("data") if isinstance(result.get("data"), Mapping) else {}
    retry = data.get("retry") if isinstance(data.get("retry"), Mapping) else {}
    return {
        "status": result.get("status"),
        "pending_id": result.get("pending_id"),
        "token": retry.get("token"),
        "head": data.get("head"),
        "diff": data.get("diff"),
        "conflicts": data.get("conflicts"),
        "receipts": data.get("receipts"),
        "summary": result.get("summary"),
        "next": result.get("next"),
    }


def _cmd_retry(parsed):
    from astrid.sdk.timeline.retry import commit_preview

    timeline = _open(parsed)
    result = timeline.retry(parsed.ref_id)
    if parsed.commit_token is not None:
        token = result.get("data", {}).get("retry", {}).get("token")
        if result.get("status") != "preview" or token != parsed.commit_token:
            raise ValueError("retry preview token is stale or invalid; run timelines retry again")
        result = commit_preview(timeline, result)
        status = result.get("status")
        data = result.get("data") if isinstance(result.get("data"), Mapping) else {}
        if status in {"accepted", "merged", "rebased"} or data.get("status") in {"accepted", "merged", "rebased"}:
            result = {**result, "status": "landed", "pending_id": parsed.ref_id,
                      "summary": result.get("summary") or data.get("summary")}
    data = _retry_data(result)
    if parsed.json:
        return print_result(DomainResult.success(data), as_json=True)
    lines = [str(data["summary"] or data["status"])]
    if data["diff"] is not None:
        lines.append(f"diff: {data['diff']}")
    if data["token"]:
        lines.append(f"token: {data['token']}")
    if data["next"]:
        lines.append(f"next: {data['next']}")
    print("\n".join(lines))
    return 0


def _run(parsed, handler):
    try:
        return handler(parsed)
    except Exception as exc:  # errors retain structured conflict fields for --json callers
        if parsed.json:
            return print_result(_error(exc), as_json=True)
        from astrid.sdk.timeline._common import TimelineEditError

        if isinstance(exc, (TimelineEditError, ValueError)):
            print(str(exc), file=sys.stderr)
            return 1
        raise


def _configure_list(parser):
    parser.add_argument("ref", help="Timeline id or slug.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--all", action="store_true", help="Include landed and dropped records.")
    parser.add_argument("--all-actors", action="store_true", help="Include other actors on this machine.")
    parser.add_argument("--json", action="store_true")
    parser.set_defaults(handler=lambda p: _run(p, _cmd_list))


def _configure_show(parser):
    parser.add_argument("ref", help="Timeline id or slug.")
    parser.add_argument("ref_id", help="Pending record id or key.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--json", action="store_true")
    parser.set_defaults(handler=lambda p: _run(p, _cmd_show))


def _configure_drop(parser):
    parser.add_argument("ref", help="Timeline id or slug.")
    parser.add_argument("ref_id", help="Pending record id or key.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--reason", help="Why this saved edit was dropped.")
    parser.add_argument("--json", action="store_true")
    parser.set_defaults(handler=lambda p: _run(p, _cmd_drop))


def _configure_pending(parser):
    nested = parser.add_subparsers(dest="pending_command", required=True)
    nested.add_parser("list", help="List saved timeline edits.").set_defaults(_configure=_configure_list)
    nested.add_parser("show", help="Show a saved edit and its conflict packet.").set_defaults(_configure=_configure_show)
    nested.add_parser("drop", help="Mark a saved edit dropped without deleting it.").set_defaults(_configure=_configure_drop)
    for action in nested.choices.values():
        configure = action.get_default("_configure")
        configure(action)


def _configure_retry(parser):
    parser.add_argument("ref", help="Timeline id or slug.")
    parser.add_argument("ref_id", help="Pending record id or key.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--commit", dest="commit_token", metavar="TOKEN",
                        help="Commit only if the current retry preview still has this token.")
    parser.add_argument("--json", action="store_true")
    parser.set_defaults(handler=lambda p: _run(p, _cmd_retry))


def configure_pending(parser):
    _configure_pending(parser)


def configure_retry(parser):
    _configure_retry(parser)
