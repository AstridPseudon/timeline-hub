# App/Agent opacity source semantic review

## Verdict

**ACK for the Agent source proposal; App native activation is not yet qualified.**

Reviewed Agent commit `70652d26567797f1df5b14e3f2480249aef743e7`, tree
`63229ef26d7b44faf765f074ff2029a1598a8d79`, and schema SHA-256
`110165ab9f7e4be3e9766d06b5ceacab8c5e8c7cc12e7180929005b67bcc82d6`.

## Contract findings

- Main `ClipPanelBody` reads `clip.opacity ?? 1`, constrains the slider to
  `0..1`, and emits the raw fractional number (`ClipPanelBody.tsx:437-443`).
- Agent adds only `values.opacity` to existing `clip.set@1`; it is top-level
  `clip.opacity`, not `params.opacity`. The schema is a JSON `number` with
  inclusive `minimum: 0`/`maximum: 1`; command finite-JSON validation rejects
  bool, null, string, NaN, and infinity before schema validation. Unknown
  fields and `params.opacity` are refused.
- `clear: ["opacity"]` removes only the leaf. The focused Agent conformance
  records exact ABSENT/present-null/present-zero/present-value before-state,
  exact inverse/redo, strict A->B->A refusal, occurrence isolation, and
  disjoint `params` rebase. Existing `_target`/`_clip_basis` owner/media reads,
  source-bound v2 capture, reads, and identity guards remain on the generic
  path.
- Inventory reconstruction is exact and test-only: removing opacity yields
  frozen project-data `392`; removing the project-data addition as well yields
  frozen private carrier `613`; the existing carrier projection then yields
  ordinary `6ba`. No frozen ref, fixture, or artifact was modified.

## App mismatch and minimal recipe

Current App `clipScalarGesture.ts`, `clipScalarCapture.ts`, and
`ordinaryScalarMember.ts` still whitelist only `hold|asset|transition`; the
current `commitSession` scalar gate also requires returned command version
`"1"`. Therefore the existing App consumer cannot submit opacity or preserve
the Agent source-bound v2 command as-is. This is a downstream activation gap,
not an Agent source-contract mismatch.

Minimal consumer recipe: widen the existing scalar args/preview to admit only
raw numeric opacity and an `opacity` clear, then have the existing session
capture/finish port call Agent `capture_clip_set` on the captured raw bundle and
forward its complete returned command unchanged (including version, expect,
reads, authorship, selections, bindings, and v2/source proof). Emit exactly
`{values:{opacity:x},clear:[]}` or `{values:{},clear:["opacity"]}`; never map
to `params.opacity`, percent values, null clears, or a snapshot/legacy writer.
Keep the current leaf-only preview and outbox/commit path.

## Tests

Passed, existing focused App tests only:

```text
node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --no-file-parallelism \
  src/tools/video-editor/commands/clipScalarCapture.test.ts \
  src/tools/video-editor/commands/clipScalarGesture.test.ts \
  src/tools/video-editor/commands/ordinaryScalarMember.test.ts \
  src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx \
  src/tools/video-editor/lib/clip-scalar-preview.test.ts
5 files, 71 tests passed
```

The requested `--configLoader=runner` variant was not usable because this
repo's config references CommonJS `__dirname`; the normal loader with
`--no-cache` passed. No Agent suite, full suite, browser, socket, generation,
pin, dependency, release, activation, or writer deletion was run.

Worktree remained clean; no product code changed.
