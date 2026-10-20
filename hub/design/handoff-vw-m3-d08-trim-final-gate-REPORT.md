# D08 exact trim deletion — independent final gate

Verdict: **APPROVE the exact two-file cut for App owner port.**

Candidate: `3812ff4c8c8fb9ccc2546f8d575e96a5a3493ac9` (`3812ff4` prefix), parent/base `0ea988bdd2907c876b82fd2620820e3fb6d6ea84`.

The candidate diff is exactly:

- `src/tools/video-editor/lib/config-utils.ts`: delete the private 16-line `getSanitizedMediaTrimProps` formula and re-export `computeMediaTrim` under the compatibility name.
- `src/tools/video-editor/lib/config-utils.test.ts`: add the 20 edge vectors and public-vs-compatibility assertions.

No package/pin, Root/bootstrap, runtime, `renderConfig`, or audio-policy file changes are present. Existing callers remain unchanged: `VisualClip.tsx:317`, `AudioTrack.tsx:295`, and time-grid conformance callers use the old compatibility name. The public declaration accepts `Partial<Pick<TimelineClip, 'from' | 'to'>>` and returns the same `{trimBefore, trimAfter?}` shape, which is assignable to the former App signature in the independent type probe.

## Independent evidence

- Direct before-vs-public12 runtime probe: **20/20 vectors passed**, including omitted `from`/`to`, half/sub-frame windows, fractional fps, negative/nonfinite trim values, equal/reversed endpoints, zero/negative/NaN/infinite fps, and omission of `trimAfter`.
- Clean private public12 graph targeted run, with this worktree's own `node_modules` leaf overlay and private Vitest cache: **7 files / 211 tests passed**, zero skips/xfails, 10.14s. Suites covered config utils, time-grid conformance, VisualClip, VisualClip evaluation, AudioTrack, player evaluation, and native media conformance (visual/video/audio clocks and props).
- ESLint on both changed files with `--max-warnings 0`: **exit 0**.
- Type compatibility probe against the actual public12 declaration and App `TimelineClip`: **exit 0**.
- Public12 package verification: version `0.0.12`; artifact SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; all **77/77** regular package members byte-match the frozen tarball.
- `git diff --check`: **exit 0**; candidate name-status remains exactly the two files above.

The shared App `node_modules` was not used as evidence because it currently contains Composition `0.0.8`. The qualified private clean graph at `.../vw-m3-app-private12-clean-install/clean-project/node_modules` was used read-only. The worker restored its own `node_modules` symlink to `/home/user/work/app/node_modules`; no shared dependency or cache writes were made.

## Commands and limits

Successful commands:

```sh
git rev-parse HEAD
git rev-parse 0ea988bdd2907c876b82fd2620820e3fb6d6ea84
git diff --name-status 0ea988bdd2907c876b82fd2620820e3fb6d6ea84 3812ff4c8c8fb9ccc2546f8d575e96a5a3493ac9
node --input-type=module  # direct 20-vector before-vs-public12 probe
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d08-trim-final-gate/vitest.clean.config.mts --configLoader bundle --no-cache src/tools/video-editor/lib/config-utils.test.ts src/tools/video-editor/lib/time-grid-conformance.test.ts src/tools/video-editor/compositions/VisualClip.test.tsx src/tools/video-editor/compositions/VisualClip.evaluation.test.tsx src/tools/video-editor/compositions/AudioTrack.test.tsx src/tools/video-editor/compositions/playerEvaluation.test.ts src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx
node node_modules/eslint/bin/eslint.js src/tools/video-editor/lib/config-utils.ts src/tools/video-editor/lib/config-utils.test.ts --max-warnings 0
node node_modules/typescript/bin/tsc -p /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d08-trim-final-gate/tsconfig.clean.trim.json
git diff --check
```

No full, browser, render, live-socket, network, install, or whole-App typecheck was run. This gate makes no Runtime/parity claim. App owner should port only these two files and perform normal integration review/merge.
