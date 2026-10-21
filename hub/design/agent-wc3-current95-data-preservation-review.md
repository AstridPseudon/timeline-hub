# WC3 current95 data-preservation review

## Verdict

**REQUESTCHANGES — do not approve whole WC3 at this exact commit.**

Reviewed Agent branch `tl/agt-review-wc3-current95-data-preservation` at
`7a2fdcb6f27603702a0ed329caea1281c029a4e3` (`fix(sdk): route parent media
replacement through native session`), tree
`a170a3dcfcfffa514ba4e34eaf84248abbdd6632`. The tree includes the normal95
staging ancestry (`e35ad5e72`, Runtime source `95bd3c5f6d00...`) and the
current-preserving Main014 forward. No code, pin, schema, browser, render, or
full-suite changes were made by this review.

## Blocking preservation finding

The test delta is exactly `+299/-67`. It does not preserve every prior
positive assertion one-to-one:

- The prior genuine raw-media positive,
  `test_remote_parent_media_replacement_publishes_exact_closure_once`, was
  removed from the parent (`HEAD^`) and replaced at
  `tests/test_timeline_clip_replacement.py:229` with a refusal-only test.
  The old test asserted success, exactly one publication, the idempotency key,
  the selected asset, preserved `at`/`hold`, and `expected_head`. The new test
  asserts only validation refusal and no publication. This encodes a lost
  behavior as the intended behavior.
- The removed raw fixture is not a complete managed-media binding: its old
  registry row has `media_id` plus type/opaque data, but no generation ID,
  variant ID, or catalog digest. A compact source probe against that exact
  fixture produced `selected clip's authored media binding is not immutable
  and complete` from `_target_pin`, confirming the known normal014 boundary;
  fabricating a five-field old selection would change the fixture’s meaning.
- The old selected parent-and-occurrence adapter test was narrowed to an
  occurrence-only fake-session test. Its parent iteration and transport-level
  assertions for project/timeline, idempotency key, base revision/publication,
  operation, selection, and exact args do not map one-to-one. The current
  conformance test has a parent adapter call, but checks only success and the
  final asset, not the removed accepted-wire assertions.

This is compatible with the settled decision to delete the whole-closure
writer only if the raw-media Main gap remains explicitly open/draft-preserved.
Do not reintroduce that writer and do not replace its positive expectation with
refusal. Restore the original raw-media expectation as a strict expected-fail
with a comment naming the normal014 complete-old-five-field-binding
requirement, and restore bounded parent/occurrence assertion parity. The
complete five-field normal path may remain the only qualified native path.

## What is sound in this slice

The current source correctly requires all five fields and a matching verified
selection for the native path (`timeline_media_replacement.py:52-63`), resolves
source objects through the project generation/variant graph with exactly one
candidate (`:106-132`), and matches pending retries on owner, operation,
selection, intent, source object, and exact old/new pins (`:200-223`). The
opaque persisted flight is flushed rather than recaptured. The prior exact-
retry review’s malformed non-mapping finding is fixed in this tree.

## Evidence

Passed locally, with shared Runtime source read-only:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/test_timeline_clip_replacement.py tests/sdk/test_timeline_sync.py \
  tests/editing_conformance/test_recipe_parent_media.py \
  tests/editing_conformance/test_recipe_occurrence_media.py \
  tests/editing_conformance/test_commit_runtime_parent_media_swap.py
=> 166 passed, 22 skipped in 10.48s
```

Existing central named normal95 result for this exact tree (`a170a3dc...`):
`main95bd-added-gates-integration` — **26 passed** against
`/home/user/work/wt/rt-pin-95bd3c5f`, including the current parent media
conformance lane. `git diff --check HEAD^ HEAD` also passed.

Not run: full suites, browser/render suites, or live HTTP qualification. The
real-HTTP lost-ACK/restart proof exists on separate commit `593c2fd35` and is
not part of this exact reviewed commit, so it is not claimed here.

## Recommended next steps

1. Preserve the raw old-media positive as strict xfail/draft evidence rather
   than a refusal assertion; leave the whole-closure deletion intact.
2. Restore parent and occurrence accepted-wire assertion parity, including
   base pair, key/receipt, exact command, and timing/opaque preservation.
3. Qualify the native adapter’s parent lost-ACK/restart path on this exact
   normal95 tree before approving whole WC3.
