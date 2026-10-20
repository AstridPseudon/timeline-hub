# App read-only adoption review: Composition public 0.0.12

Reviewed against the current App base `tl/app-m3-minimal-release-safety-refresh` / `090e1162d`, the release-12 consumer instructions, the final-theme handoff, the immutable artifact, and frozen R4 refs. No App source, dependency, pin, or vendor file was changed.

## Artifact and public contract

The supplied artifact is verified read-only:

| Check | Result |
| --- | --- |
| File | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.12.tgz` |
| SHA-256 | `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3` |
| Size | 58,444 bytes |
| Tar members | 77 regular members |

The package export map is exactly these public entries: `.`, `./evaluation`, `./theme-api`, `./registry.generated`, `./effects.generated`, `./animations.generated`, `./transitions.generated`, `./registries`, and `./package.json`. The root declaration exports the Composition/Hype components, theme provider/default/runtime conversion, animation helpers, duration, generated theme registry, modifier APIs, scene preparation/query APIs, canonical transition compilation, and registry providers. `./evaluation` additionally exposes `computeMediaTrim` and `getSanitizedPlaybackRate`, alongside clip opacity, transition/track planning, audio-envelope, scene-query, and media-capability APIs. `./theme-api` exposes the stable theme/animation/modifier/keyframe/registry-provider surface. Generated subpaths expose their corresponding registries, defaults, metadata, aliases, and IDs.

For exact consumer spelling, the runtime root names are `TIMELINE_COMPOSITION_SCAFFOLD`, `TimelineComposition`, `HypeComposition`, `composeAnimations`, `normalizeAnimationReferences`, `resolveAnimationReferences`, `ThemeProvider`, `useTheme`, `DEFAULT_THEME`, `toRuntimeTheme`, `getTimelineDurationInFrames`, `THEME_PACKAGE_REGISTRY`, `THEME_PACKAGE_CLIP_TYPES`, `MODIFIER_REGISTRY`, `composeModifiers`, `declareModifier`, `ModifierAdmissionError`, `mediaModifierBounds`, `prepareCompositionScene`, `compileCanonicalTransitions`, `prepareScene`, `querySceneFrame`, `queryCompositionSceneFrame`, `querySceneOcclusion`, `resolveElementRegistries`, `ElementRegistryProvider`, and `useElementRegistries`. The evaluation names are `declareAppTransition`, `admitTransitionContribution`, `transitionContributionIdentity`, `TransitionAdmissionError`, `clipOpacity`, `computeMediaTrim`, `getSanitizedPlaybackRate`, `prepareTrack`, `prepareDeclaredTrack`, `queryDrawFrame`, `queryTrackFrame`, `keyframeOrigin`, `timelineKeyframeTime`, `spriteKeyframeFrame`, `declareKeyframeOrigin`, `loopPhase`, `positiveModulo`, `spriteSheetIndex`, `mediaModifierBounds`, `compileAudioEnvelope`, `validateAudioEnvelope`, `audioEnvelopeAt`, `applyAudioEnvelope`, `audioEnvelopeWav`, `AudioEnvelopeError`, `prepareScene`, `querySceneFrame`, `queryCompositionSceneFrame`, `querySceneOcclusion`, `VIDEO_INTERPRETATION`, `IMAGE_INTERPRETATION`, and `provenOpaqueMedia`. The generated subpaths expose their declared IDs/registries/defaults/metadata, and `./registries` exposes `ElementRegistryProvider` and `useElementRegistries`.

The full public `DEFAULT_THEME` is the same as Agent's read-only `astrid/core/theme/_schema.py:174-186` `BUILTIN_DEFAULT_THEME` (and `builtin_theme()` returns a fresh copy):

```text
id: banodoco-default
visual.color: fg #FAFAFA, bg #050814, accent #67E8F9
visual.type.families: heading Arial, body Arial, mono monospace
visual.type.size: base 32, small 22, large 84
visual.type.weight: normal 400, bold 600
visual.type.lineHeight: 1.2
visual.motion.fadeMs: 450
visual.canvas: 1920 x 1080 @ 30fps
```

This is the approved implicit default. It intentionally changes an App absent/uninstalled-theme preview from the former public default: black background, white foreground/accent, Georgia typography, 64px base size, 700 bold, 1.1 line height, and 250ms fade to navy/Arial/cyan and the complete Agent values above. Explicit authored or installed theme values remain explicit; they must not be silently rewritten.

## Non-theme artifact deltas that App must preserve

The public 0.0.12 build contains the final Composition changes at the source seams recorded by the release handoff:

- `typescript/src/TimelineComposition.tsx:328` uses `DEFAULT_THEME.visual.color.bg` for the omitted-theme root fallback. An explicit `props.theme` background still wins.
- `typescript/src/scene-evaluation.ts:240` uses an own-property check before applying `roles[clip.id]`, then falls back to `plate -> picture` and all other tracks -> `content`. This prevents inherited keys such as `__proto__`, `constructor`, and `toString` from becoming roles.
- `./evaluation` publicly exports `computeMediaTrim` and `getSanitizedPlaybackRate`. App currently uses its local `src/tools/video-editor/lib/config-utils.ts` helpers from `AudioTrack.tsx`, `VisualClip.tsx`, and `playerEvaluation.ts`; the pin does not require replacing those helpers.

The 0.0.12 artifact was inspected as extracted read-only data only. No source or dependency directory was overwritten, and no rendering/evaluation/browser run was performed by this review.

## Exact App paths and theme-test delta

The adoption worker should keep the source policy minimal:

1. `package.json`: change only `@banodoco/timeline-composition` from `file:vendor/artifacts/banodoco-timeline-composition-0.0.10.tgz` to `file:vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz`.
2. `package-lock.json`: update the root dependency and the package entry to version `0.0.12`, resolved path `file:vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz`, and the artifact's recorded SHA-512 integrity `sha512-490yQtC4k3cuBQJ4Aee5qEqOPNrlQrXPQkE0p6R8UDACAcT8amHe8EjCRI4vE+HtvXwUiy8zBjm7RcW7aTv9eA==`.
3. Copy the exact supplied bytes to `vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz`. Preserve old archives and unrelated vendors.
4. `config/vite/timelineCompositionPackage.test.mjs`: update the test title/path, expected size `58444`, SHA-256 above, installed/manifest version `0.0.12`, and the manifest-version assertion. Keep every public-export and shared-peer resolution assertion.

Current App source already consumes the package default through `src/tools/video-editor/compositions/installed-themes.ts`; `banodoco-default` is registered as `DEFAULT_THEME`. `src/tools/video-editor/compositions/TimelineRenderer.tsx:1751` already paints `theme.visual.color.bg`, so no product source change is needed for the package pin. `src/tools/video-editor/compositions/playerEvaluation.ts:60,83` still resolves its existing local theme for evaluator calls; do not invent a new transport or refactor it in this adoption batch.

The exact stale implicit-default test material is in `src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx`:

- The historical no-theme assertions (in the public10 source) were `data-accent=#ffffff`, `data-bg=#000000`, and `data-heading=Georgia, serif`. The current base already made this test compare against `resolveTimelineRenderTheme(...)`, but its two hoisted `theme-api` mocks still contain black/Georgia-era values at approximately lines 90-180 and 264-290. Update/remove those mocks so the test uses the actual public 0.0.12 full default (navy/Arial/cyan and all fields), not a partial hand-written default.
- The existing `deep-merges timeline theme_overrides onto the installed theme` case around lines 716-732 is an explicit `2rp` positive. Keep its black `2rp` background, Sixtyfour heading, and accent override; those literals are not the implicit default and must not be bulk-replaced.
- Generic black literals in `AudioReactiveColour.test.tsx`, `AudioReactiveColour.tsx`, and unrelated media fixtures are authored/component defaults, not Composition `DEFAULT_THEME` assertions; leave them unchanged.
- `TimelineRenderer.dynamic.test.tsx` uses a deliberately small mock for the dynamic-placeholder path and has no implicit-default assertion. It does not need a theme-policy rewrite.

Add or retain a focused `src/tools/video-editor/compositions/installed-themes.test.ts` suite with these positives:

- `undefined`, `banodoco-default`, and an unknown slug resolve to the complete public 0.0.12 `DEFAULT_THEME` (whole-object equality, not only color fields).
- An explicit `2rp` theme plus a nested `theme_overrides.visual.color.bg` override preserves all other 2rp fields and does not mutate the registry.
- A complete authored `theme_overrides.visual` value is returned without default leakage.
- A partial nested override such as `visual.color.accent` preserves the public default's bg/fg, typography, motion, and canvas, and a later no-override resolution returns the unchanged default.

These tests prove the intentional black/Georgia/white -> navy/Arial/cyan implicit change while preserving explicit-theme and nested-merge behavior. Do not add an App-local Agent default literal or an `it.fails` marker for this approved public-default policy.

## Acceptance order and commands

The Runtime final document/tuple is still pending. Do not qualify the current App browser against an unmatched Runtime. Before any current browser lane, Agent must publish the same Runtime pin plus public 0.0.12 and pass its equal-theme test; App then consumes that exact pair.

After the full quiet window, the normal offline install command in the finished App adoption worktree is (not run here):

```sh
cd /home/user/work/wt/<app-root-adoption-worktree>
npm install --offline --no-audit --no-fund
```

The future root qualifier should then run the package-resolution test and targeted App theme/Composition consumers, for example:

```sh
node --test config/vite/timelineCompositionPackage.test.mjs
npx vitest run --config config/testing/vitest.config.ts \
  src/tools/video-editor/compositions/installed-themes.test.ts \
  src/tools/video-editor/compositions/TimelineRenderer.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.dynamic.test.tsx \
  src/tools/video-editor/compositions/playerEvaluation.test.ts \
  src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx
```

Those commands are acceptance proposals only; this worker did not install, run Vitest, build, typecheck, render, use a browser/socket, or request a full suite. The central service must run the post-pair current App browser qualification with exact Agent/Runtime source pins. No current browser result is claimed here.
