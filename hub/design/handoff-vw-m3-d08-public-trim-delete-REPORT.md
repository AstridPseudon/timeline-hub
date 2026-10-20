# D08 public trim deletion — complete; App owner gate remains

Base: `0ea988bdd2907c876b82fd2620820e3fb6d6ea84` (held App root 0ea).

Only two tracked files change: the authorized config-utils trim export and its direct tests. The 16-line private implementation becomes one compatibility re-export of the existing public12 `computeMediaTrim`. Existing visual/audio callers need no edits. Product delta: -15 lines. Tests add 28 lines (20 parameterized fixed expectations). All other config-utils/domain/producer behavior stays intact. No package/pin, Root, runtime, renderConfig, or policy change.

Decisions: retain the old name because VisualClip, AudioTrack and time-grid conformance still import it; a direct re-export preserves the callable contract without an adapter. No behavior gap found. Public12 contains the approved 0.0.11 trim export with the same finite checks and conversion. Invalid fps retains the existing arithmetic result; the tests do not introduce fps validation. The 11:59 MAIN golden remains opacity 0.5 for hold5/fade1/cap4; this trim-only change does not touch that path.

## Exact validation

Cwd for all commands: `/home/user/work/wt/vw-m3-d08-public-trim-delete`. Node v22.22.0, fresh installed Vitest v4.1.5. Tests used the fresh READY install READ-ONLY via this worker's REAL node_modules root/scope directories and leaf package symlinks, with private cacheDir `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d08-public-trim-delete/vite-cache` and `--no-cache`.

1. Before deleting the formula, the original helper and actual public12 both satisfy all 20 added literal vectors, alongside original config-utils positives:
```sh
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d08-public-trim-delete/vitest.config.mts --configLoader bundle --no-cache src/tools/video-editor/lib/config-utils.test.ts
```
Result: exit 0; **1 file / 43 tests passed** (1.18 s).

2. After the re-export:
```sh
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d08-public-trim-delete/vitest.config.mts --configLoader bundle --no-cache src/tools/video-editor/lib/config-utils.test.ts src/tools/video-editor/lib/time-grid-conformance.test.ts src/tools/video-editor/compositions/VisualClip.test.tsx src/tools/video-editor/compositions/VisualClip.evaluation.test.tsx src/tools/video-editor/compositions/AudioTrack.test.tsx src/tools/video-editor/compositions/playerEvaluation.test.ts src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx
```
Result: exit 0; **7 files / 211 tests passed** (10.66 s), zero skips/xfails. Original tests/expectations are unchanged. Native media endpoints use the existing test mocks; this is clock/prop evidence, not decoded pixels or real playback.

3. Lint:
```sh
node node_modules/eslint/bin/eslint.js src/tools/video-editor/lib/config-utils.ts src/tools/video-editor/lib/config-utils.test.ts --max-warnings 0
```
Result: exit 0, no diagnostics.

4. Narrow type compatibility check, importing actual App TimelineClip and public12 declarations, verifies assignability in BOTH directions with the original signature:
```sh
node node_modules/typescript/bin/tsc -p /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d08-public-trim-delete/tsconfig.trim.json
```
Result: exit 0, no diagnostics. This is not a whole-App typecheck.

5. Dependency and diff checks:
```sh
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d08-public-trim-delete/audit.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d08-public-trim-delete/graph-before.json
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d08-public-trim-delete/audit.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d08-public-trim-delete/graph-after.json
cmp /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d08-public-trim-delete/graph-before.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d08-public-trim-delete/graph-after.json
git diff --check
```
Result: all exit 0. Actual installed public12 matches **all 77 regular members** of frozen archive SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. Whole borrowed node_modules pre/post content/type/size/mtime digest unchanged: `7f7c7f6c3a6a68cf50de63392f107dab4f07a05014b5cdd81f927d7280fc7e19` (35,544 entries). No shared dependency/cache writes. No polluted App or scene-host graph was used as a dependency.

The first attempted config load with `--configLoader runner` stopped before tests because the repository config uses `__dirname`. Switching only the PRIVATE invocation to `--configLoader bundle` preserved the original config/plugins/setup and placed transient config output in the owned node_modules root. That startup attempt is not a test pass. No source workaround was added.

## Handoff and limits

Exact patch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d08-public-trim-delete-exact.patch`
Replacement map: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d08-public-trim-delete-replacement-map.txt`
File list: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d08-public-trim-delete-filelist.txt`
Logs, private config/probe, and graph checks are adjacent flat handoffs under the same prefix.

No full suite, whole-App typecheck, install, network, browser, render, socket, or environment/parity qualification was attempted. Nothing is blocked within this bounded task. App owner should gate/port ONLY this two-file patch onto its current root; wider D08 remains open. No git mutation was performed. The harness receives commit-msg and DONE; it owns the commit.
