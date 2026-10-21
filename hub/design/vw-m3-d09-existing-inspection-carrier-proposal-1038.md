# VW-D09b/c — unapplied existing-resource inspection carrier proposal

Status: **source agreement proposal only; not approved, allocated, implemented,
serialized, packaged, or activated.** Reciprocal ACK from the Composition and
Agent owners is required before any source or test change.

## Finding

The existing generic diagnostic transport is:

```text
Agent prepareSceneCapability.frame()
  -> ComponentFrameSupport.diagnostics
  -> Composition querySceneFrame()
  -> SceneLayer.diagnostics
  -> existing scene-query JSON frame answer
```

Exact current seams:

- Composition `typescript/src/scene-capabilities.ts:12-28` defines the
  component-owned diagnostic resource and its `ComponentFrameSupport` carrier.
- Composition `typescript/src/scene-evaluation.ts:166-193` sanitizes that
  resource; `:314-322` places it on the queried `SceneLayer`.
- Agent `astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/scene.ts:12-31`
  is the registered caller. Its existing `motion.ts:44-61`
  `mouthInspectionRect()` helper is the correct compatibility seam.
- Agent `remotion/scene-query.mjs:6-10,36` already queries and returns the
  public resource; no endpoint, DTO, store, authority, or explicit
  serialization path is missing.

There is no existing slot for the separate derived inspection footprint.
`diagnostics.mouth` cannot carry it: it is the semantic capability region and
must retain its current UNKNOWN rules. The smallest carrier is therefore one
optional derived-only field on the existing `ComponentDiagnostics` resource.

## One proposed field

Add exactly this field to `ComponentDiagnostics` in
`typescript/src/scene-capabilities.ts`:

```ts
  /**
   * Derived compatibility inspection footprint only; never semantic mouth
   * capability, visibility, occlusion, authority, or pixel evidence.
   * null means the component's raw compatibility helper refused the input.
   */
  inspectionMouth?: ModifierBounds | null;
```

`ModifierBounds` is the existing `{status: 'known'; rect: RenderBounds} |
{status: 'unknown'; reason: string}` type. The field is optional so old
components remain valid; `null` is the explicit no-footprint result for absent
or raw-invalid compatibility input. It is derived at the current content
frame and is not authored timeline data.

## Bounded hunk packet (illustrative, unapplied)

These are exact source hunks for owner review, not a patch to apply.

### Composition type hunk

`typescript/src/scene-capabilities.ts:14-21`

```diff
 export type ComponentDiagnostics = {
   /** Intrinsic scalar names/units belong to the component, before outer geometry. */
   motion?: Readonly<Record<string, number>>;
   face?: ModifierBounds;
   mouth?: ModifierBounds;
+  /** Derived compatibility inspection footprint; not semantic mouth geometry. */
+  inspectionMouth?: ModifierBounds | null;
   /** Declared text layout and minimum drawn font size in canvas pixels, not glyph alpha. */
   text?: {bounds: ModifierBounds; minPx?: number};
 };
```

### Composition query/sanitizer hunk

`typescript/src/scene-evaluation.ts:176-193`, inside the existing
`componentDiagnostics()` whitelist:

```diff
   if (source.face !== undefined) result.face = region(source.face);
   if (source.mouth !== undefined) result.mouth = region(source.mouth);
+  if (source.inspectionMouth !== undefined) {
+    result.inspectionMouth = source.inspectionMouth === null
+      ? null : region(source.inspectionMouth);
+  }
   if (source.text !== undefined) {
```

The existing `:311-315` `geometryReason` input must be applied through the
same `region()` path. Thus an outer crop/transform/modifier that makes the
derived rectangle stale yields `status: 'unknown'` and the existing
`invalid-component-diagnostics`/geometry finding behavior; it never rewrites
semantic `mouth`.

No change is proposed at `:314-322`: the existing `diagnostics` object already
travels on `SceneLayer` and through `scene-query.mjs` unchanged.

### Agent helper/caller hunk

No change is proposed to the existing helper at
`astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/motion.ts:44-61`.
It remains the sole compatibility input rule:

```ts
const rawInspection = mouthInspectionRect(clip.params);
const inspection = rawInspection === null ? null : (() => {
  const {left: x, top: y, width, height} = pixelGeometry(rawInspection, view);
  return {status: 'known' as const, rect: {x, y, width, height}};
})();
```

In the existing caller at `scene.ts:15-29`, use the already computed
`presenterAt(...).view` and add only:

```diff
 import {motionAt, mouthInspectionRect, mouthStateRect, pixelGeometry, presenterAt} from './motion';

   const {view} = presenterAt(clip.params, frame, fps);
+  const rawInspection = mouthInspectionRect(clip.params);
+  const inspection = rawInspection === null ? null : (() => {
+    const {left: x, top: y, width, height} = pixelGeometry(rawInspection, view);
+    return {status: 'known' as const, rect: {x, y, width, height}};
+  })();
   const geometry = pixelGeometry(mouthStateRect(clip.params), view);
   return {
     presence: 'unknown',
     opaqueSupport: 'none',
     bounds: {status: 'known', rect: {x: 0, y: 0, width, height}},
     diagnostics: {
       motion: motionAt(clip.params, frame, fps),
       mouth: presenterMosaicAt(clip.params, clip, frame, fps)
         ? {status: 'unknown', reason: 'Presenter mouth overlay is hidden by mosaic'}
         : {status: 'known', rect: {x: geometry.left, y: geometry.top,
             width: geometry.width, height: geometry.height}},
+      inspectionMouth: inspection,
     },
   };
```

The exact caller hunk therefore also adds `mouthInspectionRect` to the existing
`motion.ts` import and computes `rawInspection`/`inspection` immediately after
the existing `const {view} = presenterAt(clip.params, frame, fps)` at
`scene.ts:15-17`. It must not derive the value from `diagnostics.mouth`,
`mouthAnchor()`, pixels, a frame-zero crop, or the private fallback. The field remains advisory
and cannot affect `presence`, `bounds`, `visible`, `coverage`, occlusion,
statistics, or threshold decisions.

## Rules and representative facts

- **Semantic preservation:** `diagnostics.mouth` is unchanged, including its
  normalized width 19 and independent UNKNOWN behavior under mosaic/outer
  geometry. `motion.mouth` remains the existing scalar codebook; valid closed
  frames still report `0.0`.
- **Explicit `{x:151,y:104,w:19}`:** semantic `mouth` and derived
  `inspectionMouth` are known with the existing 799-pixel footprint
  `(298,202,345,219)` for the retained tuple.
- **Partial `{x:151,y:104}`:** semantic `mouth` remains the normalized width-19
  / 799-pixel region, while `inspectionMouth` carries the existing helper's
  width-16 / 697-pixel region `(298,202,339,219)`.
- **Absent/default and raw-invalid:** `inspectionMouth` is `null`; semantic
  `mouth` retains its current normalized result (default remains known; the
  raw-invalid case remains the current normalized width-40 result). No null
  compatibility input is converted into a default crop.
- **Unknown:** if the helper cannot produce a valid finite rectangle, or the
  existing outer-geometry guard makes the derived result stale, publish null
  for helper refusal or `status: 'unknown'` for a known-but-invalidated
  diagnostic. Never guess from the semantic region.
- **Forged/foreign data:** Composition only shape-validates the field through
  the existing diagnostic sanitizer. A supplied field is never accepted as
  authority and cannot override semantic diagnostics, visibility, occlusion,
  coverage, or private inspection. A malformed/nonfinite rectangle follows
  the existing invalid-diagnostic finding and becomes unknown. A valid-shaped
  value from a caller that did not use the admitted helper is not evidence of
  equivalence; owner tests must bind the registered `am-presenter` caller and
  current frame identity.
- **Statistics/fallbacks:** retain the strict `fraction > 0.02` denominator,
  all retained private/public/erase statistics, private fallback, and old
  explicit results. This field only exposes the derived footprint; it does not
  alter crop mapping or comparator behavior.

## Acceptance facts, before any activation

Owner reciprocal ACK should require a pure query assertion over the existing
resource for the three facts above, plus `motion.mouth === 0.0` on a valid
closed frame, and should retain the existing retained evidence:

- explicit tuple `32349`: public/compat 799;
- partial tuple `10870`: private 697 versus public/compat 799, crossing 15
  versus 16;
- absent/raw-invalid: compatibility null;
- no pixel capture, browser run, package/pin, or caller activation as part of
  this proposal.

This packet is not an approval to add the field. Until both owners ACK, the
current no-carrier disposition remains in force and all old results/fallbacks
remain authoritative.
