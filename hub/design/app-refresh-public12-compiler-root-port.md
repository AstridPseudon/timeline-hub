**Public12 compiler/root port onto refreshed MAIN — source candidate complete, held for freeze.**

Base commit `667498cc49b4ec2b1ccd3a515eb87311c5126c93`, tree `74d6c8033b1e006e8dbd4accc361b4e1288093e9`. Reviewed source: `c866da88e6acb92e6f7194324e0a29bfacab3b4b`; plan and full MAIN overlap review followed. No integration edit, commit, merge, checkout, install, push, build, project typecheck, full suite, browser, socket, or localhost run/request occurred.

The candidate ports the reviewed public12 root/lock/bundler/vendor retirement, public evaluator/compiler adapters, initial verified projection, native label capture/recovery, outbox safety, after-ACK `04346844f` scheduling fix and additive M2 Gate 5 source. Main’s render/download/admission cohort and provider remain byte-identical. No native None/PARAM/delete/split/trim/requester activation was included.

**Source and dependency identity**

- Composition `0.0.12`: SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 58,444 bytes, 77 regular archive members. All 77 installed files match the archive byte-for-byte. The unnecessary intermediate 0.0.10 archive was excluded.
- The entire public `DEFAULT_THEME` equals the read-only Agent `BUILTIN_DEFAULT_THEME` in `/home/user/peteromallet/astrid-agent/astrid/core/theme/_schema.py`, including every nested field. This is a source comparison, not Agent package/pair qualification. Whole-object default, explicit 2rp, complete authored visual, partial nested merge and no-mutation tests pass. The intended implicit preview adoption is navy/Arial/cyan; existing final-export default and explicit themes remain preserved.
- Runtime is the exact reviewed **development-only 0.2.9** producer `94114269d1ce23ab3224d7eca5a85138ce2b5fed` at `/home/user/work/wt/app-m3-runtime029-producer-source`. Only `runtime.lock.json` plus its three normally generated TypeScript files change. The normal update and producer-aware check were used; no fields were guessed and no 0.2.10 source adopted. Runtime P1 republication announced at 09:34 remains a release prerequisite.
- Only this worktree’s `node_modules` symlink was repointed to `/tmp/app-coherent-deps12/node_modules`. Every retained root dependency is present at its package-lock version, including NEW MAIN dependencies. The retired theme package is intentionally removed by the reviewed public package migration. No shared file/link/cache was changed: before/final snapshots of **35,464** entries match exactly (path, mode, size, modification time, link target).

**Minimality and overlap decisions**

| Boundary | Final composition and evidence |
| --- | --- |
| Provider/boot/auth | MAIN `schemaDigest`, exported `POLL_INTERVAL_MS`, two-reading boot behavior and `Object.entries(...).find(...)` own-key lookup remain unchanged. No redundant own-property helper or old boot override. Provider and gated-auth tests pass. |
| Render/admission/download | MAIN `useRenderState`, `renderRouter`, render pipeline/runtime and controls, with their tests, are byte-identical. MAIN streaming/blob download, `/api/astrid` admission, admitted seam warnings and omission of editor-counter authority remain intact. No hook-owned download method/type/default survives in the mixed state/store files. Distinct render scope/integrity/provenance follow-ups remain with the render owner. |
| Player/mobile portal | MAIN shell and preview lifecycle tests remain byte-identical. The surface adds only compiler selection/prop wiring; its content-scope key, stable host, layout-slot movement and single shell-owned portal remain MAIN’s. No `attachmentGeneration` remount restored. The compiler vector joins the existing deferred config/revision delivery rather than becoming a separate delivery channel. |
| Label mobile overlap | NEW MAIN explicitly leaves phone/tablet track settings to the agent (`TrackLabel.tsx` and unchanged original row tests). Keep that product behavior. Retain the reviewed positive label-capture assertions as **8 `it.fails` cases**, covering three row cases plus canvas forwarding on both concrete MAIN device classes. Each names the upstream touch label-input requirement needed to pass. Their positive assertions were preserved, not rewritten to expect refusal or missing controls. All original MAIN row/canvas assertions remain unchanged. Desktop label capture, empty value, remote-change capture and refusal/draft preservation pass. |
| Projection/recovery/root/settings | Verified initial basis checks, generation/disposal fences, atomic `editProjection` pairing, late observations, recovery, opaque-root serialization and raw shot settings protections remain. The ShotEditor source/test and save barrier remain byte-identical to the refresh. Their scoped regressions pass. |
| Bootstrap/URL/auth | MAIN canonical URL identity and canonical-ID/alias/CAS bootstrap logic remain. No older bootstrap helper, chat, authentication or URL authority was substituted. Native bootstrap and requester work remain separate. |
| Gate 5 | AST comparison against the reviewed pre-043 source (`04346844f^`) proves **all 6 existing case bodies and all 21 existing function helpers byte-identical**, plus one new Gate 5 case and one new helper. This is the reviewed migrated six-case source, not a claim that its older pre-migration legacy writer expectations were unchanged. Also retain MAIN’s original `holdTimelineSaves` support helper for its remaining consumers and add `holdCommandRequests` without deleting it. No browser/discovery execution claimed. |

Static audit: 22 protected MAIN files byte-identical; all original MAIN row/canvas assertions retained; all 6/21 reviewed journey members retained; 63 changed TypeScript/TSX files parse without syntax diagnostics; changed paths match the exact allowlist. [Audit JSON](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refresh-public12-compiler-root-port/notes/audit.json), [repeatable script](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refresh-public12-compiler-root-port/notes/audit.cjs).

Authored product on the **27 changed `src/` product paths**, excluding tests, fixtures, generated contract data and vendor source: **15,096 → 15,912 lines; +1,021 / −205; net +816**. This is the changed-path count, not an area-wide Timeline core census or unchanged MAIN infrastructure. The exact product-path list is in audit JSON. Duplicate vendor and local audio-fade code is retired by the reviewed public evaluator adoption; its replacement audio/media conformance coverage runs. Existing audio semantics changes remain those already settled in PLAN.

**Exact commands and results**

Commands run from `/home/user/work/wt/app-m3-refresh-public12-compiler-root-port`. `N` below is the exact worker notes directory; commands use private caches and one Vitest worker.

```sh
N=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refresh-public12-compiler-root-port/notes
node scripts/vendor-lock.mjs update runtime.lock.json --producer /home/user/work/wt/app-m3-runtime029-producer-source
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/app-m3-runtime029-producer-source
node --test config/vite/timelineCompositionPackage.test.mjs
node config/vite/timelineCompositionPackage.test.mjs
node node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 $(cat "$N/test-files-initial.txt")
node node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 $(cat "$N/test-files.txt")
node node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx
node node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/browser/BrowserVideoEditorProvider.test.tsx
node node_modules/eslint/bin/eslint.js --no-cache $(cat "$N/lint-files.txt")
git show HEAD:src/tools/video-editor/components/TimelineEditor/TimelineEditorCoreBody.tsx | node node_modules/eslint/bin/eslint.js --no-cache --stdin --stdin-filename src/tools/video-editor/components/TimelineEditor/TimelineEditorCoreBody.tsx
node node_modules/eslint/bin/eslint.js --no-cache src/tools/video-editor/components/TimelineEditor/TrackLabel.tsx src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx
node "$N/audit.cjs"
git diff --check
```

| Command/evidence | Result |
| --- | --- |
| Normal Runtime update/check | Exit 0; matches pinned producer. Generated bytes match the reviewed c866 producer artifacts. |
| Package/peer guard | Exit 0; direct run reports **7 passed**, checking all six bundler configs, immutable artifact and shared peers. `node --test` also exits 0 (outer file summary). |
| Initial runner setup | First attempt stopped before tests: runner loading lacks Vite’s injected `__dirname`. Private config adds that compatibility value before loading the repository config and places cacheDir under worker notes; no repository config/test weakening. |
| Initial 39-file scoped run | Exit 1: 37 files passed; **1,060 tests passed, 3 failed**; one suite failed to parse due to my conflict-resolution script error. The script error was corrected, all changed sources parsed, and affected files rerun. Three failures were stale touch-control assumptions. [Log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refresh-public12-compiler-root-port/notes/vitest.log). |
| 52-file scoped run | Exit 1: 51 files passed; **1,491 passed, 3 expected failures, 1 failed**. Only the additional canvas touch-control assumption remained. [Exact file list](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refresh-public12-compiler-root-port/notes/test-files.txt), [log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refresh-public12-compiler-root-port/notes/vitest-final.log). |
| Final row/canvas rerun | Exit 0: **2 files, 106 passed + 8 expected failures**. Reconciles the old generic `touch` cases with MAIN’s concrete phone/tablet types, retaining positive assertions and MAIN’s original controls-absence assertions. [Log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refresh-public12-compiler-root-port/notes/vitest-resolved.log). |
| Final provider follow-up | Exit 0: **2 files, 83 passed**, after dropping two residual old-download type/default lines from the mixed state/store files. [Log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refresh-public12-compiler-root-port/notes/vitest-providers.log). |
| Combined final scoped evidence | **54 distinct files: 1,574 passing tests + 8 retained expected failures; no unresolved ordinary test failure.** Counts use the latest affected-file runs, not addition of repeated assertions. |
| Scoped product ESLint | Exit 1: one existing `react-hooks/exhaustive-deps` unnecessary `deviceClass` dependency in `TimelineEditorCoreBody.tsx` (candidate line 826). The exact HEAD source reproduces the same sole error at line 824; left unchanged. [Candidate log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refresh-public12-compiler-root-port/notes/eslint.log), [baseline log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refresh-public12-compiler-root-port/notes/eslint-base.log). |
| Resolved row/canvas ESLint | Exit 0, no errors/warnings. [Log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refresh-public12-compiler-root-port/notes/eslint-resolved.log). |
| Static source audit / diff check | Exit 0. [Audit](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refresh-public12-compiler-root-port/notes/audit.log). |
| Dependency/theme audit | Archive checks and entire Agent/public default equality pass; before/final dependency/cache snapshots match all 35,464 entries. [Result](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refresh-public12-compiler-root-port/notes/dependency-theme-audit.log). |

No full suite, build, project tsc, real Runtime acceptance, same-pair Agent qualification, browser, media rendering or end-to-end Gate 5 was run or requested. The stored Gate 5 source is not release evidence. There is no blocker to this source handoff; release remains held for the safe republished Runtime/Agent/App pair and actual browser qualification. Review the eight MAIN-overlap expected failures explicitly and keep the existing lint diagnostic classified as baseline. Render-owner scope/integrity and Runtime identity-label follow-ups remain outside this port.

**Exact change allowlist: 163 paths** (SHA-256 of newline-delimited [allowlist.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refresh-public12-compiler-root-port/notes/allowlist.txt): `9d4d103f700f372572fede6ce0b6e38df4b8bc9c667f4f6c941990a5f38d9469`). Deleted vendor paths are included; no other repository path is changed.

```text
config/testing/vitest.astrid-renderer.config.ts
config/testing/vitest.boundary.config.ts
config/testing/vitest.config.ts
config/testing/vitest.edge.aliases.ts
config/vite/timelineCompositionPackage.test.mjs
config/vite/vite.config.ts
package-lock.json
package.json
runtime.lock.json
scripts/astrid-landing/public-host-browser/vite.config.ts
src/integrations/runtime/generated-contract-metadata.ts
src/integrations/runtime/generated.ts
src/integrations/runtime/timeline-commit-types.ts
src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts
src/tools/video-editor/commands/commitOutbox.test.ts
src/tools/video-editor/commands/commitOutbox.ts
src/tools/video-editor/commands/commitSession.test.ts
src/tools/video-editor/commands/commitSession.ts
src/tools/video-editor/commands/fixtures/recipe_m2_app_track_label.json
src/tools/video-editor/commands/trackLabelCapture.test.ts
src/tools/video-editor/commands/trackLabelCapture.ts
src/tools/video-editor/commands/trackLabelGesture.test.ts
src/tools/video-editor/commands/trackLabelGesture.ts
src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.ts
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.tsx
src/tools/video-editor/components/TimelineCommandRecovery.test.tsx
src/tools/video-editor/components/TimelineCommandRecovery.tsx
src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx
src/tools/video-editor/components/TimelineEditor/TimelineCanvas.tsx
src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.tsx
src/tools/video-editor/components/TimelineEditor/TimelineEditorCoreBody.tsx
src/tools/video-editor/components/TimelineEditor/TrackLabel.tsx
src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx
src/tools/video-editor/components/TimelineEditor/TrackListRenderer.tsx
src/tools/video-editor/compositions/AudioTrack.test.tsx
src/tools/video-editor/compositions/AudioTrack.tsx
src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx
src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx
src/tools/video-editor/compositions/TimelineRenderer.test.tsx
src/tools/video-editor/compositions/TimelineRenderer.tsx
src/tools/video-editor/compositions/VisualClip.evaluation.test.tsx
src/tools/video-editor/compositions/VisualClip.tsx
src/tools/video-editor/compositions/installed-themes.test.ts
src/tools/video-editor/compositions/playerEvaluation.test.ts
src/tools/video-editor/compositions/playerEvaluation.ts
src/tools/video-editor/compositions/vendoredTimelineCompositionAliases.test.ts
src/tools/video-editor/contexts/VideoEditorProvider.tsx
src/tools/video-editor/data/shotCompositionProjection.test.ts
src/tools/video-editor/data/shotCompositionProjection.ts
src/tools/video-editor/hooks/timelineStore.ts
src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx
src/tools/video-editor/hooks/useTimelineCommandSession.ts
src/tools/video-editor/hooks/useTimelineOps.test.ts
src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts
src/tools/video-editor/hooks/useTimelineOps.ts
src/tools/video-editor/hooks/useTimelinePersistence.test.tsx
src/tools/video-editor/hooks/useTimelineState.ts
src/tools/video-editor/hooks/useTimelineState.types.ts
src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts
src/tools/video-editor/hooks/useTimelineTrackManagement.ts
src/tools/video-editor/lib/audioFade.test.ts
src/tools/video-editor/lib/audioFade.ts
src/tools/video-editor/lib/serialize.ts
tests/e2e/local/support/app.ts
tests/e2e/local/support/astrid.ts
tests/e2e/local/three-products.spec.ts
vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz
vendor/banodoco-animations/fade-up/component.jsx
vendor/banodoco-animations/fade-up/component.tsx
vendor/banodoco-animations/fade-up/defaults.json
vendor/banodoco-animations/fade-up/meta.json
vendor/banodoco-animations/fade-up/schema.json
vendor/banodoco-animations/fade/component.jsx
vendor/banodoco-animations/fade/component.tsx
vendor/banodoco-animations/fade/defaults.json
vendor/banodoco-animations/fade/meta.json
vendor/banodoco-animations/fade/schema.json
vendor/banodoco-animations/scale-in/component.jsx
vendor/banodoco-animations/scale-in/component.tsx
vendor/banodoco-animations/scale-in/defaults.json
vendor/banodoco-animations/scale-in/meta.json
vendor/banodoco-animations/scale-in/schema.json
vendor/banodoco-animations/slide-left/component.jsx
vendor/banodoco-animations/slide-left/component.tsx
vendor/banodoco-animations/slide-left/defaults.json
vendor/banodoco-animations/slide-left/meta.json
vendor/banodoco-animations/slide-left/schema.json
vendor/banodoco-animations/slide-up/component.jsx
vendor/banodoco-animations/slide-up/component.tsx
vendor/banodoco-animations/slide-up/defaults.json
vendor/banodoco-animations/slide-up/meta.json
vendor/banodoco-animations/slide-up/schema.json
vendor/banodoco-animations/type-on/component.jsx
vendor/banodoco-animations/type-on/component.tsx
vendor/banodoco-animations/type-on/defaults.json
vendor/banodoco-animations/type-on/meta.json
vendor/banodoco-animations/type-on/schema.json
vendor/banodoco-effects/text-card/component.jsx
vendor/banodoco-effects/text-card/component.tsx
vendor/banodoco-effects/text-card/defaults.json
vendor/banodoco-effects/text-card/meta.json
vendor/banodoco-effects/text-card/schema.json
vendor/banodoco-transitions/cross-fade/component.jsx
vendor/banodoco-transitions/cross-fade/component.tsx
vendor/banodoco-transitions/cross-fade/defaults.json
vendor/banodoco-transitions/cross-fade/meta.json
vendor/banodoco-transitions/cross-fade/schema.json
vendor/banodoco-transitions/fade/component.jsx
vendor/banodoco-transitions/fade/component.tsx
vendor/banodoco-transitions/fade/defaults.json
vendor/banodoco-transitions/fade/meta.json
vendor/banodoco-transitions/fade/schema.json
vendor/timeline-composition/Makefile
vendor/timeline-composition/package.json
vendor/timeline-composition/scripts/gen-registry.ts
vendor/timeline-composition/typescript/src/AudioTrack.tsx
vendor/timeline-composition/typescript/src/ThemeContext.tsx
vendor/timeline-composition/typescript/src/TimelineComposition.tsx
vendor/timeline-composition/typescript/src/VisualClip.tsx
vendor/timeline-composition/typescript/src/animations.generated.ts
vendor/timeline-composition/typescript/src/effects-types.ts
vendor/timeline-composition/typescript/src/effects.generated.ts
vendor/timeline-composition/typescript/src/index.ts
vendor/timeline-composition/typescript/src/lib/animations.tsx
vendor/timeline-composition/typescript/src/lib/duration.ts
vendor/timeline-composition/typescript/src/lib/effect-params.ts
vendor/timeline-composition/typescript/src/lib/fade.ts
vendor/timeline-composition/typescript/src/lib/render-bounds.ts
vendor/timeline-composition/typescript/src/lib/tracks.ts
vendor/timeline-composition/typescript/src/lib/transitions.tsx
vendor/timeline-composition/typescript/src/lib/trim.ts
vendor/timeline-composition/typescript/src/registry.generated.ts
vendor/timeline-composition/typescript/src/theme-api.ts
vendor/timeline-composition/typescript/src/transitions.generated.ts
vendor/timeline-composition/typescript/src/types.ts
vendor/timeline-composition/typescript/src/workspace-aliases.d.ts
vendor/timeline-composition/typescript/tests/scaffold.test.ts
vendor/timeline-composition/typescript/tests/theme-api-smoke.ts
vendor/timeline-composition/typescript/tsconfig.json
vendor/timeline-composition/typescript/tsconfig.test.json
vendor/timeline-theme-2rp/package.json
vendor/timeline-theme-2rp/src/effects/art-card/component.tsx
vendor/timeline-theme-2rp/src/effects/art-card/defaults.json
vendor/timeline-theme-2rp/src/effects/art-card/meta.json
vendor/timeline-theme-2rp/src/effects/art-card/schema.json
vendor/timeline-theme-2rp/src/effects/cta-card/component.tsx
vendor/timeline-theme-2rp/src/effects/cta-card/defaults.json
vendor/timeline-theme-2rp/src/effects/cta-card/meta.json
vendor/timeline-theme-2rp/src/effects/cta-card/schema.json
vendor/timeline-theme-2rp/src/effects/resource-card/component.tsx
vendor/timeline-theme-2rp/src/effects/resource-card/defaults.json
vendor/timeline-theme-2rp/src/effects/resource-card/meta.json
vendor/timeline-theme-2rp/src/effects/resource-card/schema.json
vendor/timeline-theme-2rp/src/effects/section-hook/component.tsx
vendor/timeline-theme-2rp/src/effects/section-hook/defaults.json
vendor/timeline-theme-2rp/src/effects/section-hook/meta.json
vendor/timeline-theme-2rp/src/effects/section-hook/schema.json
vendor/timeline-theme-2rp/src/index.ts
vendor/timeline-theme-2rp/theme.json
```
