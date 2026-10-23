# G5 SDK second-failure parallel restore assessment — 1928

## Disposition

**The second test's unmodified full-document equality is conditionally wrong
under C0, but the second test's actual current failure cause is not proven.**
The G5 SDK remains draft-only and P1 remains **NO-GO**. No product or test
file was changed, and no new service, HTTP, original FOUR, c271, full suite,
or test-body execution was run by this assessment.

This is distinct from the first-test finding. The corrected 1907 packet proves
two ordinary `TimelineSession.move` commits were accepted and then the first
test stopped at `test_timeline_checkout_history_runtime.py:148`, where
`find_version` returned `None`. The 1917 source solution correctly identifies
that first-test source cause: `find_version` discarded each retained row's
`publication_id` at `timeline_sheet.py:1065-1067`. The 1917 patch is on
`697c8fd3b51562fb18e45dedecc56723984db2eb`, not on this assessment base.
It does not prove the second test's dynamic reset outcome.

## Proven source and contract facts

1. The second test restores the original revision and digest through the
   ordinary SDK path at `tests/sdk/test_timeline_checkout_history_runtime.py:273-280`.
   C0 permits the result to have the old accepted revision and a new
   publication receipt. Agent `_ack` requires the canonical document's parent
   revision to equal `data["accepted_revision_id"]` and separately requires a
   fresh receipt ID at `astrid/sdk/timeline/sync.py:95-129`. Runtime's commit
   provider validates `restored_from` against the retained source revision and
   digest at `runtime_protocol/timeline_commit_store.py:893-897`; it emits the
   canonical document from the provider plan at
   `astrid/sdk/timeline/commit.py:1161-1195`.

2. `Checkout.document()` returns the full derived-field-stripped bundle, not
   merely authored payload bytes: `astrid/sdk/timeline/publish.py:629-633`,
   with `_strip_derived` removing only underscore-prefixed derived keys at
   `astrid/sdk/timeline/doc.py:170-175`. Therefore
   `Checkout(original).document()` includes
   `original["base_parent"]["publication_id"]`.

3. The assertion at line 283 compares that old publication to the post-restore
   checkout. If the second `_reset_base()` succeeds, C0 requires the current
   base pair to be `(original revision, restored receipt publication)`, not
   `(original revision, original publication)`. Thus the line-283 equality is
   expected to fail solely on publication identity even when every canonical
   payload, closure, source pin, explicit null, asset, and opaque field is
   exact. This is an oracle boundary, not permission to drop the assertion.

4. The current source has the exact-pair path needed for a successful reset.
   `_reset_base` reads the current head, writes it without a local undo step,
   and retires draft history at `astrid/sdk/timeline/publish.py:406-430`.
   `store.fetch_bundle` obtains the current head pair from Runtime history and
   hydrates it explicitly at `astrid/sdk/timeline/store.py:451-492`.
   `_remote_timeline.open_bundle` verifies the requested revision/publication
   pair and canonical closure before installing the publication identity at
   `astrid/sdk/_remote_timeline.py:169-207`.

5. The consumed-draft guard is independently present and must remain. A reset
   retires both local history and redo directories at
   `astrid/sdk/timeline/checkout.py:323-336`; local undo/redo refuses when no
   same-base unsent step remains at `astrid/sdk/timeline/checkout.py:338-362`.
   The existing assertions at lines 284-293 preserve both guards and prove a
   newly created post-reset draft step remains undoable/redoable. The first
   `_reset_base` also has a source-level failure branch that preserves the old
   bundle but still retires history (`publish.py:408-414`); static source alone
   cannot say which branch the lost run took.

## Proven, conditional, and unavailable evidence

### Proven

- Assessment worktree is the requested unmodified Agent base
  `89c38c9355f5d4bcc68597ec74e4729435a7a07a`.
- Corrected 1907 reached both ordinary moves with accepted Runtime/provider/
  store/coordinator entry and exit packets, then failed the first test's
  retained-history lookup at line 148. It did not execute the second test.
- The 1902 `internal_error` was the observer's missing `_event(name)` argument
  before the Runtime provider path; it is not a Runtime restore cause.
- The 1917 source reconstruction found the first-test publication omission and
  its six exact-pair regressions passed in the candidate source's bounded
  selection (127 total in that report). That evidence is source/regression
  evidence for `find_version`, not a second-test restore execution.
- C0 identity rules allow `accepted_revision_id == original revision_id` with
  `receipt.receipt_id == new publication_id`; the current-pair control test
  already encodes this at
  `tests/editing_conformance/test_current_pair_reader.py:101-146`, including:
  canonical-document equality, new base publication, retained historical
  publication read, head pair, and no unsent draft undo/redo.
- The retained 1738 report stated a restore-case document/base mismatch after
  a 2-pass/2-fail FOUR result, but the full packet is unrecoverable. It does
  not preserve the second reset request, exception, current-head pair,
  accepted canonical closure, or enough detail to assign the mismatch to
  publication-only equality versus stale payload/source closure.

### Conditional only

- If the second `_reset_base()` succeeded on the current source, line 283 is
  wrong only because it compares `P0` to the valid new `Prestore`; the source
  supports exact canonical restoration under `(R0, Prestore)`.
- If the unpinned current read failed, `_reset_base` could leave the prior
  accepted-move bundle in place while retiring draft history. That would be a
  product stale-snapshot defect and would explain a payload/closure mismatch,
  but this is a static possibility, not an observed result here.
- No static reading can distinguish those branches, and no current second-test
  run is authorized by this brief. Do not convert the conditional branch into
  an actual-cause claim.

## Concrete unapplied minimal test adaptation

Do not apply this in this worker and do not weaken/delete the original test
before manager-owned meaningful current FOUR evidence. If the expected boundary
is accepted, replace only the line-283 oracle with an identity-aware oracle
that preserves every other field and keeps all lines 279-293:

```python
        new_publication = restored['receipt']['receipt_id']
        assert restored['data']['accepted_revision_id'] == original['base_parent']['revision_id']
        assert new_publication != original['base_parent']['publication_id']
        expected = copy.deepcopy(original)
        expected['base_parent']['publication_id'] = new_publication
        assert draft.bundle['base_parent'] == expected['base_parent']
        assert draft.document() == Checkout(expected).document()
        assert draft.bundle['source_mapping']['_runtime_document'] == (
            original['source_mapping']['_runtime_document']
        )
```

This changes exactly the publication identity mandated by the accepted receipt;
it retains the original revision, digest, parent payload, every child/closure
pin, source mapping, asset/null/opaque values, and all public document fields.
The existing undo/redo refusal and fresh-step undo/redo assertions remain
unchanged. The `source_mapping['_runtime_document']` assertion is the explicit
raw canonical-closure guard; the full `document()` comparison retains the
public source pins and opaque fields. A product payload or closure mismatch
must continue to fail.

## Bounded next control

Manager-owned next control, after meaningful current FOUR evidence:

1. Keep `89c…` and P1 **NO-GO** until the independent 1917 exact-pair source
   review is complete; do not merge or activate from this assessment.
2. Preserve the unmodified second test for that control run, while capturing
   only the ordinary restore reply/receipt, the second reset's current history
   head pair, `fetch_bundle/open_bundle` result or exception, and canonical
   closure identity. No synthetic state or replacement fixture.
3. If the result is `(R0, Prestore)` with exact closure and only line-283
   publication mismatch, manager may apply the snippet above as a minimal
   contract correction. If canonical payload/closure remains stale or differs,
   classify the product defect at the unique allowed seam
   `_PublishMixin._reset_base -> store.fetch_bundle`, require exact capture of
   that failure, and do not grant a guard waiver or introduce a new policy.

## Checks and limits

Read-only checks performed:

```text
git status --short                                      PASS (clean)
git diff --check                                        PASS
git diff --check 89c38c9..697c8fd3                      PASS
AST/source hash lock for both original test bodies      PASS
reviewed production source SHA-256 capture              PASS
Agent identity                                           89c38c9355f5d4bcc68597ec74e4729435a7a07a
Runtime identity                                         2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d
Runtime tree                                             f79a2355cfb39d9ada7721978bd20d5702105778
```

Original body hashes on this base are unchanged:

```text
test_checkout_reload_undo_cli_redo_uses_retained_history
  source 1ea4f8c1a8342c049933e580f70282a9fef87fdc73f9f45366c854664b513056
  AST    f2a95ff5f3ae236097cf339fd7c3053df53c24256d7913be6875bede8267f7aa
test_retained_restore_does_not_reopen_consumed_draft_steps
  source 43a5cab36e8464974c86af04ed37e138ea7ec441c3d1180235587bba4b363b1f
  AST    8e60a62f573bdc277433bb7fb2fba3738240b99a7106828976e68a1630a254f5
```

No test command was executed: the brief explicitly prohibits the original
body, a new service/HTTP run, FOUR, c271, and full suites. Existing 1907/1917
packets report credential scans with zero findings; no credentials were added
by this assessment. No product/test files, pins, schema, daemon, environment,
or shared dependency were modified.
