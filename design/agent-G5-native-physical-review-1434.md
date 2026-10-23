# G5/R2 native physical review

## Verdict

**PASS — retained-input fidelity. PASS — causal ownership diagnosis.** This is
an independent diagnostic review of `f527261833dd1467a0180b9c179ad4029ca66a58`,
not product acceptance. G5 remains P1-gated and no whole-inverse pass is claimed.

## Evidence and fidelity

- The submitted SHA adds only
  `tests/sdk/fixtures/g5_inverse_retained.json` (377,565 bytes) and
  `tests/sdk/test_timeline_restructure_inverse_retained.py`.
- The fixture is lossless for the five requested immutable source events. Its
  `context`, `source`, `history`, `previous`, and `prepared` objects compare
  exactly with packet `runtime-G5-inverse-1358-01ccdec35f2a8f3e.json` events
  115, 117, 119, 129, and 158 respectively. No compact history, invented
  steps/ordinals, or projected fields were introduced.
- The orientation is settled by the retained source: event 117 is accepted
  split `authoring-parent-revision-caa332...`, with three occurrences and
  config digest `e6d3e227...`; event 129 is the previous flat
  `authoring-parent-revision-a58d...`, with one occurrence and config digest
  `32613189...`. The request base and `prepared.expected_head` are the split
  `caa332...`; `prepared.canonical_document` is the flat `a58d...` output.
- Existing Agent reconstruction produces the prepared native writes and steps
  exactly. The first three sequential before checks pass. The fourth write is
  `parent/occurrences`; the only difference between the physical observed rows
  and the native authored rows is the compiler-authored
  `shot_revision_id` pin on each row.
- The original inverse test body is unchanged from `91ac58a9` and retains body
  SHA-256 `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`.
  The two new tests are unskipped; the intended authentication-positive test
  remains a known RED result from the submitted evidence and was not replayed.

## Causal ownership

The current failure is Runtime-owned at the authenticated observation boundary,
with contract coordination required before any repair:

- Runtime `runtime_protocol/timeline_commit_auth.py:734-738`,
  `_inverse_stage_state`, returns the physical aggregate directly.
- Runtime `:970-972`, `_inverse_stage_boundaries`, compares that physical state
  directly to the native write's `before` value.
- Agent `astrid/sdk/timeline/_command_state.py:290-292` reads the authored
  placement list; `:369-379` requires occurrence-order writes to preserve every
  authored row; and `:282-286` rejects `revision_id`/`shot_revision_id` on an
  authored occurrence root.

Therefore the missing normalization is not an Agent source-orientation bug:
adding physical pins to the native recorder would violate the existing Agent
state/order contract. It is also not a source inconsistency: the full retained
request, accepted source, predecessor, history, prepared candidate, bindings,
effects, dependencies, undo metadata, and canonical output establish one
consistent split-to-flat orientation. Runtime must authenticate the physical
observation against the native/authored representation at this boundary, under
an explicitly coordinated contract. No speculative patch, pin lift, or native
coverage change is authorized by this review.

## Diagnostic controls

The scratch-only pin-lift control makes Runtime validation green, confirming the
causal distinction, but changes prepared bytes and is not provider, receipt, or
production proof. The 13 negative controls all refuse as intended:

`native-before`, `native-after`, `effect-before`, `effect-after`, `publication`,
`step`, `ordinal`, `digest`, `foreign`, `membership`, `order`,
`native-sequence`, and `ABA`.

These controls do not constitute a whole-inverse PASS. The failed authenticated
positive remains visible and G5 stays blocked pending a reviewed native/physical
observation contract and a new original-body qualification.
