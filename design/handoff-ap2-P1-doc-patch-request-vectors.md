# Handoff: AP2 P1 doc.patch request vectors

Status: early real-corpus collection only. No H3 GO, merge/inverse proof, or
Runtime service credit is claimed.

## Artifacts

- `tests/sdk/fixtures/p1_feasibility/doc_patch_requests.json`: eight small,
  data-driven request operand vectors with source SHA-256, source test node,
  exact closure root, tagged guards, created IDs, expected authored deltas,
  expected conflict fields, and explicit unexecuted provider cases.
- `tests/sdk/test_p1_doc_patch_requests.py`: fixture-only validation. It checks
  source/copy provenance, contract operation shape, id-addressed paths, exact
  `before` tags, opaque values, list order guards, and expected authored deltas.
  It never applies a patch.

## Source and decisions

Current source is Agent `tl/integration` at `3f1ceaed`, which contains the
integrated collection commit `250db8c8`. The governing contract is Timeline
commit v2 (C0 + C0b + adopted C0c addressing principle). Trim and list vectors
address `parent` because that is where the real authored collection and fields
live. The source internal child is compiled output, not an invented patch root.
Scalar vectors use the existing source-record address `occurrence:o/clip:c`.
No publication IDs, idempotency keys, provider result, or guessed Runtime API
fields were added because the real fixtures do not contain them.

## Follow-up when R1 is available

Use the existing Runtime entry point
`astrid.sdk.timeline.commit.RuntimeCommitService.commit(context, port)` via the
`commitTimeline` route (`/v1/projects/{project}/timelines/{timeline}/commit`),
with a live `base_publication_id` and idempotency key. The current branch has no
registered `doc.patch` operation, so execution is intentionally deferred to the
R1 provider. Run the focused vector test together with `tests/sdk/test_p1_case_corpus.py`
after the provider accepts the command; then add the real reply/receipt evidence
in the P1 integration lane rather than changing this collection into an executor.

## Verification

The focused new test passes: 7 tests. The required combined command passes with
20 tests; Ruff and mypy are clean, and `git diff --check` has no output. Pytest
reports one pre-existing environment warning because the configured `timeout`
option is unknown. No full, browser, socket, or provider suite was run.
