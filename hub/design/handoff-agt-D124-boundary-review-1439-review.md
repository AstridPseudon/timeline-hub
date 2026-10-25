# D124 boundary-core review

Verdict: **PASS, bounded source diagnosis only**. This is not a product-green
verdict and does not authorize merging the still-failing regression without the
Runtime owner correction.

## Source finding

- Agent `_commit_patch.py:615-618` records materialization on the step's final
  command ordinal, while `:641-665` derives the proposed bindings from the
  complete step input/output closures. `:701-718` emits both shot and internal
  source-to-successor edge pairs with the exclusive owner and step identity.
- Runtime `timeline_commit_auth.py:2868-2873` builds each later command's
  sequential `command_input` from the preceding command output.
- Runtime `timeline_commit_auth.py:2908-2918` passes that command input as
  `boundary` while retaining the outer step input as `step_input`.
- Runtime `timeline_commit_auth.py:498-499` correctly authenticates a
  `commit.materialization` image against `step_input`, but
  `:565-580` derives `before_rows`, the before shot, and before internal image
  from `boundary`. For the second command this is the intermediate boundary,
  not the source boundary used by the binding. The resulting rejection at
  `:577` is therefore a real boundary mismatch, not evidence of bad Agent
  materialization.

## Contract cross-check

C0 `contract/commit-v2.md:314-322` distinguishes step/command evaluation
boundaries; `:388-412` requires provider effects to preserve the relevant
before/after union and authenticated materialized source-to-successor relation;
and `:614-651` makes sequential step boundaries authoritative. The Agent
binding and Runtime image check follow these rules; the Runtime edge comparison
does not for the later command.

## Test construction

`tests/sdk/test_d124_sequential_materialization.py` is the sole candidate delta
(58 lines). The `native_child` fixture registers the existing
`create_runtime_commit_service()` on a real `RuntimeService` and uses one child
occurrence. The source-custody test proves three distinct revisions, one
synthesized step with command ordinals `[0, 1]`, two complete edge pairs, final
ordinal attribution, and singleton owner custody. The grouped test submits the
same two commands through the registered service and retains accepted track
order plus inverse restoration assertions. It contains no mock validator,
fabricated records, collector, grouping change, dropped binding, or ordinal
move.

The source-custody test inspects the production Agent plan before service
submission; the grouped test is the provider acceptance path. Thus the
provider-backed RED is genuine, while the companion PASS is a custody
comparator rather than a second Runtime submission.

## Scope limits

The four retained originals remain UNKNOWN/unreplayed. No all-four closure is
claimed and no shared cause is inferred. Runtime source was read-only; no
Runtime fix was applied.
