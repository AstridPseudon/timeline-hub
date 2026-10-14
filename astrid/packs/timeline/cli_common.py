"""Small helpers shared by the working-copy verbs (lint, lines, words, discard, duplicate, status).

Kept out of ``cli.py`` so each verb module stays short. Everything here takes the parsed argparse namespace
and reads the timeline name from ``parsed.ref`` (the product parser's positional).
"""
from __future__ import annotations

import argparse
import sys
from collections.abc import Mapping
from typing import Any


class VerbError(Exception):
    """A user-facing failure: the message goes to stderr and the verb exits with ``code``."""

    def __init__(self, message: str, code: int = 1):
        super().__init__(message)
        self.code = code


def guard(default_code: int):
    """Turn a VerbError, TimelineEditError or SheetError into one stderr line and an exit code."""

    def wrap(fn):
        def run(parsed: argparse.Namespace) -> int:
            from astrid.sdk.timeline._common import TimelineEditError
            from astrid.sdk.timeline_sheet import SheetError

            try:
                return fn(parsed)
            except VerbError as exc:
                print(str(exc), file=sys.stderr)
                return exc.code
            except (TimelineEditError, SheetError) as exc:
                print(str(exc), file=sys.stderr)
                return default_code

        run.__name__ = fn.__name__
        run.__doc__ = fn.__doc__
        return run

    return wrap


def need_project(parsed: argparse.Namespace) -> str:
    if not getattr(parsed, "project", None):
        raise VerbError("--project P is required (the timeline is named inside its project)", 2)
    return parsed.project


def draft_name(parsed: argparse.Namespace) -> str:
    """The working copy a command uses: --draft NAME, else the current one (last checked out), else main."""
    if getattr(parsed, "draft", None):
        return parsed.draft
    try:
        from astrid.sdk.timeline_checkout import current_draft, resolve_ids

        project_id, timeline_id, _head = resolve_ids(need_project(parsed), parsed.ref, client=parsed.client)
        return current_draft(project_id, timeline_id)
    except Exception:  # noqa: BLE001 - the runtime is unreachable: the default name
        return "main"


def working_copy(parsed: argparse.Namespace, *, create: bool) -> tuple[Any, bool]:
    """(checkout, existed). ``create=True`` makes the working copy from the head when there is none."""
    from astrid.sdk.timeline_checkout import Checkout, find_draft

    project = need_project(parsed)
    name = draft_name(parsed)
    existed = find_draft(project, parsed.ref, name, client=parsed.client) is not None
    if not existed and not create:
        return None, False
    return Checkout.draft(project, parsed.ref, name, client=parsed.client, fresh=bool(getattr(parsed, "fresh", False))), existed


def short_rev(revision: Any) -> str:
    text = str(revision or "")
    return text.removeprefix("authoring-parent-revision-")[:8] or text


def clips_changed(n: int) -> str:
    """The one count every verb prints for a working copy: clips added, removed, moved or edited."""
    return f"{n} clip{'s' if n != 1 else ''} changed"


def cuts_summary(tl: Any) -> str:
    return f"{len(tl.cuts)} cuts · {len(tl.clips())} clips · {len(tl.words())} words"


def cap(lines: list[str], limit: int = 30) -> list[str]:
    """A long re-flow prints its first lines and a count; the rest is one `timelines diff` away."""
    if len(lines) <= limit:
        return lines
    return lines[:limit] + [f"… and {len(lines) - limit} more (timelines diff shows them all)"]


def check_lines(report: Any, cuts: list[str] | None = None) -> list[str]:
    """After an edit: valid or not, and NEW lint on the cuts it touched (the full report is `timelines check --all`)."""
    brief = getattr(report, "brief", None)
    if callable(brief):
        return brief(cuts=cuts) if cuts is not None else brief()
    lines = str(report).splitlines()
    return [lines[0]] + [ln for ln in lines[1:] if ln.startswith(("!", "  ", "lint"))]


def working_copy_view(parsed: argparse.Namespace) -> dict[str, Any] | None:
    """The unpublished working copy of this timeline (its document and edits), or None."""
    from astrid.sdk.timeline_checkout import Checkout, find_draft

    try:
        path = find_draft(parsed.project, parsed.ref, getattr(parsed, "draft", None), client=getattr(parsed, "client", None))
    except Exception as exc:  # the runtime is not reachable: say so, show the published head
        print(f"working copy: not checked ({exc}); showing the published head", file=sys.stderr)
        return None
    if path is None:
        return None
    checkout = Checkout.load(path)
    return {
        "bundle": checkout.document(),
        "path": str(path),
        "base_revision": checkout.base_revision,
        "changes": list(checkout.edits().get("changes") or []),
    }


def working_banner(working: Mapping[str, Any]) -> str:
    """The one-line banner show, lint and diff print when they read the working copy."""
    return (f"WORKING COPY · {clips_changed(len(working['changes']))} vs published {working['base_revision']} · "
            "--published for the live version")
