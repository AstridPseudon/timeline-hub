# P4 early case collection

Status: collection complete; P4 execution is intentionally pending. This is not a P4 pass.

## Collected corpus

- `tests/sdk/fixtures/p4_commit_cases/cases.json` is a small declarative corpus with provenance for the real sheet, CLI, Python, and editing-conformance inputs.
- `tests/sdk/test_p4_commit_cases.py` validates the real inputs with `parse_sheet`, `initial_bundle`, `load_fixture`, `bundle_from_document`, and `document_from_bundle`.
- `single-real-edit` records the existing `parent/clip:a` move from `at=0` to `at=5`, with CLI/Python/sheet front-door provenance and show/history readback expectations.
- `ten-notes-one-commit` records ten exact absent-to-text field deltas under `parent/clips/id:clip-a/app/org.example/p4_note`, one ordered `doc.patch` and step per note, one commit, history/show readback, independent step undo, a same-field concurrent conflict, and a bounded three-attempt Python re-run scenario.

All commit, conflict, undo, and re-run outcomes are marked `pending-contract-dependent`; no live Runtime/provider execution is claimed.

## Exact missing seams

These are the real current seams that still need integrated implementation before this corpus can execute:

- `astrid/sdk/timeline/sync.py:137` (`TimelineSession`) has the existing registered-command session, but not the planned `timeline.open()` / `tl.commit(label | fn, merge=, dry_run=)` provider facade or bounded function re-run.
- `astrid/sdk/timeline/commands.py:116` admits registered operations and legacy inverse/restore, but has no v2 `doc.patch` operation for these cases.
- `astrid/sdk/timeline/document_diff.py:345` is the existing document-diff-to-native-command writer; G3 must provide the document-to-`doc.patch` emitter before the planned deletion of this route.
- `astrid/sdk/timeline/sync.py:375` sends whole-publication `timeline.inverse`; R2 still needs guarded per-step undo with previous-value and later-commit scans.
- `astrid/packs/timeline/cli.py` and `astrid/sdk/timeline_sheet.py:849` expose the current CLI/sheet native front doors; G3 must route their accepted edits through the v2 commit producer while preserving these real inputs.
- `astrid/sdk/_remote_timeline.py:127` forwards a commit body, but does not itself establish the v2 provider contract, authoritative step patches, conflict reply, or history evidence.

C0c root addressing is still pending in the control docs, so this collection does not assume final root-resolution or per-step effect/undo wire shapes.

## Validation

The requested Agent venv is absent: `/home/user/work/venv-agent/bin/python` does not exist. No dependency was installed or changed. The available read-only author/reviewer toolchain was used instead.

Passed:

```text
PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_commit_cases.py
2 passed, 2 warnings in 0.66s

/root/.local/bin/ruff check tests/sdk/test_p4_commit_cases.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_commit_cases.py
Success: no issues found in 1 source file
```

The two pytest warnings are the fallback environment reporting unknown `timeout` and `timeout_method` config options. The requested-path equivalents were unavailable because the venv path does not exist.

No full/live/browser suite was run.
