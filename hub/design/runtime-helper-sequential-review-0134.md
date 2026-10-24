## Source review: FAIL for assessment0125 attribution; actual owner UNKNOWN

- Exact retained failure: `tests/sdk/test_timeline_helper_capture.py::test_contiguous_helpers_keep_sequential_steps[True]` refused at Runtime `timeline_commit_auth.py:2196` (“replay binding duplicated or omitted”); no write accepted.
- Runtime’s invariant is explicit: every moved-head `doc.patch` change maps to `(ordinal, "patch", change_ordinal)`; only changed physical reads map to `(ordinal, "read", ref, path, phase)`. Entries must be unique, complete, source-bound, owner-bound, and image/digest-authenticated.
- Agent’s production path is `commit.py:1141–1153, 1192–1208` → `_commit_preview.capture_sequential_execution:25–80`. The private carrier has exactly six top-level fields: `schema_version`, `context`, `original`, `landing`, `replay_bindings`, `prepared_digest`.
- Runtime receives it at `timeline_commit_port.py:177–204, 664–673`, then validates through `timeline_commit_store.py:867–881` and `timeline_commit_auth.py:1983–2287`.
- Current Agent `3b0dc9e80f` (tree `b0dd9758…`) changed journal/helper normalization and tests; the historical 851/67ba reports are insufficient proof that current3b0 emitted the failing map. Current Runtime HEAD is `db11ea829` (tree `a92a576a…`), and the validator/port/store sources are unchanged from failing Runtime `8ea0766f5`.
- The retained causal capture available is a successful `original9` preview, not the review0107 failure. The actual failing replay list versus Runtime’s computed expected map is missing.

No source edits, tests, typecheck, lint, or known-failure rerun were performed. Worktree remains clean.

Request only these already-retained artifacts if available: worker0048 `commands.txt` and `numeric-capture.json.gz`; G5 `boundary-001-execute.json` through `boundary-005-execute-error.json` and `sequential-cut.log`, including complete envelopes, records, request/context, prepared digest, replay map, heads, and intervening history.