# App render/download public12 source cohort

Status: source-only candidate; held for the manager-owned current Agent/Runtime
tuple and central browser gate. This document records lineage and local evidence;
it is not a release or parity qualification.

## Exact allowlist and lineage

Base: `tl/app-m3-public12-es2020-guard-fix6b22b03c3`, `6b22b03c3`.

The seven reviewed product/test paths are the byte-identical blobs from both
`f08c3b976` (`tl/app-m3-render-current-safety-refresh-r1`) and `320784f82`
(`tl/app-m3-render-standard-deps-requalify`):

- `src/tools/video-editor/components/TimelineRenderControls.test.tsx`
- `src/tools/video-editor/components/TimelineRenderControls.tsx`
- `src/tools/video-editor/hooks/timelineStore.ts`
- `src/tools/video-editor/hooks/useRenderState.test.tsx`
- `src/tools/video-editor/hooks/useRenderState.ts`
- `src/tools/video-editor/hooks/useTimelineState.ts`
- `src/tools/video-editor/hooks/useTimelineState.types.ts`

The existing 320784 viewing-parity closure was copied without product changes:
`playwright.viewing-parity.config.ts`,
`tests/e2e/timeline/player-export-frame-parity.spec.ts`, and all files under
`tests/e2e/timeline/viewing-parity/` from `admission`, `authority`, `bootstrap`,
`compare`, `diagnostics`, `download`, `fixture`, `frames`, `harness`, `media`,
and `tsconfig` (the added `directframes.test.ts` is the capture-only test from
the approved patch below).

Finally, only
`handoff-vw-m3-capture-current-port-capture-fix.patch` was applied: it updates
`viewing-parity/frames.ts` to dismiss the completed-render dialog and wait for
`[data-dialog-backdrop]` before Player capture, and adds
`viewing-parity/directframes.test.ts`. No old 7989 ancestry or source tree was
imported. Current public12 track-label removals in `timelineStore.ts` and
`useTimelineState*` were retained while adding the reviewed download callback
wiring.

No root, lock, theme, default, endpoint, renderer, authority, or production
writer-retirement files were changed by this cohort.

## Public12 dependency/import guard

Tests used the read-only dependency tree `/tmp/app-coherent-deps12/node_modules`
by temporarily repointing only this worktree's ignored `node_modules` symlink;
the original symlink was restored after each run. The shared dependency tree was
not modified.

Observed versions: Composition `0.0.12`, React/React DOM `18.3.1`, Remotion,
`@remotion/media`, `@remotion/player`, and `@remotion/layout-utils` `4.0.509`,
Vitest `4.1.5`, and TypeScript `5.9.3`. Root, `/evaluation`, and `/theme-api`
imports resolved under `/tmp/app-coherent-deps12/node_modules`; the package
contains 77 regular files. Root/evaluation exports and `DEFAULT_THEME` were
imported successfully. The default was the navy `banodoco-default` theme
(`bg #050814`, `fg #FAFAFA`, accent `#67E8F9`, Arial/Arial/monospace,
1920x1080 at 30fps).

All declared Composition peer checks passed for React, React DOM, Remotion,
`@remotion/media`, and `@remotion/layout-utils`. `@remotion/player` was
installed at `4.0.509` but is not declared by the observed Composition
`0.0.12` manifest; this is recorded as a tuple detail, not changed here.

## Local evidence

All commands were source-only, max one worker, with no install, build, browser,
socket, full suite, or TypeScript run:

- direct render lane: **95 passed**, 2 files;
- render route/planner/refusal lane: **233 passed**, 5 files;
- state/store/preview/command/provider neighbors: **357 passed**, 13 files;
- render security/bounds neighbors: **148 passed**, 7 files;
- viewing-parity pure helper/controller tests: **9 passed**, 9 Node test files;
- `config/vite/timelineCompositionPackage.test.mjs`: **1 passed**;
- scoped ESLint, `git diff --check`, and forbidden-marker scan: **pass**.

The direct and Vitest commands used `node node_modules/vitest/vitest.mjs run
--config config/testing/vitest.config.ts --maxWorkers=1` followed by their
listed paths. The parity command was `node --import tsx --test` followed by the
nine `tests/e2e/timeline/viewing-parity/*.test.ts` files. The package guard was
`node --test config/vite/timelineCompositionPackage.test.mjs`.

## Unresolved tuple and handoff

The actual Agent12 and Runtime matched pins required by the owner gate were not
published for this source-only worker. Therefore the current tuple is unresolved:
App source `6b22b03c3` plus this uncommitted candidate, public Composition
`0.0.12` from the private dependency tree, Agent pin **unpublished**, Runtime
pin **unpublished**. No current-tuple pack-host run, native MP4 download,
codec/playback check, frame/audio parity, or planted mismatch check is claimed.
The manager must re-freeze the complete tuple and run the one bounded central
normal-render gate after headless safety closure. The candidate remains HELD.
