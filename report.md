# P4 case-collection review

## Result: FAIL

Reviewed author SHA `f69615515d02a3f1359235e1c971efcbef01f8a6` (`test(agent): collect P4 timeline commit cases`). This is a collection review only; it is not a P4 execution pass, native lifecycle proof, or H3 claim.

## Findings

1. **The single-edit CLI provenance is not a single edit.** `cases.json` cites `tests/packs/timeline/test_cli_native_sheet.py::test_export_preview_apply_and_undo` and records only `parent/clips/id:clip-a/at: 0 -> 5`. The cited test edits both `parent/clip:a` to `5` and `parent/track:picture` to label `Picture`, sends two commands, and then undoes the batch. The corpus therefore omits an authored field delta from its claimed one-edit case. Fix by citing an existing one-edit source test (for example a focused `TimelineSession.move` test) or by recording the complete two-edit case and changing its purpose/count.

2. **The Python source provenance is setup-only, not a Python edit.** `cases.json` cites `tests/sdk/test_timeline_sync.py::initial_bundle`, which constructs the initial bundle but does not call `TimelineSession.move`, `trim`, `commit`, or another edit API. It cannot substantiate the report's “CLI/Python/sheet front-door provenance” for the move. Replace the symbol with a real existing Python edit test, or label `initial_bundle` as fixture setup and add the actual Python edit source to the pending case.

The collection otherwise stays within scope: it adds only the owned P4 fixture/test files plus the requested root review report; it has no production/generated/schema/pin changes, no executor, golden, skip, xfail, or weakened assertion; and it does not claim accepted/merged/conflict/undo/rerun execution. The sheet and editing-conformance inputs are real and are exercised through `parse_sheet`, `load_fixture`, `bundle_from_document`, and `document_from_bundle`. The ten-note declaration records one commit, ten `doc.patch` commands/steps, ordered note IDs, show/history expectations, independent undo guards, a same-field conflict, and a bounded three-attempt rerun, but remains intentionally pending provider execution.

## Source provenance checked

These are the current Git blob hashes at author SHA `f6961551`; the paths exist and are the files resolved by the corpus:

| corpus source | path | blob SHA |
| --- | --- | --- |
| sheet | `tests/fixtures/timeline_editing/tiny.sheet` | `f9605090c73d0959a86e471fdc302c2ec9f7f0d7` |
| CLI | `tests/packs/timeline/test_cli_native_sheet.py` | `27e6bf6ee89f8308263b97d624a0bab0978ee210` |
| Python | `tests/sdk/test_timeline_sync.py` | `f59189d429fb96ed285c1fdd33d427b1d0d1f885` |
| editing-conformance document | `tests/editing_conformance/fixtures/recipe_m2_clip_trim.json` | `19f94e9052054e109ad8be7b8387bbc6c887f465` |

The sheet parser checks version `0ca00d3ed76f`, cuts `c1`/`c2`, both narration lines, and sound asset `Q`. The document check verifies `project-1`/`film` and an exact bundle round trip. These checks validate real input validity only; they are not P4 execution.

## Required pending execution seams

- **G2:** `astrid/sdk/timeline/sync.py:137` must provide the planned `timeline.open()` / `tl.commit(label | fn, merge=, dry_run=)` facade and bounded function rerun. The current `TimelineSession` has native one-shot methods only.
- **G3:** `astrid/sdk/timeline/document_diff.py:345` must be replaced by the document-to-`doc.patch` emitter before deletion. `astrid/packs/timeline/cli.py` and `astrid/sdk/timeline_sheet.py:849` must route the real CLI/sheet front doors through that producer and emit steps.
- **R2:** `astrid/sdk/timeline/sync.py:375` currently sends whole-publication `timeline.inverse`. Provider/runtime work must add guarded whole/per-step undo, previous-value checks, later-history/dependency scans including A→B→A, and authoritative step patches. R2 merge remains gated by C0c; apply the unique physical-root principle and never silently retarget an alias.

No full, live, socket, browser, install, merge, rebase, or push operation was run.

## Acceptance checks

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_commit_cases.py` — **PASS**, `2 passed, 2 warnings in 0.65s`. Warnings: the environment's pytest does not recognize `timeout` and `timeout_method`.
- `/root/.local/bin/ruff check tests/sdk/test_p4_commit_cases.py` — **PASS**, `All checks passed!`.
- `/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_commit_cases.py` — **PASS**, `Success: no issues found in 1 source file`.

The targeted checks pass because they validate the declarative collection and real parsing/round-trip inputs; they do not cover the missing execution seams or repair the two provenance mismatches above.

## Recommended next step

Correct the CLI/Python source mapping on a follow-up case-collection change, rerun the three checks, then leave the execution cases pending until G2, G3, and R2 are integrated and exercised against the real provider. Do not treat this collection as P4 or H3 evidence.
