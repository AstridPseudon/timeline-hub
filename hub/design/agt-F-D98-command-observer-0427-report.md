Implemented one source-only observer: [tools/timeline_d98_command_observer.py](/home/user/work/wt/agt-F-D98-command-observer-0427/tools/timeline_d98_command_observer.py).

- Passively traces Runtime `timeline_commit_auth.validate_claims`.
- Emits only safe field paths, shapes, SHA-256 hashes, record ordinal, and hashed input tuple identity.
- Fail-closed if tracing/introspection is unavailable.
- No product/test/Runtime edits; no original execution.

Checks passed:

- In-memory compile
- `ruff check`
- `mypy`
- `git diff --check`
- AST source-only audit

Observer SHA-256: `d751532f2a5f1d4be74f038b3c55a8e9745620580db72609b5399aaa08a1428a`

Exact selectors for the receiving MAIN run:

1. `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[image-add]`
2. `tests/editing_conformance/test_recipe_m2_auto_placement.py::test_exact_capture_replay_inverse_and_redo[image-anchor]`
3. `tests/editing_conformance/test_recipe_occurrence_media.py::test_same_alias_materialized_whole_payload_read_allows_exact_undo_redo`

Activate by copying the observer as private evidence `sitecustomize.py`, setting `D98_EVIDENCE_DIR`, and prepending that evidence directory to the existing route’s `PYTHONPATH`. Verify an `observer_active` record and allow only the documented safe JSON keys. The D73 launcher currently overwrites `PYTHONPATH`, so the receiving body must inject the evidence path before Python starts; this task did not alter that launcher.

No behavior claim or D82 classification is made until the bounded run produces safe records. Missing exact command-pair handoff artifacts remain unverified.

Commit message written; `DONE` created.