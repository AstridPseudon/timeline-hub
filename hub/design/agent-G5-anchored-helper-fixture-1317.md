# G5 anchored helper fixture — test-only report

## Result

Added only `tests/sdk/test_timeline_helper_capture.py`.

The new fixture uses the existing genuine `restructure_runtime` Runtime service,
creates the `media.transcript/v1` document through the public document client,
reads the stored document back from that service, derives its canonical pin with
Runtime's `content_digest`, and uses the existing `capture_clip_add`,
`capture_anchor`, and command executor. It asserts the real project/timeline
scope, the authenticated base revision/publication pair, the exact transcript
pin and stable word ID, the native `anchor.transcript` dependency, and the
source binding. Missing-pin and schema-valid forged-word variants both refuse
without changing the Runtime SQLite dump.

Existing helper/cut/restart/disjoint/strict negative bodies were not changed;
an AST body comparison found 10 existing function bodies unchanged.

## Evidence

```text
pytest ... test_genuine_anchor_capture_has_exact_source_scope_and_base_pair
1 passed in 11.66s

pytest ... test_missing_or_forged_anchor_binding_never_writes
2 passed in 28.36s

pytest ... test_cut_nudge_restart_merges_other_cut[None] ... [+1s]
2 passed in 19.89s

pytest ... test_cut_nudge_restart_merges_other_cut["second"]
failed before nudge capture: candidate.timing: missing exact word binding for
('occ-film', 'film', 'inside') .on
```

The retained inline-word child-cut setup still lacks an authenticated retained
transcript binding in the timeline closure. I did not retry it or turn the
failure into an expected refusal. This is the precise remaining authority/setup
blocker; no production or Runtime change was made.

```text
ruff check --no-cache tests/sdk/test_timeline_helper_capture.py
All checks passed!
git diff --check
PASS
scripts.reshape.compare_ruff_baseline
current=2149 baseline=2149
scripts.reshape.compare_mypy_baseline
current=1912 baseline=1912
```

No full/browser/HTTP/native suite was run. No generated/schema/pin/shared
dependency or Git state was modified.
