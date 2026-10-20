# Runtime current carrier peer handoff

Date: 2026-10-20 UTC

## Status

**Private source review approved; final counterpart review and native adoption
remain held.** This handoff is for one Agent counterpart review and one
coordinated native pair. It is not approval to pin, freeze, publish, release,
activate, merge into `tl/integration`, or claim native qualification.

## Exact reviewed tuple

- Runtime private carrier commit: `7b8d6d9afe963e2b7a6c6b32fd4e3797451090da`
- Runtime private carrier tree: `d20b745c26a33c2ea4e20863f846335c8cf33e1e`
- Current Runtime source image retained by the fence review:
  `81f8c7e0b22c34804015c054762af3d737e4698a`
- Exact Agent counterpart: commit
  `3730d0bd51686a1692450359482205df64dcc839`, tree
  `3892a10bcffa9bf520b4c79591637cf3259d6724`
- Matched private Agent command schema SHA-256:
  `f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`
  (48 definitions, 22 operation clauses, 13 source-bound v2 operations).
- Public Agent floor remains immutable at SHA-256
  `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`.

The carrier is private-only. The ordinary 55-definition/29-operation source
and the broader 310/55/29 source were not imported.

## Reviewed boundary and delta

The final fence review records that the current composition has the exact
documented 16-path allowlist and that all **415 tracked paths outside that
allowlist match** the `81f8c7e` current source image. Existing provenance,
owner/item, `_same_materialization_slot`, global raw-item reservation,
canonical `item_id`, accepted-ledger-first retry, and C4 historical reuse
checks remain intact.

The material safety delta is the actual v2 catalog-head fence:

- the current, inverse-source, and accepted-historical-slot authorization
  paths require the project-scoped `shot_revision_heads.revision_id` to equal
  the authenticated accepted image revision;
- the Runtime store contains the new **19-line guard** in
  `runtime_protocol/timeline_commit_store.py`;
- `tests/test_timeline_projection_ownership.py` contains the new **55-line
  regression** `test_source_bound_owned_slot_cannot_overwrite_newer_catalog_head`,
  covering exact accepted retry, current overwrite refusal, and historical
  reuse refusal after a newer catalog head.

The original typed/public-floor controls and legacy-v1 behavior are preserved:
the public floor is unchanged, no xfail/skip/weakened expectation/DTO/endpoint
was added, and accepted v1 ledger-first retry plus undo/redo/restore behavior
remain part of the reviewed source.

## Current integration delta that must survive

Current Runtime integration is:

- commit `a51af885ea631c695a857985239c7fe7bf2e871f`
- tree `7c6ab6700307309a7942e64eb4d0c6c7cc42b681`

It includes the selected-media CAS fix from commit
`3021a5b79102e9c0873f70df46f5a686bd1276ff`, tree
`521fb1dc9aa9e4094e0f901aa3961a1f9db0d471`. That fix adds the existing
`MediaReads`/`RequestCommitPort` exact selected-object CAS-byte verification
helper and its native clip-replacement controls. The accepted-ledger-first
retry path remains unchanged. The current-base successor must preserve this
CAS port helper and its tests; do not replace `timeline_commit_port.py` with
the older carrier-side copy.

Reviewed catalog-text replay commit `63e761e29e7e51fc5fa71cc01cd1fe0cf595212f`
is **not currently an ancestor** of `a51af88`. If it is merged before the
successor is composed, preserve its text replay behavior and re-review the
resulting current base. Do not claim that text change is already present.

## Pending merge conditions

1. Compose the private carrier onto one current Runtime-base successor,
   including `a51af88`/`7c6ab670` and the CAS helper. Preserve the catalog-head
   fence, the 19-line guard, the 55-line regression, the existing typed/public
   floor and legacy-v1 controls, and any reviewed `63e761e` text change only if
   it is actually merged into that base.
2. Agent independently reviews the exact committed successor and its tree
   against Agent `3730`/tree `3892`, with the private schema digest above.
   Review must specifically cover the new guard/regression and the preserved
   CAS path. A moving worktree or an asserted pre-commit SHA is not evidence.
3. After that review, coordinate **one** named native `3730` pair covering
   ledger-first accepted-v1 retry, undo/redo, lost-ACK/restart behavior,
   own-slot occupancy, global-item occupancy, and draft preservation. Runtime
   must not duplicate the comprehensive/native execution in this handoff.
4. Keep public pin/freeze/release/adoption and artifact authority held until
   the counterpart review and that single coordinated pair both complete.

## Evidence boundary

This worker performed source/ref/status inspection only and ran no tests. The
`1 passed` current-GREEN native-provider fence result, the prior bounded
195/209 lanes, and CAS-focused results are inherited evidence recorded in the
referenced review documents, not reruns by this worker. No full, matrix,
browser, live-socket, or duplicate native suite is claimed.

References:

- `runtime-carrier-current-fence-final-review.md`
- `agent-review-runtime-carrier-83fe.md`
- `runtime-carrier-current-tree-candidate.md`
- `runtime-media-cas-final-review.md`
- `runtime-selected-media-cas-integrity.md`
