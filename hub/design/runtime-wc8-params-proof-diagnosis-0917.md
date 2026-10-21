# Runtime WC8 parameter proof diagnosis

## Result

The second actual failure is a test oracle/fixture assertion error, not a
product failure. The existing guarded inverse/redo contract preserves the
authored revision while publishing a new history edge with a new
`publication_id`. The product's revision/publication pair semantics remain
unchanged.

The source correction is test-only and limited to
`tests/editing_conformance/test_native_sheet_ordinary_runtime.py` on Agent
tree `33f88975eea0006a624c5e0a95bd2fd307695028`.

## Exact prior failures

1. `rt-m2-wc8-params-actual-neighbor-0905-rt-wc8-current14-integration-1021090849-21270`, snapshot tree
   `9916d1c8e7d9190b941eee6cbf4af778f289252d`, failed at the stale witness.
   It passed detached legacy `null_text` to `NativeSheet.apply`; the product
   correctly refused the changed sheet shape with
   `sheet structure/basis is read-only; additions and removals are unsupported`
   before the intended retained-basis guard. The corrected source uses the
   retained `native.text` and the exact basis-error match.
2. `rt-m2-wc8-params-corrected-actual-0913-rt-wc8-current14-integration-1021091407-21888`, snapshot tree
   `45a46eeda044f33c99f0fb118cc6cd0da373d5dd`, reached the intended stale
   refusal and all preceding null/rename accept, reload, inverse, and redo
   assertions. It then failed only because the final assertion compared the
   current head to the earlier `renamed_head`: revision
   `...1dbbe54577eb` was unchanged, while redo legitimately changed
   publication `txn-b5bbe938517a481697f64f8f2d4c2bac` to
   `txn-2707d8b6c2034f228c55a21858aba84d`.

The existing implementation and passing tests explicitly require this
behavior: an equal authored state is still a later publication, and guarded
undo must refuse an earlier publication after an intervening equal-state
write. The plan's accepted identity is therefore the pair, not revision-only
or publication-only equality.

## Test-only correction

The original rename assertions remain unchanged: accepted `renamed_head`
revision/data, parameter order, owner, sibling, reload, inverse, and redo
document equality are still asserted. The corrected node additionally:

- captures the undo head;
- asserts redo keeps `renamed_head['revision_id']`, returns its new receipt as
  the head publication, and uses a distinct publication;
- asserts the redo history entry's `previous` pair is the undo head and its
  `records.undo_of` names the undo publication;
- captures the actual post-redo head/history and request count immediately
  before the stale original-basis attempt, then requires exact history,
  outbox, and request-count equality after refusal.

No assertion was deleted, weakened, converted to revision-only equality, or
used to erase publication identity. No product, source guard, schema, pin,
fixture, or live caller changed. The retained opaque clear limitation remains
unclaimed because the detached grammar cannot represent omission.

## Evidence

Independent data-safety review `rt-m2-wc8-params-safety-review-0903` was
**APPROVE** for Agent product `c0671afddb34f4fe6b8ca66f511df9fc530cc344`.

Before the correction, exact node collection passed (1 node), the compact
non-socket redo/unchanged-write probes passed (5 tests), and the permitted
neighbor lane passed (18 tests, 93 deselected). After the correction:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" PYTHONDONTWRITEBYTECODE=1 \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
tests/sdk/test_timeline_sheet_native.py tests/editing_conformance/test_native_sheet_current.py \
-k 'unsupported_cells_refuse_whole_batch_before_queue or custom_pack_param_refuses_without_client_inputs or formula_bound_params_are_a_named_requirement_and_refuse_before_queue or detached_mixed_edit_with_opaque_neighbor_is_staged'
```

Result: **18 passed, 93 deselected**. AST syntax parsing and `git diff --check`
also passed. The corrected actual HTTP/socket/body test was not rerun, and no
full, browser, renderer, install, or live-socket suite was run in this task.

The future single diagnosed final actual requires independent
assertion/data-safety approval of this correction first. This report does not
claim actual qualification or a whole-WC8 result.
