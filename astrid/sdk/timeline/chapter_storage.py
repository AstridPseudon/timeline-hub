"""Bind chapter storage adaptation to the existing story and timing compiler."""
from __future__ import annotations

import copy

from astrid.core.timeline.authoring_bundle import compile_authoring_candidate as _compile
from astrid.core.timeline.chapter_storage import ChapterStorageError, split_chapter_storage


def resolved_chapters(bundle):
    from astrid.sdk.timeline.compiler import TimingInputs, compile_timing
    from astrid.sdk.timeline.story import _compiled_checkout, resolve_ranges
    compiled = compile_timing(TimingInputs(copy.deepcopy(bundle)), commands=())
    tl = _compiled_checkout(compiled)
    rows, findings = resolve_ranges(tl)
    if findings:
        raise ChapterStorageError("; ".join(f["message"] for f in findings))
    return [r for r in rows if r["range"]["kind"] == "chapter"]


def compile_candidate(bundle):
    """One final physical compilation, using canonical resolved frame edges."""
    ranges = resolved_chapters(bundle) if bundle.get("storage_policy") == "chapters" else None
    return _compile(bundle, resolved_chapters=ranges)


def restructure(self, *, expected_head: str, policy: str = "chapters"):
    from astrid.sdk.timeline.commands import CommandError
    if expected_head != self.bundle.get("base_parent", {}).get("revision_id"):
        raise CommandError("restructure expected_head differs from the exact pinned base")
    if policy != "chapters":
        raise CommandError("restructure supports only the chapters storage policy")
    probe = copy.deepcopy(self.bundle)
    probe["storage_policy"] = policy
    # Validate the entire conversion before changing even detached authored state.
    split_chapter_storage(probe, chapters=resolved_chapters(probe))
    self.bundle["storage_policy"] = policy
    return self


def guard(tl, command):
    from dataclasses import replace

    from astrid.sdk.timeline import commands
    expectations = dict(command.expect or {})
    states = commands.entity_states(tl)
    # Guard exactly the storage choice and complete range selection (beats and
    # display names included). Rebase never silently chooses different walls.
    for path in ("storage_policy", "config.app.astrid.ranges"):
        key = "parent::" + path
        if command.expect is not None and key not in expectations:
            raise commands.CommandError("recorded restructure lacks exact storage/range preconditions")
        current = commands.state_at(states, "parent", path)
        if command.expect is not None and path.endswith(".ranges"):
            def selection(state):
                if state.get("state") != "present" or not isinstance(state.get("value"), list):
                    return state
                return [{k: v for k, v in row.items() if k != "name"} if isinstance(row, dict) else row
                        for row in state["value"]]
            if selection(expectations[key]) == selection(current):
                expectations[key] = current  # chapter display names are not storage identity
        expectations.setdefault(key, current)
    args = dict(command.args)
    if command.expect is not None:
        args["expected_head"] = tl.bundle["base_parent"]["revision_id"]
    return replace(command, expect=expectations, args=args)
