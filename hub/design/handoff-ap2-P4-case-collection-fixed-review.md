# Handoff: P4 case-collection fixed review

Result: **PASS — collection only** at author SHA `d0e1b5140cf93fe8bb229220e390e24c82280a45`. This is not P4 execution proof, an H3 result, or a native lifecycle claim.

The bounded correction fixes both prior provenance findings. The single-edit case now cites the real CLI move test `tests/packs/timeline/test_cli_commit_move.py::test_ordinary_edit_literal_move_uses_native_outbox` and the real Python edit test `tests/sdk/test_timeline_sync.py::test_failed_ack_write_recovers_the_original_flight`. The former has one literal `edit` move (`--clip a --on 5`); the latter performs one `TimelineSession.move("parent/clip:a", 5)`, with later flush only recovering that edit. The test now AST-validates exactly one cited CLI edit call and one cited Python `.move` call.

The ten-note corpus is retained: one commit with ten ordered `doc.patch` commands/steps, show/history expectations, independent per-step previous-value/later-history undo guards, same-field conflict, and bounded three-attempt rerun. It remains explicitly pending and claims no execution outcome. Existing sheet parsing and document load/round-trip APIs validate real inputs. No synthetic executor/golden, weakening, skip, xfail, production/generated/pin edit, or unsupported proof claim was added. The author delta has no root `report.md` or other unintended management artifact.

Verified Git blob hashes:

```text
tests/fixtures/timeline_editing/tiny.sheet                                      f9605090c73d0959a86e471fdc302c2ec9f7f0d7
tests/packs/timeline/test_cli_commit_move.py                                     e21ca372250774874ad8a8ccfece347b08834bb9
tests/sdk/test_timeline_sync.py                                                  f59189d429fb96ed285c1fdd33d427b1d0d1f885
tests/editing_conformance/fixtures/recipe_m2_clip_trim.json                      19f94e9052054e109ad8be7b8387bbc6c887f465
```

Checks:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_commit_cases.py` — **PASS**, 2 passed, 2 config warnings for unknown `timeout` and `timeout_method`.
- `/root/.local/bin/ruff check tests/sdk/test_p4_commit_cases.py` — **PASS**.
- `/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_commit_cases.py` — **PASS**.
- `git diff --check f69615515d02a3f1359235e1c971efcbef01f8a6 HEAD` — **PASS**.

Pending execution seams:

- **G2:** `astrid/sdk/timeline/sync.py:137` — planned `timeline.open()` / `tl.commit(label | fn, merge=, dry_run=)` facade and bounded function rerun.
- **G3:** `astrid/sdk/timeline/document_diff.py:345` — document-to-`doc.patch` emitter and CLI/sheet v2 command/step routing.
- **R2:** `astrid/sdk/timeline/sync.py:375` — guarded whole/per-step undo, previous-value plus later-history/A→B→A scans, and authoritative step patches.
- **C0c:** adopted unique physical-root principle is still pending approval; R2 merge remains gated by C0c.

No full/live/socket/browser suite or install was run. Integrated G2/G3/R2 execution is required before this collection can substantiate P4.
