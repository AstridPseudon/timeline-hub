# Agent F V2 fixture handoff — 0903

Result: **PASS for the two named detached provider fixture nodes; quality gate caveat recorded.**

## Exact source/delta

Starting from the F-provider repair branch `fad05679a` (`tl/agt-F-provider-0847`):

- `tests/sdk/test_timeline_commit_provider_scalar.py` now installs `schema_options(configured_project_pack, old)` before creating the selected element clip. At the replacement boundary it creates the replacement document with the authentic new project-pack `schema_source` pin, installs the corresponding retained snapshot/object custody, and then restores it. The original `dependency_changed` and complete `(head, entries, documents)` no-state-change assertions are unchanged.
- `tests/sdk/test_timeline_commit_graph_roots.py` patches only the target test's local `root_values` function so the new occurrence has `duration_ms=3000` while the child operation continues to write/read `hold=3`. This satisfies C0 timing validation and preserves original IDs plus reload/inverse/redo closure assertions.

Only those two test files changed. Production provider/V2/Runtime validation, schema, generated files, locks, ceilings, and all unrelated tests remain untouched.

## Evidence and counts

- Exact named nodes: **2 passed in 2.36s**.
- Exact nodes with four focused local neighbors: **6 passed in 18.60s**.
- Strict timing/schema negative neighbors: **14 passed in 3.68s**.
- Scoped Ruff: pass.
- Normal Ruff: **2149 current / 2149 baseline**.
- Vendor lock: pass (`ok runtime.lock.json`).
- Artifact manifest: pass (`artifacts.json is current`).
- Diff check: pass.
- Mypy baseline comparator: no output for 180 seconds and exit 124 under a guard; **not verified**. The requested comparator was not silently replaced by a weaker claim.

## Limits and ownership

This is detached Agent fixture evidence only. It does not claim Runtime acceptance, integration introduction, upstream status, or a full-suite result. No full/live/browser/heavy suites were run. No shared installs, service rows, refs, or other worktrees were touched.

The graph `2000ms → 3000ms` is the sole behavior/setup decision: C0's half-open timing rule requires a 3-second hold to fit, and the task explicitly protects `hold=3`. No contract escalation was needed. Agent integration/review owns merge and integrated rerun; environment/test ownership should resolve and rerun the stalled mypy comparator.
