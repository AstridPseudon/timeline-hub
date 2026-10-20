# vw-m3-known-cliplook-source-independent-review

## Decision

**APPROVE** the source proposal at `7e38f9c4e5359ab1e9d6670af00d2ec743e292f3` (`feat(composition): evaluate known clip-look scene geometry`) for source/release-readiness purposes.

This is not a package publication or version decision. The orchestrator/version owner must decide the package version and publication step before release. The proposal leaves `package.json` and `package-lock.json` unchanged.

## Scope and exact diff

Reviewed `HEAD^..HEAD` (`e7ef7a0729a2d7dad3c0ae60da9e6bb8f844d332..7e38f9c4e5359ab1e9d6670af00d2ec743e292f3`) in the assigned Composition worktree:

`/home/user/work/wt/vw-m3-known-cliplook-source-independent-review`

Six files changed, `149 insertions(+), 38 deletions(-)`:

- `typescript/src/builtins/animations/fade-up/component.tsx` — `6/12`
- `typescript/src/builtins/animations/scale-in/component.tsx` — `6/12`
- `typescript/src/lib/clip-look.ts` — `21/3`
- `typescript/src/scene-evaluation.ts` — `70/8`
- `typescript/tests/scene-diagnostics.test.ts` — `7/3`
- `typescript/tests/scene-evaluation.test.ts` — `39/0`

The source portion is `103 additions/35 deletions`; tests are `46 additions/3 deletions`. No other paths changed. There is no package pin, tarball, repack, generated package artifact, new root export, DTO, or public signature change. `BuiltinClipLookStyle` remains an internal helper export from `lib/clip-look.ts`, not a package-root API.

Key reviewed locations in the proposal tip: shared render helper at `typescript/src/lib/clip-look.ts:185-199`; known entrance admission at `typescript/src/scene-evaluation.ts:73-111`; crop/entrance/exit handling at `typescript/src/scene-evaluation.ts:226-248`; diagnostic-region invalidation at `typescript/src/scene-evaluation.ts:295-298`; wrapper call sites at the two changed builtin component files, lines `1-24`.

## Source review

- `fade-up` and `scale-in` now call the exact shared `builtinClipLookStyle` helper used by Scene evaluation. The helper preserves the existing Remotion spring configuration (`damping: 14`, `stiffness: 110`), linear interpolation ranges, explicit progress/easing behavior, and spring overshoot render styles.
- Crop geometry reuses `getVisibleBoundsFromCrop` and `computeRenderBounds` from the existing render-bounds implementation. Crop is known only for an element with known bounds and no custom modifiers.
- Scene opacity and geometry use `draw.contentFrame`, matching the renderer's `ClipLook` clock after transition planning. `queryTrackFrame` retains the existing half-open `[drawStart, drawStart + drawDuration)` mount interval, and incoming transition content continues to use the existing nonnegative incoming clock.
- Unknown animation composition, unknown custom animation IDs, malformed animation/easing data, custom-modifier crop, and all exit animation paths remain unknown rather than manufacturing support or alpha.
- When crop or an active known entrance transform changes outer geometry, component diagnostic regions and `minPx` are invalidated through the geometry reason; old coordinates are not silently reused. Motion scalars remain available as intrinsic values.
- Existing focused tests cover the known crop/entrance cases, unknown custom modifier geometry, half-open entrance boundaries, incoming clocks, and diagnostic invalidation. No main-feature regression was found in the reviewed source.

## Evidence

All commands ran in the assigned worktree, using a temporary symlink to the read-only shared Composition dependency install. Generated `dist/` and `typescript/test-dist/` were removed afterward.

- `npm run build:test` — PASS.
- `node --import ./typescript/tests/register-extensionless.mjs --test typescript/test-dist/tests/scene-evaluation.test.js typescript/test-dist/tests/scene-diagnostics.test.js` — PASS, 2 tests, 0 failures.
- `node --import ./typescript/tests/register-extensionless.mjs --test typescript/test-dist/tests/animations.test.js typescript/test-dist/tests/registries.test.js typescript/test-dist/tests/evaluation.test.js typescript/test-dist/tests/clip-opacity.test.js` — PASS, 4 tests, 0 failures.
- `node --import ./typescript/tests/register-extensionless.mjs --input-type=module` with SSR probes for `FadeUp` and `ScaleIn` — PASS; output retained the prior spring values and explicit linear styles (`translateY(20px)`/`scale(0.9249999999999999)` at the existing pinned fixture point).
- `npm run gen-registry:check` — PASS.
- `npm run build:ts` — PASS.
- `git diff --check HEAD^ HEAD` — PASS.

Not run: full suite, browser/e2e, live-socket tests, or a physical video render. Those are outside this non-heavy source review and remain central/orchestrator evidence.

The first SSR probe attempt omitted the repository's extensionless-import loader and failed during module resolution; the same probe rerun with `--import ./typescript/tests/register-extensionless.mjs` passed. This was test setup only, not a source failure.

## Blockers and next step

No source blocker found. Before publication, record the independent approval alongside the orchestrator's package version/publication decision; this review intentionally does not choose a version.
