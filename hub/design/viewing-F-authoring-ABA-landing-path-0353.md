## Report — FAIL

NEW13559 has a source-backed Agent projection mismatch during undo.

Path:

1. CLI publication uses `timeline_document.py:327-333` → `TimelineSession.commit_many`; the retained publication path succeeds with `occurrence.swap-media` and `doc.patch`.
2. Undo uses `TimelineSession.undo()` → `_flush()` (`sync.py:411-451`, `514-546`) and submits `timeline.inverse`.
3. Agent’s final prepared document correctly calls `document_from_bundle(..., inverse_records=inverse_records)` (`commit.py:1192-1193`).
4. The private sequential landing capture instead calls `inverse_closure(...)` without `inverse_records` (`_commit_patch.py:477-482`). `document_from_bundle` only removes inverse-introduced media/document pins when those records are supplied (`commit.py:366-398`).
5. Runtime’s sequential validator compares that captured landing output with the prepared canonical document and rejects the mismatch as `invalid_records` (“landing execution output differs from the prepared document”). The retained failure matches this path exactly.

Owner: `vw-F-authoring-ABA-landing-sol-0349`, specifically `_commit_patch.py`. Smallest correction: thread the authenticated `inverse_records` through the inverse execution-boundary projection, centralizing it in `inverse_closure`; no Runtime, binding, guard, schema, or client retargeting change is indicated.

The passing publication path does not cover this inverse case: ordinary publication has no inverse source restoration or manifest-removal projection, so both projections use the same ordinary document conversion.

Offline probe:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/vw-F-authoring-ABA-landing-path-0353:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
tests/editing_conformance/test_occurrence_media_manifest_inverse.py::test_compiled_popup_inverse_restores_exact_original_document \
tests/editing_conformance/test_authoring_undo_projection.py::test_single_inverse_captures_transient_roots_and_exact_parent \
tests/editing_conformance/test_authoring_undo_projection.py::test_final_stage_uses_authenticated_parent_after_retained_pin_removal
```

Result: `6 passed in 2.02s`.

The initial Agent-only probe stopped before collection because `runtime_protocol` was absent from `PYTHONPATH`; rerunning with the existing Runtime worktree succeeded. No product, test, or fixture files changed. `git diff --check` passed and status is clean.

The original private packet remains unavailable, so this is source-backed diagnosis plus retained-fixture confirmation, not a reconstruction of that packet or a product completion claim. DONE marker and commit message were written.