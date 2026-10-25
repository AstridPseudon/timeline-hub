# D100 source applicability validation

## Decision

The held D100 source is applicable to App's missing projection item-birth dependency, but current Agent `d4ba991638f7d94e6b9f91f5a463cd3587af00eb` is not product-qualified. The smallest proved source seam is the Agent provider's `State.shot_item_map`, `State._item_ids`, and `State.project_shot_items` in `astrid/sdk/timeline/_command_state.py`.

The current path reaches the registered Runtime commit provider and applies the source-item `doc.patch`. The retained exact own9 run stopped at `_command_state.py:369` with `identity_conflict: shot item correspondence changed`: one authored item was compared with an authenticated empty baseline. It stopped before Runtime acceptance, persistence, canonical reread, or duplication. `source_mapping.item_id_map` is custody, not allocation authority.

Held D100 changes the physical-source branch to authenticate the immutable image and its source pins, permits physical item membership replacement without extending placement alias maps, and keeps existing copied-placement correspondence strict. The `capture.py` exact-time changes are a separate D100 concern and do not affect this item-birth seam.

## Static checks

All checks were read-only and completed against the current worktree and held Git objects:

```text
ast.parse current/held production files: PASS
git diff --check current..held: PASS
git diff --check base..held: PASS
git diff --check worktree: PASS
retained App facts/predicate JSON parse: PASS (4 files)
```

Static call trace, by source symbols:

```text
tests/sdk/test_timeline_capture_projection.py:_RuntimeAuthoringWriter.commit_timeline
  -> RuntimeCommitService.commit_timeline
  -> registered provider / commands.execute
  -> State.set
  -> State.project_shot_items
  -> State.shot_item_map / State._item_ids
```

The exact source diff from current `d4ba` to held product source `d3b5` is 67 insertions and 20 deletions across the two production files. Current `d4ba` and captured core `a4e016` have identical relevant production blobs, so the captured core does not supply the held seam.

## Retained App evidence used

- Sol1650 and independent whole-path1650 agree on the first boundary and owner.
- Own9 1646 retained 9 tests, 9 setup errors, 0 failures, and 0 skips.
- The retained predicate map preserves 43 original assertions, 11 original test functions, 54 fixture statements, and the authored goldens, inputs, pins, and topology.
- These retained six-fixture controls are not treated as a product PASS.

## Missing/unpublished records

- The held test-repair object `fb9a47c2fc873e9ef388bfccec54de650ce2d308` has no retained ref. It is classified `EXACTMISSING` for source attribution; no fetch or alternate route was attempted.
- The frozen candidate-sdk tree lacks `tests/sdk/test_timeline_capture_projection.py`; this is also `EXACTMISSING`, with no alternate route.
- No missing record was used to invent source attribution or a product result.

## Not run / next step

No product tests, pytest, service, browser, full suite, source installation, Runtime guard work, SWAP/WAL work, or source edit was performed. The required next acceptance is one exact own9 rerun after the reviewed Agent seam is normally adopted, followed by independent review; it must retain the nine selectors and all original predicates. Runtime is not the owner of this missing dependency.
