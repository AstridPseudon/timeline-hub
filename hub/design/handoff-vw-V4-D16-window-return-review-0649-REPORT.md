# V4 D16 first-return independent review

## Verdict

**Semantic/no-weakening scope: PASS. Behavior verification: PENDING. No merge approval.**

Reviewed `15d82aa877ab17a212cb94f8bf4335a322c87e57` against
`3e4261e9694c7bd7c1b5fada9bf01d91007bcc80`. The diff changes only
`tests/editing_conformance/test_native_word_anchor.py` and only the named
stale-window test.

The returned adaptation follows the settled D16 exception:

- `pick(case, 1)` is called against the original real bundle and is not
  submitted. The base is captured immediately afterward from the original
  head.
- The original legacy seed remains in `parent/clips/id:card/app/astrid/on`,
  with the fixture's real declaration and no `word_anchors` namespace.
- The captured request retains the original base revision/publication pair,
  real source token, transcript pin, and stable word ID. No authored anchor is
  created or used as a replacement baseline.
- The window edit is submitted at that original base and is expected to be
  the first rejected operation under D16. The stale anchor request is retained
  for audit only and is correctly not submitted, because a rejected window edit
  cannot create an intervening head.
- The test preserves the original message match, `invalid_anchor` reason,
  original-base `invalid` classification, and no-write/head checks, adding the
  required legacy path `parent/clips/id:card/app/astrid/on`. The full bundle
  equality also preserves the captured source mapping and word data.

No hardcoded authored anchor or fixture rewrite substitutes for the legacy
declaration. The expected source and word facts are checked from the command
produced by `pick` and the real captured transcript/document data; the test
does not persist `word_anchors`.

## Source-trace limitation

The prior report's `native_word_anchor.py:378-381` trace is valid for the
rejected bound-anchor (`word_anchors`) scenario, but it does not establish the
legacy error origin in this returned test. With the unbound legacy seed:

1. `compile_recorded` returns early at `native_word_anchor.py:366-367` when
   there are no `word_anchors` and no legacy beats.
2. Final validation computes legacy reference-basis equality in
   `_commit_timing_validation.py:244-264`; the real source-window change is
   included in the word-reference basis (`:84-100`), so the changed window
   cannot receive the unchanged-unresolvable legacy exemption.
3. Validation then calls `legacy_binding` at
   `_commit_timing_validation.py:375-379`. With `from=4`/`to=6`, the real
   captured words selected by the original declaration are outside the source
   window, so the current implementation raises `TimingCompileError("legacy
   word anchor is missing")` rather than the required structured
   `invalid_anchor`/half-open-window error.
4. `validation.py:605-611` wraps that as a final-candidate error, and
   `commit.py:1158-1160` classifies it as `invalid_document` without a path;
   the serialized path is therefore currently `[]`.

The normative D16 expectation in the adaptation—`invalid_anchor`, the existing
half-open-window message, and path
`parent/clips/id:card/app/astrid/on`—therefore remains behavior-pending on the
provider/source correction. The empty path and the bound-anchor trace were not
waived or treated as passing evidence.

## Checks

- `ruff check --no-cache tests/editing_conformance/test_native_word_anchor.py`
  — **PASS**.
- `git diff --check 3e4261e9694c7bd7c1b5fada9bf01d91007bcc80..15d82aa877ab17a212cb94f8bf4335a322c87e57`
  — **PASS**.
- Typecheck — **N/A**, test-only adaptation.
- The known behavior test was **not rerun**, as required; no full, browser,
  native14, heavy, or broad suite was run. The prior known failure is not
  repeated as evidence for this returned body.

## Delivery / handoff

The intended delivery behavior is that a source-window edit which would orphan
the existing legacy declaration is refused at edit time with no head write.
The adaptation is semantically complete but remains unqualified and should
remain unmerged under H9. No additional worker or repair is recommended in
this review; the original suite remains AS IS for the farm final. If this is
reopened later, the provider owner must supply the legacy structured error and
one fresh targeted behavior check before any merge decision.

