# D10 Home consumer authorized port

## Exact diff

Applied only the Home hunk from `design/handoff-vw-m3-d10-owner-packet.patch`, against bridge `27ee90ac1`.

- Changed file: `src/pages/Home/astrid-public-host.tsx`
- Diff: 6 insertions, 18 deletions
- Removed the nine direct Composition-owned vendor imports and their nine explicit component entries.
- Added `PUBLIC_COMPOSITION_ELEMENT_COMPONENTS` and spread its registry entries into the existing `componentEntries` list.
- No vendor file, provenance file, pin, package, catalog, schema, loader, API, policy, or test was edited.

The resulting source diff is:

```diff
 import type { ComponentType } from 'react';
 import { ASTRID_RENDERING_ELEMENTS } from '@astrid-public/packs/rendering/elements/public-catalog.ts';
-import FadeAnimation from '@astrid-public/packs/rendering/rendering/elements/animations/fade/component.tsx';
-import FadeUpAnimation from '@astrid-public/packs/rendering/rendering/elements/animations/fade-up/component.tsx';
-import ScaleInAnimation from '@astrid-public/packs/rendering/rendering/elements/animations/scale-in/component.tsx';
-import SlideLeftAnimation from '@astrid-public/packs/rendering/rendering/elements/animations/slide-left/component.tsx';
-import SlideUpAnimation from '@astrid-public/packs/rendering/rendering/elements/animations/slide-up/component.tsx';
-import TypeOnAnimation from '@astrid-public/packs/rendering/rendering/elements/animations/type-on/component.tsx';
 import AudioReactiveColour from '@astrid-public/packs/rendering/rendering/elements/effects/audio-reactive-colour/component.tsx';
-import TextCard from '@astrid-public/packs/rendering/rendering/elements/effects/text-card/component.tsx';
-import CrossFadeTransition from '@astrid-public/packs/rendering/rendering/elements/transitions/cross-fade/component.tsx';
-import FadeTransition from '@astrid-public/packs/rendering/rendering/elements/transitions/fade/component.tsx';
 import EndSpanningLayer from '@astrid-public/packs/local/rendering/elements/effects/end-spanning-layer/component.tsx';
 import FrameOverlay from '@astrid-public/packs/local/rendering/elements/effects/frame-overlay/component.tsx';
@@
 import frame from '@astrid-public/packs/local/rendering/elements/effects/frame-overlay/assets/frame.png?url';
 import { createAstridPreviewAssetWrapper } from '@/tools/video-editor/sequences/components/createAstridPreviewAssetWrapper.tsx';
+import { PUBLIC_COMPOSITION_ELEMENT_COMPONENTS } from '@/tools/video-editor/runtime/publicCompositionElementRegistry.ts';
@@
 const FrameOverlayPreview = createAstridPreviewAssetWrapper(FrameOverlay, {frame});
 
 const asComponent = (value: unknown) => value as ComponentType<AstridElementComponentProps>;
+const compositionComponentEntries = Object.entries(PUBLIC_COMPOSITION_ELEMENT_COMPONENTS) as Array<[
+  string,
+  ComponentType<AstridElementComponentProps>,
+]>;
 const componentEntries: Array<[string, ComponentType<AstridElementComponentProps>]> = [
-  ['animation:fade', asComponent(FadeAnimation)],
-  ['animation:fade-up', asComponent(FadeUpAnimation)],
-  ['animation:scale-in', asComponent(ScaleInAnimation)],
-  ['animation:slide-left', asComponent(SlideLeftAnimation)],
-  ['animation:slide-up', asComponent(SlideUpAnimation)],
-  ['animation:type-on', asComponent(TypeOnAnimation)],
+  ...compositionComponentEntries,
   ['effect:audio-reactive-colour', asComponent(AudioReactiveColour)],
-  ['effect:text-card', asComponent(TextCard)],
-  ['transition:cross-fade', asComponent(CrossFadeTransition)],
-  ['transition:fade', asComponent(FadeTransition)],
   ['effect:end-spanning-layer', asComponent(EndSpanningLayerPreview)],
   ['effect:frame-overlay', asComponent(FrameOverlayPreview)],
 ];
```

## Tests and controls

All Vitest controls used the read-only PRIVATE13 Composition `0.0.13` graph. A temporary overlay in `/tmp` routed `@banodoco/timeline-composition` to PRIVATE13 and was removed afterward; the worker's `node_modules` link was restored to `/home/user/work/app/node_modules`.

1. `timeout 60s env NODE_OPTIONS='--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-main17-independent-refresh-review/vitest-preload.cjs' node /home/user/work/app/node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/runtime/publicCompositionElementRegistry.test.ts src/tools/video-editor/compositions/vendoredTimelineCompositionAliases.test.ts src/tools/video-editor/compositions/TimelineRenderer.public-host.qualification.test.tsx` — PASS, 3 files / 20 tests.
2. `node scripts/build/verify-astrid-vendor-sources.mjs` — PASS, 65 pinned source files, 155 vendor files, 11 Home `@astrid-public` imports.
3. `node --test scripts/quality/astrid-public-boundary.test.mjs` — PASS, 1 test.
4. `git diff --check` — PASS.

No full suite, project TypeScript check, install, browser, build, network, or live-socket test was run, per task scope.

## Preserved custom paths and authority

- Catalog authority remains `ASTRID_RENDERING_ELEMENTS` from `public-catalog.ts`; descriptor identity, schema, `packId`, revision, renderability, and unknown diagnostics remain host-controlled.
- `AudioReactiveColour`, local `EndSpanningLayer`, local `FrameOverlay`, the preview asset wrapper, and all seven local asset URL imports remain unchanged.
- Sequence registration, dynamic sequence resolution, capability reporting, and unknown-element handling remain unchanged.
- Normal Vite still resolves `ASTRID_PUBLIC_CHECKOUT` through `resolveAstridSource(..., 'ASTRID_PUBLIC_CHECKOUT')` and the `@astrid-public` alias in `config/vite/vite.config.ts`.
- Standalone public-host Vite still requires the absolute `ASTRID_PUBLIC_CHECKOUT`, realpaths `<checkout>/astrid`, and uses the same `@astrid-public` alias in `scripts/astrid-landing/public-host-browser/vite.config.ts`.

## Remaining D10 blocker

Agent source removal and the normal vendor refresh/provenance regeneration are still outstanding. The nine vendor implementation files remain present and no provenance/pin deletion was attempted. D10 vendor-file retirement must wait for the Agent source removal commit and the normal refresh to produce updated provenance.
