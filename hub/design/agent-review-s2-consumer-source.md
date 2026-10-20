# Agent S2 consumer-source verdict

Verdict: conditional pass for source preparation only. `fc69684789f52ef1d65467dc9b590893ed8d7b3b` is a narrow descendant of current Agent integration (`78d548cf`) and the approved frozen S2 source (`26ef2bbb31b4892fdd7c15ee5b20700bd40cb933`). I found no new unchecked authority or schema narrowing in the reviewed prep. It is not ready for integration until the normal paired Runtime/generated-client pin closes the two intentional strict xfails below.

## Reviewed correctness

- `astrid/core/timeline/schema/edit-command.schema.json` is byte-identical to the approved S2 bytes: SHA-256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`. The canonical source has 48 `$defs` and 22 `EditCommand` operation conditionals. Published floors and the reviewed optional `ClipSetElementArgs.schema_source` addition remain guarded by `tests/sdk/test_timeline_current_union_schema.py`.
- Producer proposals retain the original admitted target, proposal digest, task/attempt/executor identity, fence and runtime epoch. `producer.guard` is first-only, requires a non-empty proposal, and is rejected without Runtime `producer_attempt` capture. `commit.py` passes the verified pin into execution/rebase; the provider records an exact `producer_attempt:<task_id>` authority dependency. No caller-supplied pin or source bytes become authority.
- Element source resolution is bounded to the exact document pin and selected pack owner. `_hydrate` captures `clip.set-element` and `clip.set-params` schema sources; `_schema_resolver` requires the selected admitted element, exact retained pack document and snapshot object before execution. Raw element-only refusal and retained declaration tests preserve head, history, opaque values, inverse/redo and replay behavior.
- Keyed views have the intended scope split. `inspect_timeline` and `show` remain read-only and do not create view artifacts. `create_timeline_view` is the write-scoped operation, receives an explicit/retry-stable idempotency key through `_RemoteFamily._typed`, and tests cover fresh keys, same-key replay, lost acknowledgement, and `projects:write` refusal.
- Current integration behavior survives the prep merge: history, trim, capture projection, auto-placement, shared auto-placement, and shot-pool targeted tests passed. `_timing_evaluators._timing_number` is unchanged and remains the exact-fraction helper.

## Pin prerequisites

1. The final normal Runtime/generated-client pin must add the keyed `create_timeline_view(..., idempotency_key=...)` contract. The current generated client in the prep still exposes the old three-argument method (`astrid_runtime_client/generated.py:932`), while `WorkspaceClient.create_timeline_view` now intentionally requires the key (`astrid/sdk/workspace_client.py:555-572`). Re-run the keyed-view source tests and the matching Runtime transport/scope checks after regeneration.
2. Remove the temporary strict xfail from `tests/editing_conformance/test_commit_runtime_m1.py` for `touched_basis=False` once the genuine matching pair passes. Preserve the original positive disjoint-rebase/undo assertions exactly.
3. Remove the temporary strict xfail from `tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes` only after Runtime accepts the native recorded `producer.guard` metadata. Preserve the original numeric-positive assertions exactly; do not replace them with refusal expectations.
4. Do not claim producer acceptance from this source review. The current Runtime pin is known to refuse at the normalized guard boundary (`producer_dependency_unavailable` / “producer authority requires its guard record”); the final pin must prove preview, acceptance, restart-safe exact retry, changed-key refusal, undo and no history mutation on refusal.

## Explicit debt and limits

The public WC4 element helper in `astrid/sdk/timeline_elements.py:16-72` was intentionally retained and is unchanged by this prep. It still performs its legacy live admission/whole-candidate publication path and has no WC4 deletion-ledger closure. That is explicit follow-up debt, not new authority introduced by S2; the native `clip.set-element` path must remain the qualified authority for new callers, and no helper cut should be claimed here.

No product code was changed in this review. I did not run Runtime integration/socket/browser/App journeys, full or `full*` suites, generated-client regeneration, the final normal pin, or WC4 closure. The producer positive and original M1 disjoint positive remain unverified until that pin.

## Exact checks

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -o cache_dir=/tmp/agt-s2-review.../.pytest_cache tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_producer_guard.py tests/sdk/test_native_timeline_facades.py tests/sdk/test_workspace_client_timeline_commit.py tests/editing_conformance/test_settled_proposal_contract.py` — **140 passed** in the private `fc696847` snapshot.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_checkout_history.py tests/sdk/test_timeline_checkout_history_boundaries.py tests/sdk/test_timeline_capture_projection.py tests/sdk/test_timeline_clip_trim_provider.py tests/editing_conformance/test_recipe_m2_clip_trim.py tests/editing_conformance/test_recipe_m2_auto_placement.py tests/editing_conformance/test_recipe_m2_shared_auto_placement.py tests/editing_conformance/test_recipe_m2_shot_pool.py` — **325 passed, 9 deselected**.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/core/test_timeline_element_publication.py tests/editing_conformance/test_recipe_clip_set_element.py tests/sdk/test_timeline_selected_schema.py tests/sdk/test_timeline_clip_scalar_provider.py` — **84 passed**.
- Static checks: `git diff --name-status 78d548cf..fc696847`, exact schema SHA/count check, and source inspection of the resolver/guard/view paths — passed; no changes to shared dependencies, Runtime, generated client, integration worktrees, or ledger.
