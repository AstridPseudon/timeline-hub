# App Timeline-core size census

Read-only refresh 2026-10-21. Main860 baseline is `origin/main` at `860d43b331fb4422b16bc0dbd7b08666a0c766a0`; current integration is `tl/integration` at `d8d150b7a36e9b607685cbd04a1c9b08f32b1393`. The assigned worker snapshot is its parent `HEAD` `b030ca517c0867b6a56400e605d3b7f263d84a2a`; the intervening merge changes only excluded tests, so the authored counts are identical.

| reviewed authored Read/See/Edit footprint | present files | physical | nonblank |
|---|---:|---:|---:|
| baseline Main860 | 198 | 67,759 | 62,831 |
| current integration | 207 | 71,987 | 66,983 |
| current − baseline | +9 | +4,228 | +4,152 |

Boundary: App-owned Timeline commands, projections, timing/data adapters, editing UI/writers, popup/placement producers, commit/capture/outbox/history, SDK timeline, and the named Timeline slices of mixed Runtime files. The prior reviewed manifest’s 12 justified domain additions are included; seven layout/error shell files are separate (Main860 821/755, current 822/756 physical/nonblank). Viewing-owned PreviewPanel/compositions/render and shared render hooks remain separate (Main860 10,078/9,264; current 10,370/9,546; delta +292/+282).

Excluded: generated clients/contract data/registries, tests/helpers/fixtures, vendored source/defaults, archives/binaries/lockfiles/build output, untouched generic Main infrastructure, and retained generic Supabase/completion code. This is a bounded reviewed footprint, not a recursive dependency closure; `graphProjector.ts`, `patchPreview.ts`, `materialRuntime.ts`, `useAssetManagement.ts`, `useSwitchToFinalVideo.ts`, and `data-kinds/` remain to be classified before claiming a global App total.

Zero-legacy-writer target remains OPEN: D01/D02 and the existing fallback, popup, placement, ordinary-batch, bootstrap, and element-route ledger rows are not closed by size counting. Exact recorded physical deletions, kept outside the core total, include D03 Supabase canonical writers (29 production files, 7,914 lines), four fallback/generated registries (246), `createDefaultTimeline.ts` initializer helper (28), compiler-canary source plus private tests (2,171; 601 product/1,570 test), `DebugTrack.tsx` (59), `audioFade.ts` (66), dead `renderPipeline.ts` (177), private trim math (16), rate wrapper (5), duration implementation (6), and fallback render runtime (14). No deletion is inferred from these numbers.

Method/reproduction: use the prior census/review’s fixed path manifest and AST declaration ranges; `git rev-parse origin/main HEAD tl/integration`, read committed blobs with `git show SHA:path`, count `splitlines()` (blanks included) and `strip()` nonblank lines, union mixed Runtime symbols once, and inspect deletions with `git diff --name-status --diff-filter=D origin/main HEAD`. The PLAN’s 20–26k size target remains a rough guide, not a gate; no product rewrite, deletion, or compliance claim follows from this census.
