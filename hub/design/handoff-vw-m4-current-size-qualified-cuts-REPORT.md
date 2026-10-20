# Viewing M4 current-size / qualified-cuts handoff

## Result

One safe Composition cleanup is implemented on this worker branch: remove the
private `lib/fade.ts` hook wrapper and call the already-used pure
`fadeMultiplier` directly from `VisualClip`. No Agent or App files were
modified. One additional App fallback-only unit is statically qualified for
the App owner; it is not claimed merged here. D09 remains held.

## Exact tuple and counting

Read-only source heads: Composition `ff0536bb53d84db5008b859be304b932b1dd5252`,
Agent `33b0a8385f2cd184f0e79544f78678bc0dbee0d7`, and App
`5912bfc3284da03112ef6c235447cfbeffb678bd`. Composition has the local
uncommitted cleanup described above; the SHA is the source base, not a merged
claim.

Counts are nonblank physical lines. Comments and JSON/YAML metadata count;
tests, fixtures, `dist`, locks, tarballs, vendored trees, and documentation
are excluded from authored-canonical counts. Generated Composition registries
and curves are reported separately, not counted twice. App active roots exclude
tests and fallback-only files. Agent `packs/rendering` excludes docs, skill
templates, fonts, inspector assets, README/STAGE files; its visualize row is a
subset and must not be added to the pack total.

| area | exact files | nonblank lines | status / debt |
|---|---:|---:|---|
| Composition 0.0.11 authored `typescript/src` | 78 | 4,088 | current canonical source after this worker cleanup |
| Composition generated source + timer declaration | 7 | 405 | separately reported; not authored-canonical savings |
| Agent `astrid/packs/rendering` | 150 | 54,073 | current active viewing/rendering area; includes visualize |
| Agent `timeline_visualize` subset | 57 | 25,349 | current; keep pixel lane and `_timing_evaluators` policy |
| Agent `remotion/src` | 13 | 1,700 | current host source, not a Composition duplicate |
| Agent `astrid/core/timeline/onscreen.py` | 1 | 375 | current private evaluator; D09 held |
| App active PreviewPanel + compositions + render roots | 30 | 7,164 | current integration after D03/new integration cuts |
| App fallback-only modules | 4 | 229 | qualified next App deletion; no callers found |
| App live vendor Composition source | 21 | 1,504 | duplicate, separately counted; package pin/adoption held |

The standalone area totals overlap and are not a consolidated target sum. The
PLAN 20–26k target applies after coordinated adoption and approved deletions,
not by relabelling active Agent rendering or App preview behavior dead.

Binary/generated debt is also separate: App has
`vendor/artifacts/banodoco-timeline-composition-0.0.8.tgz` (50,664 bytes),
and Agent has `remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz`
(58,008 bytes). Neither is counted as authored product lines.

## Qualified deletion units

### Q1 — Composition private fade wrapper — implemented here

Files: delete `typescript/src/lib/fade.ts`; update
`typescript/src/VisualClip.tsx` to import `useCurrentFrame` and call the
existing `fadeMultiplier` from `typescript/src/lib/clip-look.ts` directly.

Proof: repository-wide caller search found only the old `VisualClip` import and
the historical comment in `clip-look.ts`; no public export, serialization,
dynamic registration, or consumer path names `lib/fade`. The replacement is
the identical call `fadeMultiplier(clip, useCurrentFrame(), fps)`.

Replacing tests: `typescript/tests/transition-policy.test.ts` (real
`VisualClip` rendering, including default dip and incoming policy) and
`typescript/tests/registries.test.ts` (rendered registry/component neighbors).
Exact run and result:

```text
npm run build:test
node --import tsx --test \
  typescript/test-dist/tests/transition-policy.test.js \
  typescript/test-dist/tests/registries.test.js
2 passed, 0 failed
git diff --check: passed
```

No build output remains in the worktree. This change is unmerged until the
harness commits it.

### Q2 — App fallback-only Composition shims — qualified for App owner

Files (current App `5912bfc32`):

```text
src/tools/video-editor/compositions/fallback/registry.generated.tsx  (51)
src/tools/video-editor/compositions/fallback/theme-api.tsx            (85)
src/tools/video-editor/lib/theme-api.fallback.tsx                    (90)
src/tools/video-editor/lib/registry.generated.fallback.ts            (3)
```

Exact `git grep` over the current App tree found no import/path reference to
any of these four files outside the first file's self-import. Active code uses
the installed package exports through `sequences/registry.ts` and
`TimelineRenderer`; App package adoption and the live vendor source remain
separate. No App file was changed by this worker.

Replacing tests for the App owner to run after deletion:

```text
npx vitest run --config config/testing/vitest.config.ts \
  src/tools/video-editor/compositions/TimelineRenderer.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.dynamic.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.public-host.qualification.test.tsx \
  src/tools/video-editor/compositions/vendoredTimelineCompositionAliases.test.ts
```

Named coverage includes installed registry dispatch, unknown placeholders,
dynamic registry refusal, registered-sequence rendering/default theme, public
host owner resolution, and vendor-alias isolation. Dependencies: none for the
four unreferenced files; retain the package pin, active `installed-themes.ts`,
and all vendor alias tests.

## Held / not qualified

- **D09 Agent private evaluator deletion:** current Agent still has
  `astrid/core/timeline/onscreen.py` (375 lines). The held proposal is based on
  Agent `4a75f68f32049a69fd86135c645fa64c51175c14`, source
  `09cfd10a44b17a24d6f77ef6b8f41cce9cd0db1e`, and its 18-file list is recorded
  in `handoff-vw-m3-d09-current-deletion-unit-FILELIST.md`. It deletes a
  452-line held-tree `onscreen.py`, but is not a current-tree deletion. Do not
  claim it staged or merged. Required blockers remain exact source/asset/theme/
  occurrence joins, label/capture forwarding, real component positives for
  crop/alpha/selected assets, paired public package adoption, and MAIN 0.0.6
  intended-DIP pixel proof. Keep `_timing_evaluators`, fast-lane/sweep pixel
  verification, and existing behavior tests.
- **D10 vendored Composition copies:** App's 1,504-line live vendor source and
  binary artifacts are not safe cuts until the coordinated App/Agent package
  pin/root/vendor adoption gate passes. Do not count this duplicate as authored
  canonical Composition twice.
- **D08, VW-AUDIO-STEP, mouth/crop descendants:** parity, trusted source joins,
  real positives, or both-consumer proofs remain open. No quota-driven cuts.
- D12 stale `dist`/build masking is already deleted; do not recount it.

No full suite, browser, live socket, network, install, or central test service
run was requested. The prior App owned-dead cleanup was not repeated.
