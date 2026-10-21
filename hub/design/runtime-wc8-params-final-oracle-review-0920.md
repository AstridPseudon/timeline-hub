# WC8 retained-parameter corrected actual oracle review

Verdict: **APPROVE** the exact corrected actual-test blob below, for the
retained WC8 opaque-parameter test only. This approval permits carrying this
unchanged test onto the current Agent preserving port. It does not qualify the
live actual, the whole WC8 family, or any product beyond the independently
approved Agent `c0671afddb34f4fe6b8ca66f511df9fc530cc344`.

## Candidate identity and scope

- Review tree/commit: `5c00518939fdfe8f064a9713a9a91ea2746513fe`
- Review tree: `254d2e975ef06b14214db08ebb439a579042e926`
- Reviewed path: `tests/editing_conformance/test_native_sheet_ordinary_runtime.py`
- Reviewed Git blob: `f561128f89b756eb3c624264a81a0e1402032872`
- Reviewed file SHA-256: `e001ccb91bc88807e77a86e753ff90713698b5ad85e2c4811398f61df112cad4`
- Reviewed node: `test_current014_detached_opaque_null_rename_uses_retained_basis_and_guarded_http[detached-historical]`

The review worktree was clean. Relative to c067, the candidate changes only
the one ordinary-runtime test file; the product and the already approved c067
implementation are outside this review. Relative to the 33f test, the
correction is limited to the redo publication/history assertions and the
full stale pre/post history snapshot.

## Assertion and data-safety review

The diagnosis of the two earlier results is correct:

1. The 0905 actual used detached legacy `null_text` as the stale witness.
   That changed the sheet shape and correctly stopped at the structural
   refusal before the intended retained-basis guard.
2. The 21888 actual reached the intended stale refusal, but its final
   `runtime.history()['head'] == renamed_head` assertion incorrectly required
   redo to reuse the prior publication. The authored revision remains equal;
   guarded redo is a new publication/history edge.

The corrected test preserves the original positive path and strengthens only
the erroneous oracle:

- The initial retained `NativeSheet` remains the original object loaded from
  the first outbox artifact. Its retained `_bundle` and `_basis` are checked;
  the stale witness is derived from that object’s original `native.text`, not
  from the later renamed export or a refetched head.
- The first opaque-null publication still checks the exact retained bundle and
  basis, one expected `clip.set-params`, exact request base revision and
  publication, `source == {'via': 'sheet'}`, null data, sibling preservation,
  restart, inverse, and redo.
- The rename is re-exported from the accepted null head. The original rename
  basis, request body, renamed data, parameter order, reload, inverse data,
  and redo document checks are unchanged.
- After rename inverse, `undone_head` captures the actual undo head. After
  redo, `redone_head` requires the same authored `revision_id`, a new
  publication equal to the redo receipt and distinct from `renamed_head`.
  The matching history item must point to `undone_head` in `previous` and name
  the undo receipt in `records.undo_of`. This is the normal publication-pair
  semantics and covers the exact failure diagnosed at 21888.
- Immediately before the stale attempt, the test snapshots the actual current
  `runtime.history()` (including its current head), outbox bytes, and
  `len(runtime.calls)`. It then applies a changed text based on the original
  `native.text` and requires the retained basis error. After refusal it
  requires byte-identical outbox state, identical complete history/head, and
  no additional call. Thus the stale attempt cannot refresh basis, queue
  pending work, or send HTTP.
- The explicit comment correctly leaves opaque omission/clear unclaimed;
  `opaque=null` is a value, not an omission.

No assertion was deleted, weakened, converted to revision-only equality, or
made expected-to-fail. The replaced final head assertion was invalid because
it treated a new publication as an error; the replacement is stronger because
it asserts the whole post-redo history is unchanged by the stale refusal.

## Checks run and reused

Direct permitted no-socket neighbor lane on this exact tree:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" PYTHONDONTWRITEBYTECODE=1 \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
tests/sdk/test_timeline_sheet_native.py \
tests/editing_conformance/test_native_sheet_current.py \
-k 'unsupported_cells_refuse_whole_batch_before_queue or custom_pack_param_refuses_without_client_inputs or formula_bound_params_are_a_named_requirement_and_refuse_before_queue or detached_mixed_edit_with_opaque_neighbor_is_staged'
```

Result: **18 passed, 93 deselected**.

The exact actual node was collected once as one parametrized case:

```text
...test_native_sheet_ordinary_runtime.py::test_current014_detached_opaque_null_rename_uses_retained_basis_and_guarded_http[detached-historical]
1 test collected
```

`git diff --check` and Python syntax compilation passed. The prior diagnosis’s
five no-socket redo/unchanged-write probes and the 18-neighbor evidence were
reused as directed; the failed 0905/21888 actuals were not replayed.

Not run: the corrected actual HTTP/socket test, any live-socket or full suite,
render, browser, install, or product re-audit. The final actual must be run
once by the central service against the approved current preserving port,
using exactly the blob/hash and node above; no test variation is covered by
this approval.

## Disposition

**APPROVE** — exact test blob `f561128f89b756eb3c624264a81a0e1402032872`,
SHA-256 `e001ccb91bc88807e77a86e753ff90713698b5ad85e2c4811398f61df112cad4`,
scope limited to the single corrected WC8 opaque null/rename actual node on the
current preserving Agent port. No smallest correction is required.
