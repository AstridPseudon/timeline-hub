# RT03 accepted film-reference projection authority review

## REQUESTCHANGES

Source commit: `4e562de0de44335ea29add039d1e0a6dfcfc3a64`  
Source tree: `7ff848323c76c6642417896da50d3cd0d4f8346e`

The accepted projection correctly uses only the literal
`occurrence.provenance.astrid.timeline_reference` v1 binding
(`version`, `reference_id`, `role: "source"`, `asset`), resolves the
occurrence-owned registry asset, normalizes the selected media identity, and
requires exact accepted media-manifest custody. Missing, contradictory,
out-of-manifest, and occupied bindings are preflight refusals inside the
acceptance transaction. The project catalog/RK01 paths are untouched.

The authority/data-loss boundary is not safe to merge yet:

1. `runtime_protocol/timeline_commit_store.py:827-829` treats every
   `reference_id` in the previous `timeline_revisions.references_json` as
   owned by this occurrence projection. A clear or restore therefore deletes
   prior references that were not emitted by this carrier. An isolated probe
   seeded a legacy `legacy-ref` row and included it in the prior snapshot next
   to the accepted `reference-1`; accepting a candidate with empty occurrence
   provenance removed `legacy-ref`.
2. `_apply_reference_projection` deletes
   `timeline_reference_state` by global `id` at lines 848-850, without first
   proving that the state row belongs to this timeline/reference projection.
   This can damage shared/global state if a malformed or legacy snapshot names
   an ID owned elsewhere. The reference row deletion is timeline-scoped, but
   the companion state deletion is not.
3. `desired` is keyed only by `reference_id` at lines 798-801. Two occurrence
   bindings with the same identity and same normalized value are silently
   coalesced. The Agent contract makes the binding occurrence-owned and calls
   for unique identities; duplicate ownership should refuse (or be explicitly
   proven legal) rather than collapse silently.

Required correction: derive removals only from references proven to be this
carrier's prior occurrence projection (or conservatively retain any reference
without that ownership proof), and guard/scope state deletion against the
accepted timeline row before mutation. Add focused regressions for an
unrelated prior reference, cross-timeline/global state, and duplicate
occurrence identity. Keep the original strict native positive OPEN; the
prepared fixture is not native authoring proof.

## Evidence

- `ASTRID_CHECKOUT=/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/tests:$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_reference_projection.py tests/test_timeline_projection_occupancy.py`: **23 passed**.
- `ASTRID_CHECKOUT=/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/tests:$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_reference_authority.py -k 'service and not genuine_accepted'`: **72 passed, 73 deselected**.
- Central test service: `request-test rt-m2-review-reference-projection-authority commit-integration --files "tests/test_timeline_reference_projection.py tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider"`, then `wait-test`: **11 passed, 5 deselected**.
- Central targeted request: `request-test rt-m2-review-reference-projection-authority targeted --files "tests/test_timeline_reference_projection.py tests/test_timeline_projection_occupancy.py tests/test_timeline_reference_authority.py"`, then `wait-test`: **22 passed, 1 deselected, 145 errors**; the errors were environment/setup failures in the authority file, not product assertions. It is not a product pass.
- `git diff --check`: passed; review worktree clean.

The source worker's local socket result (**7 passed, 4 permission-blocked**) is
not counted as product evidence. No full, renderer, or browser suite was run.
