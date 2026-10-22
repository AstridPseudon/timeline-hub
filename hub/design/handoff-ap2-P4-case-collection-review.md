# Handoff: P4 case-collection review

Result: **FAIL** for the collection review at author SHA `f69615515d02a3f1359235e1c971efcbef01f8a6`.

The targeted acceptance checks all pass, but two provenance defects prevent accepting the collection:

1. `single-real-edit` cites `tests/packs/timeline/test_cli_native_sheet.py::test_export_preview_apply_and_undo` while recording only the clip move. That real test also edits the parent track label to `Picture` and sends two commands, so the corpus omits a real field delta from its claimed one-edit case.
2. Its Python source cites `tests/sdk/test_timeline_sync.py::initial_bundle`, which only constructs fixture state. It does not perform a Python edit, so it cannot substantiate Python front-door provenance. Use a real `TimelineSession.move`/`trim` test symbol or label this as setup and add the actual edit source.

Source paths exist at the reviewed author tree. Blob hashes: sheet `f9605090c73d0959a86e471fdc302c2ec9f7f0d7`; CLI `27e6bf6ee89f8308263b97d624a0bab0978ee210`; Python `f59189d429fb96ed285c1fdd33d427b1d0d1f885`; editing-conformance document `19f94e9052054e109ad8be7b8387bbc6c887f465`.

The rest of the collection is appropriately declarative and pending: real sheet parsing and document load/round-trip are exercised; the ten-note case specifies one commit with ten ordered `doc.patch` commands/steps, show/history expectations, per-step undo guards, same-field conflict, and bounded rerun. It claims no accepted/merged/conflict/undo/rerun execution and makes no H3/native-lifecycle claim. The root `report.md` is the requested review artifact, not a product delta; no production/generated/schema/pin files changed.

Checks:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_commit_cases.py` — PASS, 2 passed, 2 warnings (`timeout` and `timeout_method` config warnings).
- `/root/.local/bin/ruff check tests/sdk/test_p4_commit_cases.py` — PASS.
- `/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_commit_cases.py` — PASS.

Pending seams to report:

- G2: `astrid/sdk/timeline/sync.py:137` needs `timeline.open()` / `tl.commit(label | fn, merge=, dry_run=)` and bounded function rerun.
- G3: `astrid/sdk/timeline/document_diff.py:345` needs the document-to-`doc.patch` emitter; CLI and sheet paths must emit v2 commands/steps through it.
- R2: `astrid/sdk/timeline/sync.py:375` currently emits whole-publication inverse only; guarded whole/per-step undo, previous-value/later-history dependency scans including A→B→A, and authoritative step patches remain to be implemented. R2 merge remains gated by C0c and must apply the unique physical-root principle.

No full/live/socket/browser suite or install was run. Correct the two source mappings, rerun the three checks, then execute only after G2/G3/R2 integration.
