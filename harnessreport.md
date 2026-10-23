# P4 mounted-facade early proof

## PASS

Commit under test: `131561e2ba99eab41ce3588cfdee59e193aeeff3` (`feat(timeline): mount document patch emitter`).

The new `tests/sdk/test_p4_commit_v2.py` proves two bounded cases through the public Python facade:

- `timeline.open("p", "t")` → `Timeline.commit` free bundle edit → mounted G3 `emit_document_commands` → `TimelineSession.submit` → the existing generated submission boundary. The connected provider then executes the emitted `doc.patch` through the real Agent command engine/R1 implementation. The returned canonical document contains the changed clip position.
- Ten public `Timeline.command` calls, each with one independent note `doc.patch`, followed by one `Timeline.commit`. The submitted request has ten commands, ten contiguous command ordinals, ten step patches and the explicit `merge: "fields"`, `reads: []` declarations. The provider executes the request and the returned canonical document contains all ten note values while preserving timing, asset and track fields.

The test uses a complete parent-only Runtime document for the original P4 parent edit. The existing generated test provider’s compile helper omits unchanged child revisions when a document has an unrelated child closure; adding a child mutation would no longer be the single-edit case. The joined child-closure path remains covered by the existing G3 test in `tests/sdk/test_timeline_open_commit_v2.py`.

## Exact checks

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_commit_cases.py tests/sdk/test_p4_commit_v2.py
4 passed, 1 warning in 1.05s
warning: pytest config option `timeout` is unknown in this environment

/root/.local/bin/ruff check tests/sdk/test_p4_commit_v2.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_commit_v2.py
Success: no issues found in 1 source file

git diff --check
pass (no output)
```

## Not claimed / gaps

- This is provider/submission evidence, not official Runtime acceptance: `connected.Generated.commit_timeline` is a test transport whose command execution is real, while HTTP, Runtime coordinator/port acceptance, authentic Runtime receipts and CLI process execution are not exercised here.
- CLI G3 coverage is unavailable on this head. The generic fallback in `astrid/packs/timeline/cli.py:_cmd_edit` (`:3270-3305`) calls `_edit_checkout` and `tl.save`; the ordinary move path in `astrid/packs/timeline/cli_native.py:commit_edit` (`:191-214`) submits a native command directly. Neither calls `timeline.open`/G3.
- Sheet G3 coverage is unavailable on this head. `NativeSheet.apply` (`astrid/sdk/timeline_sheet.py:849-875`) previews native commands and submits `session.commit_many`; legacy `apply_sheet` uses the detached checkout path. No sheet caller reaches the mounted emitter.
- R2 is not integrated. There is no proof of whole-commit or per-step guarded undo, including ten independent note undos, A→B→A history scans, or merged-commit inversion.
- The new ten-note case does not claim a ten-note conflict or function re-run. Existing G2 evidence in `tests/sdk/test_timeline_open_commit_v2.py` covers bounded Python re-run/new-key behavior for a native move; a document-patch note conflict/re-run remains unexecuted.
- `show` readback and authoritative `history` readback of step labels/patches/dependencies are unexecuted. The request seam is checked; the connected provider does not return R2/R2r step history data.
- The full v2 reply matrix (merged canonical reply fields, dependency/effect attribution, invalid structured errors, dry-run/history shapes, idempotency replay and Runtime `Idempotency-Key` behavior) is not qualified by this early proof.

The three named G2/R2/P4 readiness handoff paths were not present in the frozen Agent checkout; `contract/commit-v2.md` was read from the Runtime worktree. No product files, fixtures, generated files or shared dependencies were changed.
