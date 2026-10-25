"""Bounded, offline registered-provider commit benchmark.

Run with PYTHONPATH=.:tests:<Agent checkout>, the Runtime dependency interpreter,
and --scratch beneath TMPDIR. Uses the integration editing fixture unchanged;
only registered commits grow its accepted state. Output contains aggregates,
never requests, documents, receipts, identifiers or raw profiler dumps.
"""

from __future__ import annotations

import argparse
import cProfile
import json
import shutil
import time
from contextlib import contextmanager
from pathlib import Path
from types import CodeType

import pytest

from runtime_protocol.util import canonical_json
from tests import test_timeline_commit_integration as integration


def check_disk():
    if shutil.disk_usage(Path(__file__).resolve()).free < 4_000_000_000:
        raise RuntimeError("offline source benchmark stopped below 4 GB free")


@contextmanager
def editing_fixture(root):
    check_disk()
    root.mkdir()
    with pytest.MonkeyPatch.context() as monkeypatch:
        film = integration.film.__wrapped__(root, monkeypatch)
        agent = integration.agent.__wrapped__(film, None, monkeypatch)
        fixture = integration.editing.__wrapped__(film, agent)
        edit = next(fixture)
        try:
            yield edit
        finally:
            fixture.close()


def grow(edit, history, tracks):
    for index in range(tracks):
        command = edit.agent.track(edit.agent.bundle(edit.document()), "parent",
                                   {"id": f"offline-track-{index}", "kind": "visual"})
        result = edit.commit(edit.body([command]), f"grow-track-{index}")
        assert result["data"]["status"] == "accepted"
    for index in range(history):
        result = edit.commit(edit.body([edit.move("music-bed", index % 2 + 1)]),
                             f"grow-history-{index}")
        assert result["data"]["status"] == "accepted"


def profile_rows(profiler):
    rows = []
    for entry in profiler.getstats():
        code = entry.code
        rows.append({
            "file": Path(code.co_filename).name if isinstance(code, CodeType) else "<builtin>",
            "line": code.co_firstlineno if isinstance(code, CodeType) else 0,
            "function": code.co_name if isinstance(code, CodeType) else code,
            "calls": entry.callcount, "recursive_calls": entry.reccallcount,
            "self_seconds": entry.inlinetime, "cumulative_seconds": entry.totaltime,
        })
    return sorted(rows, key=lambda row: row["cumulative_seconds"], reverse=True)


def replay(edit, *, profiled=False):
    base, document = edit.head(), edit.document()
    first = edit.body([edit.move("music-bed", 5, document=document)], base)
    disjoint = edit.body([edit.move("music-other", 6, document=document)], base)
    preview = edit.body([edit.move("music-bed", 7, document=document)], base)
    preview["dry_run"] = True
    samples = []
    accepted = None
    for name, body, key in (("preview", preview, "preview"),
                            ("accepted", first, "first"),
                            ("merged", disjoint, "disjoint"),
                            ("retry", first, "first")):
        check_disk()
        before = integration.rows(edit.service) if name in ("preview", "retry") else None
        profiler = cProfile.Profile() if profiled else None
        start = time.perf_counter()
        if profiler is not None:
            profiler.enable()
        try:
            result = edit.commit(body, key)
        finally:
            if profiler is not None:
                profiler.disable()
        elapsed = time.perf_counter() - start
        if name == "retry":
            assert result == accepted
        elif name == "preview":
            assert result["data"]["status"] == "preview"
            assert result["data"]["would_status"] == "accepted"
            assert result["receipt"] is None
        else:
            assert result["data"]["status"] == name
            edit.assert_readback(result)
            if name == "accepted":
                accepted = result
        if before is not None:
            assert before == integration.rows(edit.service)
        samples.append({"operation": name, "seconds": elapsed,
                        "profile": profile_rows(profiler) if profiler is not None else None})
    return samples


def run(scratch, repeats=2, dimensions=((0, 0), (4, 0), (4, 16))):
    if not 1 <= repeats <= 3:
        raise ValueError("repeats must be 1..3")
    rows = []
    for history, tracks in dimensions:
        for repeat in range(repeats + 1):
            root = scratch / f"history-{history}-tracks-{tracks}-run-{repeat}"
            with editing_fixture(root) as edit:
                grow(edit, history, tracks)
                document = edit.document()
                rows.append({"history_growth": history, "track_growth": tracks,
                             "repeat": repeat, "profiled": repeat == repeats,
                             "document_bytes": len(canonical_json(document).encode()),
                             "history_entries": len(edit.history()),
                             "samples": replay(edit, profiled=repeat == repeats)})
    return {"scope": "offline RuntimeService -> registered Agent -> port -> Store -> auth",
            "limits": ["Not the original App element document/history/lifecycle",
                       "No HTTP, mounted handler, door, daemon, browser or renderer",
                       "First realm is process-cold; subsequent realms have warm schema caches",
                       "Profiled times include cProfile overhead; compare unprofiled rows"],
            "measurements": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=2)
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=False)
    result = run(args.scratch, args.repeats)
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
