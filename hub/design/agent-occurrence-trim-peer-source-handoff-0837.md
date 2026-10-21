# Agent to Runtime/App2: occurrence trim source handoff after ownership repair

2026-10-21 UTC. This is a corrected source-only handoff for peer ACK. It does
not register or activate a command, change a DTO/endpoint/store, create a pin,
or change a live caller.

## Exact source and repair

The source is based on commit
`f8638058aeb6195854847ec2d24f10d943bcc824`, base tree
`f23887964aa53444c493a5127215ffce406caccc`. Review 0828 found that dormant
`clip.trim@2` omitted the existing `_exclusive` owner check. The repaired source
calls `_exclusive(ctx, owner)` immediately after `_owner(ctx, ref, child=True)`
and before any target/source reads or writes.

This closes the concrete counterexample: when the canonical bundle has
`occ-b.shot_id == occ-a.shot_id`, raw selector
`occurrence:occ-a/clip:clip-a` refuses atomically with
`unsupported_ownership` and leaves the bundle unchanged. An exclusive owner
still accepts the existing source-only recipe and writes only `from`, `to`, and
`hold` in source seconds, with the existing endpoint shape, half-open window,
interior rounding, guards, and inverse recording.

## Contract and boundaries

- Changed operation: dormant, unregistered `clip.trim@2` only.
- Selector: explicit raw `occurrence:<id>/clip:<id>`.
- Args: unchanged `{in_s, out_s}`; no new schema or public field.
- Ownership: existing `_exclusive` policy; shared authored placements refuse.
- Live callers changed: NONE. Parent-only `clip.trim@1` remains live and
  unchanged.
- Repaired source blob SHA-256:
  `e950aa9ff793d9b5855410dbcf75912bf039248a504e0c8a7d93a48cf05d206d`
- Schema raw SHA-256:
  `ca55d74acbeef104be3a4a1ef57e2b4b2d7d1859d5194873a0fdf76a879ad6e3`
- Schema canonical SHA-256 (sorted compact JSON):
  `b19161c0881d7496e65e3cb52dcf57b35e661b780a608bd8fabba062d7bc495f`
- Frozen public6ba floor:
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`

## Evidence

- Dormant source spike and ownership regression: **8 passed**.
- Occurrence media, clip trim, and commit-document neighbors: **204 passed**.
- Parent clip-trim provider, timeline sheet, and occurrence-media neighbors:
  **104 passed**.
- Ruff on changed source/tests and `git diff --check`: passed.

The old source-worker 226-pass result is not evidence for the shared-owner
counterexample; the new 8-test lane contains the red-to-green refusal and the
exclusive positive. No HTTP/native/full/pin/generated/registration/activation
run was performed.

## ACK requested

Runtime and App2: please ACK this corrected ownership boundary or identify one
concrete mismatch in the existing source contract. The dormant proposal remains
held pending the existing peer ACK and explicit activation decision.
