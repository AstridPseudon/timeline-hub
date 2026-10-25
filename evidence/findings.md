# D136a/D100 independent actual-result/custody review

## Verdict: FAIL allfindingsonce / NO_GO

The exact original9 ran once after admitted free space of 5,316,198,400 bytes.
The private JUnit node counts are 9 tests, 9 setup errors, 0 failures, 0
passes, and 0 skips; exit code 1. The XML case names equal the nine exact
selectors in the supplied predicate map. Every case has the same first seam:
`provider intermediate command lacks an authenticated physical observation`.

This is a product guard refusal, not a classifier or safety refusal. The
immutable Runtime pin's guard is proven at
`runtime_protocol/timeline_commit_auth.py:2209`, in `command_output`, while
projecting an intermediate command observation. The production path remains
the registered Runtime commit service: `publish_authoring_candidate` calls the
writer at `astrid/core/timeline/authoring_bundle.py:1884`; the original9
authoring writer enters `service.commit_timeline` at
`tests/sdk/test_timeline_capture_projection.py:270-276`; Runtime's public entry is
`runtime_protocol/service.py:2469-2483`.

The specific missing record/ref/ordinal is not present in safe evidence. It
would require exporting protected request, payload, key, URL, or raw stack
material. Therefore the causal owner is **UNKNOWN**. The proven finite record
is nine intermediate-observation guard refusals, one per selector. No shared
cause is inferred from the D100 comparator.

## Custody and conservation

The received source is exactly the two-path candidate delta over receiver
base, with the unchanged timing evaluator retained. D100 product, boundary
test, and projection hashes match the held manifest; projection census remains
43 predicates, 11 test bodies, and 54 fixture statements. Independent AST
comparison found 19/19 non-FPS validation functions unchanged and 7/7 prior
D136 test functions unchanged; three D136 test functions are additive.

Prior source reviews remain bounded PASS evidence only: D136a review 2119 is
`PASS_BOUNDED_SOURCE_SECURITY`; D100 security review 1803 is
`PASS_SOURCE_SECURITY` with behavior not run under its disk gate. The supplied
focused source checks remain 57 passed, Ruff/mypy/compile/diff PASS. None of
these overrides the actual original9 result.

No source release, normal merge, qualification, retry, fixture/input/test
edit, guard edit, authentication widening, or product-author attribution is
made.
