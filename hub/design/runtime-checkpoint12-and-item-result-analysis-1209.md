# Runtime checkpoint 12 and RT08 item/global result analysis

## Decision context

Read `PLAN.md` and Runtime `STATUS.md`. The owner 11:48 interim rule is
applied: independent diff review plus original targeted assertions before an
interim merge; full checkpoints/journeys run on the farm; M4 gates are
unchanged. Runtime STATUS identifies b92d3e7a05eec65c142294ef4873edd059e9b31d
(`tree 6abc2f117391de8e7e35c0283f575a002199894d`) as the current integration
source, says a red checkpoint blocks subsequent Runtime merges, and keeps RT08
item/global materialization open.

## Existing request: 12:00 integration checkpoint

Request: `runtime-full-retained-owned-temp-integration-1021120516-19340`

- Scope: `target=integration:runtime`, Runtime full-retained-owned-temp-
  integration suite; no file filter. The recorded command used the retained
  owned-temp wrapper and `python -m pytest -q -n 3`, with
  `ASTRID_CHECKOUT=/home/user/work/agent`.
- Source: Runtime tree
  `6abc2f117391de8e7e35c0283f575a002199894d`, corresponding to integration
  commit b92d3e7a05eec65c142294ef4873edd059e9b31d.
- Result: **PASS**, exit code `0`, duration `389s` (pytest body `387.26s`).
- Counts: `6002 passed, 26 skipped, 15 xfailed, 12 warnings`; nonzero test
  count: **0**.
- Distinct failures: none. The skips are platform-specific Windows cases;
  the xfails are the recorded retired direct-writer/commit-replacement holds.
  The retained owned temporary root was `/tmp/rt-full-ov9ml974`.

This is a green integration checkpoint. The checkpoint rule does not block
the next Runtime merge on this result.

## Existing request: RT08 item/global targeted acceptance node

Request:
`rt-m2-rt08-item-global-witness-source-1148-private017-agent4b7-integration-1021120712-7227`

- Scope: one targeted integration node on candidate target
  `rt-m2-rt08-item-global-witness-source-1148`, specifically
  `tests/test_timeline_projection_occupancy.py::test_startup_provider_materializes_source_items_and_refuses_global_item_occupancy`.
  The recorded command used Runtime candidate tree
  `065e602ba4fa336e162977cac199b48388d97e30`, Agent checkout
  `/home/user/work/wt/agt-pin-4b7a2712`, and the `private017-agent4b7-
  integration` suite.
- Result: **FAIL**, exit code `1`, duration `3s` (pytest body `1.62s`).
- Counts: `1 failed`; nonzero test count: **1**. There were no passes,
  skips, xfails, or zero-test conditions in this node.
- Named test: `test_startup_provider_materializes_source_items_and_refuses_global_item_occupancy`.
- First concrete cause: the test's renderer-unavailable fixture replaces
  `runtime_protocol.service.evaluate_closure` with a function that raises
  `AssertionError("save evaluated a scene")`. Before the item/global
  assertion, `publish_source_items()` calls `RuntimeService.publish_parent_composition()`;
  the service reaches `runtime_protocol/service.py:3076` and calls
  `evaluate_closure`, producing that assertion. The trace is therefore:
  `tests/test_timeline_projection_occupancy.py:427` -> helper line 99 ->
  `runtime_protocol/service.py:3076` ->
  `tests/test_timeline_commit_integration.py:72`.

Classification: **product**, not fixture or environment. The fixture is an
intentional renderer-independent-save guard, and the failure is a deterministic
call from the Runtime save/publication path into scene evaluation. The test
never reaches the item/global occupancy assertion, so this node does not prove
or disprove that occupancy behavior.

This is candidate-only evidence and is separate from the green integration
checkpoint; it is not an integration checkpoint failure. RT08 item/global
materialization remains open and this candidate cannot be accepted until the
save-path cause is addressed and a later authorized acceptance establishes the
item/global behavior. No retry was requested.

## Actions and limits

No product, test, suite, dependency, schema, version, or pin was changed. No
test was run or requested by this worker; only the two existing result records,
their summaries/logs, source metadata, PLAN.md, and Runtime STATUS.md were
read. No prior passing proof was replayed and no exhaustive audit was started.
