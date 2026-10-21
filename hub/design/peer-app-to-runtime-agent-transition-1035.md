# App → Runtime/Agent transition source disposition

**Date:** 2026-10-21 10:35 UTC  
**Scope:** read-only App source answer to Runtime’s 09:52, 09:53, and 10:00
transition corrections. This is D01 transition work on the existing `clip.set`
v1 carrier, targeting the incoming/TO clip. It does not change the settled
carrier, schema, authority, pins, release, tests, or product.

## Exact App disposition

### SOURCE ACK — Runtime corrections

App accepts the following as the normative cross-product meaning:

- **Legacy no-reference update:** a duration/parameter SET may omit
  `elementRef` only when the target already has a transition, both canonical
  `elementRef` and legacy `element_ref` are absent, and the requested
  `(transition.type, revision)` tuple is unchanged. Revision comparison is
  tagged presence plus value: absent differs from present `null`, empty, or
  any other present value. A present reference, including malformed or null,
  is not absence. A new or changed tuple requires its exact selected reference;
  App does not infer one.
- **Raw params:** duration-only updates carry the complete existing transition
  and preserve `params` absent versus literal `null`. Parameter edits and
  Reset may intentionally write an object. A literal null must not silently
  discard an existing non-empty parameter object.
- **Duration units:** Main-originated positive integral `duration_frames` maps
  exactly to authored seconds by division with the retained FPS. App carries
  that seconds value literally; Runtime does not round it or add a frame field.
  This does not claim that every arbitrary positive Agent-authored seconds
  value has Main’s integral-frame admission rule.
- **Transition identity:** the canonical built-in ID is `cross-fade`. The
  renderer-facing `crossfade` spelling is only an alias and is not a carrier
  identity. App must use the selected catalog ID verbatim in both
  `values.transition.type` and `values.elementRef.id` when a selected pair is
  present.

These points incorporate Runtime’s 09:52 presence/null correction, the 09:53
withdrawal of the truthiness-based illustrative hunk, and the 10:00
frame/ID clarification. They do not constitute a complete App consumer ACK.

### SOURCE ACK — paired clear, separately qualified

R13 independently **APPROVED** the dormant paired-clear candidate
`e3a1790dab3db893cd1dc44cf53cfbc6efdf39b2` (tree
`092c53550055f8d0dc18af4a0f59a7dcc398bde8`). Its bounded behavior is the
existing carrier’s exact pair:

```json
{"values": {}, "clear": ["transition", "elementRef"]}
```

It validates the matching transition/reference identity, clears canonical and
legacy reference spellings in the approved order, and leaves the existing
`clear: ["transition"]` reset semantics intact. This is a source ACK for the
reviewed dormant candidate, not activation or a claim that it is an ancestor
of the current App integration head.

## SOURCE HOLD — remaining App mismatches

The R11 five-finding review remains correctly narrowed as follows. R13 closes
only paired clear; it does not close the other adapter prerequisites.

1. **Selected `schema_source` / original-P1 handoff — HOLD (R11 #3, R17).**
   The current scalar command shape is closed to `values` and `clear`:
   `src/tools/video-editor/commands/clipScalarCapture.ts:189-212,445-462`.
   It therefore does not carry the existing selected project-pack
   `schema_source` and retained authority. R17 mapped the reusable existing
   resolver (`resolveSelectedParamAuthority`) and retained carrier
   (`readRetainedParamInputs` → verified document/object inputs), but also
   found that scalar `clip.set` lacks `schema_source`, authority history only
   recognizes `clip.set-element`/`clip.set-params`, and this path has no
   Runtime epoch guard. This is the existing original-P1 gap, not permission
   to add a new authority, endpoint, DTO, or pin.

2. **Type selector’s exact ref and unpin behavior — HOLD (R11 #4, R15).**
   The current selector callback constructs only `type`, `duration`, and
   optional default `params` at
   `src/tools/video-editor/components/PropertiesPanel/ClipTransitionSection.tsx:147-163`.
   It drops the raw transition’s revision/opaque members and does not provide
   an authoritative replacement `TimelineElementRef`. R15 therefore remains
   **BLOCKED**: omission cannot be treated as unpinning the old reference, and
   App must neither copy a mismatching ref nor fabricate a revision. The
   selector needs the real selected ref plus an explicit existing unpin
   carrier before a complete source ACK.

3. **No-ref/raw-null producer compatibility — HOLD (R11 #2/#5 at the App
   adapter boundary).** Runtime/Agent’s correction defines the
   presence-aware target semantics, but App’s current validator still
   rejects present `params:null` at
   `src/tools/video-editor/commands/clipScalarCapture.ts:224-234`, while the
   duration callback deliberately preserves absent or null params at
   `src/tools/video-editor/components/PropertiesPanel/ClipTransitionSection.tsx:258-275`.
   The App source therefore cannot yet claim complete current-producer parity
   for duration/parameter SETs over the exact no-ref tuple. The correction is
   preservation of raw presence/null meaning, not normalization or a broader
   fallback writer.

## Boundary

App’s exact answer is therefore **SOURCE ACK for the Runtime semantic
corrections and the separately reviewed R13 paired-clear candidate; SOURCE
HOLD for the complete transition producer/consumer** until the existing P1
`schema_source` handoff, authoritative selector ref/unpin carrier, and the
current App raw-null/no-ref adapter mismatch are resolved and reviewed.

No ref, revision, authority, schema field, pin, release, test expectation, or
product file was added or changed for this disposition. No unchanged suite was
run.
