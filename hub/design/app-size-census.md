# App timeline-core size census

Read-only refresh 2026-10-21. Baseline is `origin/main` at `860d43b331fb4422b16bc0dbd7b08666a0c766a0`; current is `tl/integration`/`HEAD` at `b1b27fa9cc77c517b82aacc560852d16fa7bfe44`.

| same explicit authored path set | files | physical | nonblank |
|---|---:|---:|---:|
| baseline `origin/main` | 198 | 67,688 | 62,760 |
| current integration | 208 | 72,498 | 67,428 |
| current − baseline | +10 | +4,810 | +4,668 |

Boundary: App-owned Timeline Read/See/Edit commands, projections, timing/data adapters, editing UI/writers, popup/placement producers, commit/capture/outbox/history, and SDK timeline; mixed Runtime files use only named timeline/commit/media symbols. Viewing-owned PreviewPanel/compositions/render is separate (baseline 32/10,078/9,254; current 31/10,370/9,546; delta −1/+292/+292).

Excluded: tests/helpers/fixtures, generated clients/contract data/registries, vendored source/defaults, archives/binaries/lockfiles/build output, untouched generic Main infrastructure, and retained generic Supabase/completion code. Hand-authored timeline data adapters remain in scope.

Relevant deletions: current removed `TimelineModeSwitcher.tsx` (scoped path set), `TimelineMobileInspectorDialog.tsx` (already adjacent-shell excluded), `DebugTrack.tsx`, `audioFade.ts`, `renderPipeline.ts`, fallback registries, and vendored Composition/Agent/default copies; excluded deletion debt is not credited separately.

Method/reproduction: `git rev-parse origin/main HEAD`; enumerate the fixed path manifest from the prior census/review, read each blob with `git show SHA:path`, count `splitlines()` and nonblank `strip()` lines, union only the recorded mixed Runtime symbol ranges, and run `git diff --name-status origin/main HEAD` for deletions. No 20–26k compliance claim; this is a rough-guide measurement, not a gate.
