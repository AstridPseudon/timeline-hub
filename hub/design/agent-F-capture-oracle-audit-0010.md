# Report

Disposition: both failures are a stale test/oracle seam, not a production gap.

- `prepare_filmstrip()` builds the exact capture snapshot with parent revision/content digest, child/shot pins, registry, and working-copy metadata.
- `invocation.py:2872–2892` intentionally keeps canonical captures inline at the SDK→Runtime boundary. Saved captures and candidate captures with forwarded `authoring_preview` enter `runtime_capture`; SDK does not publish CAS there.
- Runtime then converts the inline snapshot to `capture_snapshot_ref` via `rewrite_spec_snapshots()` and publishes the exact JSON through `publish_snapshot()`. Runtime validates revision/candidate bindings before claim.
- The failing test uses `tests.sdk.test_visualize_authority_objects.Runtime`, whose task double records the pre-admission spec and does not perform Runtime rewrite/publication. Its expectation of no inline snapshot and an already-published reference therefore fails for both `working_copy=False` and `True`.
- The later same-file test explicitly expects inline `capture_snapshot`, matching the production branch. This is corroborated by `tests/sdk/test_capture_source_runtime.py`, which separately tests both inline admission and post-publication reference materialization.

The original assertions protect valuable invariants—CAS digest integrity, project/timeline/revision or candidate identity, dependency pins, and host round-trip—but they are asserted at the wrong boundary. The faithful raw-published boundary is the real Runtime fixture’s `create_task()` → snapshot rewrite/publication → claim → `GenericPackHost` materialization path.

Recommended bounded fix: restore/adapt the real Runtime closure fixture from `39535a495`, or split the proof into:

1. SDK pre-admission: assert inline snapshot, duplicate authority equality, forwarded candidate, and no SDK CAS write.
2. Runtime post-admission: assert `capture_snapshot_ref`, exact CAS digest, source kind, revision/candidate bindings, and materialized source equality.

No production change, refusal, skip, xfail, assertion weakening, schema change, or authority fabrication is justified.

Tests were not run, per the explicit read-only/no-test instruction. Worktree remains clean. Retained parent full evidence remains unchanged: 17,159 passed, 262 failed, 5 errors, 4 skipped; no new full or body rerun was requested. Frozen R4 does not contain this current capture-closure test or applicable contract.

