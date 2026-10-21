# App2 transition SET source ACK/HOLD

Date: 2026-10-21 UTC  
Scope: App2 source only; no implementation, schema, pin, artifact, publication,
activation, or consumer-proof claim.

## Verdict

**SOURCE HOLD for the proposal as a whole, with a bounded SOURCE ACK for the
built-in dormant `clip.set` capture carrier.**

The existing dormant scalar capture matches the proposed incoming TO shape and
the settled Main adjacency/fit boundary for built-in transitions. It does not
currently carry `schema_source` on `clip.set`, does not resolve the selected
project-pack P1 authority for that operation, and does not accept the proposed
paired `clear: ["transition", "elementRef"]`. Those are concrete source
incompatibilities for project-pack SET and associated removal. Built-ins must
remain pinless; this source does not manufacture a project pin.

## Exact identities

- Proposal:
  `runtime-transition-set-owner-proposal-20261021T0920.md`
  SHA-256 `a5dd58763f838e30403c016894c8ec9b84af8bb2c1803e5d97fbf5fb3428cb24`.
- Unapplied schema diff:
  `runtime-transition-set-schema-diff-UNAPPLIED.patch`
  SHA-256 `30a07c13f250a66fbff75058205d03eebbfd83921604a96479a8abb6af3a7e1e`.
- Reviewed App2 HEAD/tree: `4db86a76acd505dd1c7dc798695e2b7a9c932170` /
  `461fa0cddd67f4eb574563b38407733bd50afa7c`.
- Proposal’s frozen Main witness: commit
  `860d43b331fb4422b16bc0dbd7b08666a0c766a0`, tree
  `ea4eabb8eb469df63fd1d515f84982d85b2f14cc`.
- Candidate `public018` was not allocated, generated, adopted, or published.
  `public014` RESET and immutable `private017` remain distinct and untouched.

## SOURCE ACK — bounded built-in carrier

The dormant App2 path is structurally able to represent the built-in SET
example as one existing `clip.set` command:

- `src/tools/video-editor/commands/clipScalarCapture.ts:189-235` admits only
  `hold`, `transition`, and `elementRef` values; transition validation keeps
  authored `duration` in seconds, requires a non-empty type and positive finite
  duration, preserves JSON-valued `params` and opaque top-level keys, and
  refuses compiled-only `id`, `durationFrames`, `align`, and `incomingPolicy`.
- `:243-287` records the same-track predecessor selection and reads both
  predecessor and destination. It enforces the existing Main boundary:
  `abs(from.end - to.start) < 0.001` and frame-window fit with Main’s
  `+0.0001` tolerance. `:351-390` writes the transition and optional matching
  `elementRef` atomically to the selected destination row, including stable
  `parent/clip:<id>` and `occurrence:<id>/clip:<id>` targets.
- `src/tools/video-editor/commands/clipScalarCapture.ts:444-462` is the
  existing capture carrier. `src/tools/video-editor/commands/clipScalarGesture.ts:33-50`
  requires the finished result to remain exactly one `clip.set` with the
  captured selector and args. `src/tools/video-editor/commands/commitSession.ts:758-783`
  places it on the existing scalar session/outbox path.
- The dormant parity fixture at
  `src/tools/video-editor/commands/clipScalarCapture.test.ts:58-86` captures
  incoming TO ownership, paired transition reference, opaque nested data, and
  predecessor selection. This is source evidence only; no test suite was run
  for this review.

The Main producer field mapping is exact at the frozen witness’s
`src/tools/video-editor/runtime/element-adapter.ts:175-189, 355-377`:
`from_clip` resolves the predecessor, `to_clip` is the destination, the
stored transition type is `transition.id`, stored duration is
`duration_frames / fps` (authored seconds), revision is retained, params are
copied, and `elementRef` is written on the TO row. The update path at
`:379-416` spreads the existing raw transition, so a native caller must pass
the complete raw envelope when changing a field. Main’s old remove path at
`:418-423` removes both fields; that is not an approval of the native paired
clear semantics.

The current ordinary RESET path remains distinct: 
`src/tools/video-editor/components/PropertiesPanel/ClipTransitionSection.tsx:111-120`
submits `{ values: {}, clear: ["transition"] }`, and
`src/tools/video-editor/components/PropertiesPanel/BulkClipPanelBody.tsx:207-217`
uses the same scalar batch carrier. This preserves explicit transition-only
clear behavior; it must not be widened by this ACK.

## SOURCE HOLD — exact incompatibilities

### 1. `schema_source` is not carried by transition `clip.set`

The existing selected-declaration carriers put `schema_source` inside
`args`, not beside `args`:

- `src/tools/video-editor/commands/clipParamsCapture.ts:7-25` emits
  `clip.set-params` with `args.schema_source`.
- `src/tools/video-editor/commands/elementCapture.ts:103-158` emits
  `clip.set-element` with `args.schema_source`.
- `src/integrations/runtime/timeline-commit-types.ts:28, 112-113` types
  `schema_source` for those two operations only. Its current `ClipSetArgs` at
  `:116-127` still permits only hold values and the existing clear set.

By contrast, `clipScalarCapture.ts:189-212` requires `command.args` to have
exactly `values` and `clear`; `ClipScalarArgs` at
`src/tools/video-editor/commands/clipScalarGesture.ts:7-15` has no
`schema_source`; and the current scalar capture never calls the selected
authority resolver. Therefore a project-pack transition cannot map to the
proposal’s `clip.set` shape with an exact admitted `DocumentPin` in this
App2 source. Adding or manufacturing a pin, alias, operation, DTO, endpoint,
store, or second authority is out of scope and was not done.

### 2. Existing selected-pin authority does not cover transition `clip.set`

`src/tools/video-editor/commands/selectedParamAuthority.ts:151-201` accepts
only accepted records whose operation is `clip.set-element` or
`clip.set-params`; it validates `args.schema_source`, the exact selected
element, the retained snapshot, and fixed bindings. Its history walk at
`:317-364` likewise recognizes only those operations. The mounted selected
PARAM session in `src/tools/video-editor/commands/commitSession.ts:785-849`
prefetches and checks the pin for that separate carrier.

There is no corresponding transition `clip.set` authority path. Consequently
this source cannot ACK the proposal’s rule that ordinary same-reference
transition SET retains original P1 after P2, while genuine reselection is the
only way to establish a new pin. The existing selected PARAM authority is not
silently reused or inferred for transition SET.

### 3. Paired transition/reference clear is not an App2 scalar shape

`clipScalarCapture.ts:202-212` currently allows `clear` values only from
`hold`, `asset`, and `transition`; `clipScalarGesture.ts:8` has the same type
floor. Thus the proposal’s explicit associated removal
`clear: ["transition", "elementRef"]` is not currently representable by the
dormant App2 scalar carrier. The existing `clear: ["transition"]` RESET must
remain the original path and must continue preserving unrelated references.
This is a HOLD on associated removal, not a reason to alter RESET.

## Active producer boundary (not proof of adoption)

The current transition UI is still outside the dormant native carrier:

- `ClipTransitionSection.tsx:147-162, 267-275, 300-334` and
  `BulkClipPanelBody.tsx:557-573, 661-665` send transition SET/update data to
  legacy `onChange` callbacks. They spread existing transition data locally,
  but do not emit the dormant `clip.set` capture command.
- `ElementsLibraryPanel.tsx:128-142` sends transition application to the
  existing `timeline.apply_transition` adapter. The adapter’s current source
  implementation at `element-adapter.ts:355-377` is the exact Main mapping
  above, but it is a direct producer path rather than a native scalar
  session/outbox consumer.

Accordingly this report makes no ACK of publication, activation, all-Main
coverage, native consumer proof, browser/build/service behavior, or removal of
the legacy writer. HOME’s live transition row and RESET work were not edited
or duplicated.

## Evidence and commands

Read-only source inspection was performed from the clean App2 HEAD above. The
following checks passed:

```text
sha256sum <proposal> <unapplied-schema-diff>
git rev-parse HEAD HEAD^{tree}
git diff --check
git status --short --branch
```

`git diff --check` passed and the worktree remained clean. No tests were run:
this was a source/proposal-only review with no source changes, and the brief
explicitly excluded browser/build/daemon/socket/service execution and broad
old transition suites.

## Next step

Keep this App2 result **SOURCE HOLD** for project-pack transition SET and
paired removal. A later bounded consumer task may use the already-existing
scalar session only after the matched Agent/Runtime carrier is present and the
App path has an explicit retained-P1 handoff plus the proposal’s paired-clear
semantics. Built-ins remain the only bounded ACKed source case here.
