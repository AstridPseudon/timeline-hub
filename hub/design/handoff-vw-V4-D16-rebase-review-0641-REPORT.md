# V4 independent D16 positive-rebase disposition review

## Verdict

**PASS — D16 deferral is required for this particular positive.**

The retained positive is an unbound legacy-word case that the current v2
production path cannot provide at all. An earlier refusal cannot preserve the
test's later positive assertions, so adapting the test to that refusal would
be unsound. The disposition in
`vw-V4-D16-rebase-disposition-0637/REPORT.md` is correct and may be delivered
as a bounded current limitation/future-work paragraph.

## Scope and settled rule

- Reviewed against exact Agent base
  `3e4261e9694c7bd7c1b5fada9bf01d91007bcc80`.
- Applied the D16 header/INBOX ruling at 06:22: an earlier refusal may be
  adapted only while retaining every original assertion; D14-style deferral is
  allowed only when v2 cannot provide the behavior at all.
- The original positive function is
  `tests/editing_conformance/test_native_word_anchor.py::test_follow_rebases_original_choice_after_source_move_and_reorder`.
- No product, test, fixture, recipe, generated, pin, package, assertion, or
  deletion change was made. No new escalation or C0 ruling is needed.

## Why an earlier refusal cannot satisfy this test

The unchanged test requires all of the following after the first source move:

1. the original captured `voice` choice survives although ordinal reselection
   now selects `other`;
2. the stale request lands with its expected rebase/merged status and authored
   choice;
3. projected timing follows the moved source;
4. restart preserves that timing;
5. a second source move is accepted and updates timing; and
6. the accepted history keeps the intended read set, including no direct
   `voice` `at` read.

The real native provider rejects the first `move-source` before the stale
request is submitted. The failure is
`candidate.timing: legacy word anchor is missing`. Therefore an earlier
refusal can establish neither captured-choice retention, landing status,
restart behavior, second-move behavior, nor recorded reads. Calling those
assertions proven from the refusal would violate D16.

The cause is bounded and source-backed: the seed has the parent legacy
declaration `"again" in line #2 +1f`, with no authored `clip.anchor` choice.
The reused `voice`/`other` clips share the same media and transcript but the
ordinary move changes the physical search basis. Provider `_hydrate` obtains
authenticated transcript captures from the dependency manifest or an explicit
anchor call; this legacy seed has neither at the move. The timing validator's
legacy path calls `legacy_binding`, which has no authenticated capture to
search after the basis changes and raises `legacy word anchor is missing`.
The reference-basis logic also deliberately includes the physical source
geometry and pinned documents, so a guard waiver would be incorrect.

## Existing production-path check

There is no exact authenticated production counterexample that provides this
same unbound-legacy sequence with all original assertions unchanged. The
nearby supported path is explicit `clip.anchor`: `native_word_anchor.binding`
validates the occurrence, stable word IDs, exact transcript pin and source
geometry, and `_hydrate` can load that pin from the accepted manifest or the
anchor call. The related first-use/restart and explicit-anchor controls prove
that authenticated path only; changing this test to use it would change the
case and would not answer D16.

## Approved delivery disposition

Classify this as one bounded known v2 limitation: the current native provider
cannot preserve an unbound legacy word choice through a source move/reorder
when no authenticated transcript capture/reference is present. Keep the
original test unchanged, unskipped, and visibly failing. Fund a source-side
authenticated exact-transcript carrier/reference path that preserves the
original physical owner and stable word choice, then rerun the unchanged
positive sequence. Do not fabricate a pin, waive the source/word/physical-owner
guard, rewrite the fixture, add a carrier/evaluator, or adopt the failed
`706fb017ecb662c2bb940467d39200445298de6f` status-only branch. No 52/54,
overall-suite, or V4-DONE claim follows.

## Evidence and verification limits

The independent source run already recorded the exact command:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ad823e0a PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-ad823e0a /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_native_word_anchor.py -k follow_rebases_original_choice_after_source_move_and_reorder
```

Result: `1 failed, 53 deselected in 1.91s`; only the `[True]` case was
collected/executed. The original file has 54 tests with one `[True]` retained
case for this function. This review did not rerun tests or collection, and no
scoped checks were applicable to the read-only prose/source verdict.

Worker folder:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-V4-D16-rebase-review-0641`

