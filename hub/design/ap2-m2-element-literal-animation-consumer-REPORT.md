# Literal animation consumer: blocked on published native SET capability

## Result

No App source was changed. The exact published tuple does not have a native
operation that can apply, update, or remove a literal animation while retaining
the current visual behavior. The existing App adapter writes the raw animation
fields, so routing this family through `clip.set-params`, an overlay row, or an
invented command would change semantics or violate the settled plan.

This is a genuine prerequisite blocker, not a consumer implementation hold.
The existing literal effect overlay consumer and existing-clip PARAM consumer
remain untouched, as do transitions, selected-pack elements, preview/render
paths, ordinary/media/duplicate ports, and the legacy animation route.

## Exact capability check

Checked the requested frozen/public sources:

- Agent `8130a401bf44a518d5a40ae274d398b8c560be55`
  (`origin` branch `candidate-sdk` / `hub/timeline/agent/tl/app-m3-agent8130-safety-source-keeper`).
- Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
  (`origin` branch `candidate-runtime` / `hub/timeline/runtime/tl/rt-m2-pin-2c4ac180`).
- Composition `@banodoco/timeline-composition` `0.0.13` at the current published
  package tree.

Agent's published `ClipSetArgs` is closed to `values.hold` and
`clear: [hold, asset, transition]`. It explicitly says transition authoring is
outside v1. Runtime's published schema fixture carries the same `clip.set`
union. `clip.set-element` only revises an already-existing element reference
with the same id, kind, and selected pack owner; it cannot attach a new
animation or clear one. `clip.set-params` writes the `params` object, which is
not the animation phase field.

The App's current legacy animation implementation is the semantic reference:

- `timeline.apply_element` with `placement: 'clip'` writes
  `elementRef` and, for animations, `entrance: { type: element.id, duration:
  0.4, params?: operation.params }`.
- `timeline.update_element` preserves the clip and merges `params`.
- `timeline.remove_element` removes `elementRef` and clears `entrance` only
  when it belongs to the removed animation.

Those raw fields are visible in `src/tools/video-editor/types/index.ts` as
`TimelineClip.elementRef`, `entrance`, and `exit`; the concrete behavior is in
`src/tools/video-editor/runtime/element-adapter.ts:284-343`.

## Required peer prerequisite

Agent + Runtime must extend the existing `clip.set` carrier, not add a new
wire DTO or operation, so that the current App element session can emit one
guarded intent per gesture:

```text
clip.set v1, select = parent/<or existing scoped owner>/clip:<stable-id>
  args.values: { elementRef: <exact literal ref>, entrance: <raw animation>,
                 [exit: <raw animation>] }
  args.clear: []
```

For update, the same existing `clip.set.args.values` carrier must support
replacing the raw `entrance`/`exit` value and, if the operation changes the
element identity, the same `elementRef` field in the same guarded command.
For remove, the existing `clip.set.args.clear` carrier must support clearing
`elementRef` plus the matching animation phase field(s), preserving an
unrelated phase (for example, removing an entrance animation must not clear an
independent exit animation). The accepted command must record the original raw
before values, declared intent, stable target, all relevant reads, and exact
after values so inverse/retry/undo can be qualified through the existing App
session/outbox.

The native acceptance contract must also define whether a literal animation
reference is stored in `elementRef` only, in the phase field only, or both. The
current App behavior uses both; the prerequisite must preserve that exact
representation and validate animation kind/id/revision and phase semantics.
No App-side cast, fabricated `clip.add`, `clip.set-params` workaround, or
late whole-document save is safe before this carrier exists.

## Evidence

Read-only source checks:

```text
git show 8130a401...:astrid/core/timeline/schema/edit-command.schema.json
  -> ClipSetArgs values only hold; clear only hold/asset/transition
git show 2c4ac180...:tests/fixtures/published-command-schemas/agent-0a0ac7ba.json
  -> Runtime-published clip.set / clip.set-element / clip.set-params union
git show HEAD:package.json (Composition)
  -> @banodoco/timeline-composition 0.0.13
```

Targeted App baseline (no source changes):

```text
npx vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/components/ElementsLibraryPanel.test.tsx \
  src/tools/video-editor/runtime/element-adapter.test.ts \
  src/tools/video-editor/commands/elementCapture.test.ts \
  src/tools/video-editor/commands/elementOverlayCapture.test.ts \
  src/tools/video-editor/commands/elementGesture.test.ts
```

Result: 4 discovered test files, 26 tests passed. The named
`elementGesture.test.ts` path is absent in this tree; Vitest completed the four
existing files. No full, browser, localhost, socket, dependency, public-pin,
or native-environment run was made.

## Handoff status

No source diff, no deletion, and no ledger closure. Resume this App row only
after Agent/Runtime publish and qualify the existing `clip.set` carrier for the
raw animation fields above; then wire `ElementsLibraryPanel` through the
existing element port/session/outbox and add direct apply/update/remove,
zero-legacy, retry, undo, and current-native-record evidence.
