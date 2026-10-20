# App trim-helper deletion on current root

Status: bounded candidate complete; ledger update remains a proposal until integration. No settled PLAN decision changed.

## Exact source, base, and candidate identity

- Current base SHA: `3599fc49ad76dfdd7847ab4c813fc9317a0304eb`.
- Current base tree: `74130f681f6b0c87a7c61cb33d4ae6a092c03046`.
- Reviewed source SHA: `172b0cf874ca00bf6cb740c950e11a42be8efffd` (`tl/app-m3-d08-trim-current-root-port`).
- Reviewed source tree: `430f45bb5e9cae4acae4ba09879a05886372cb37`.
- Source parent `b1ef4b9b9` and current base have byte-identical target files; no target-file drift was found.
- Candidate worktree tree (computed from tracked HEAD entries plus the two worktree blobs): `9b3a0a813e9731a60493d94e66e63da7a68ce4d2`.
- Worktree patch SHA256 (`git diff --binary HEAD | sha256sum`): `cf07936d040b411e11b3f7d760e8184ad549cd4575ef9573b78f5921f3fef6f1`.
- The applied two-file diff is byte-identical to the reviewed source commit's parent-to-commit diff.

## Exact delta

Only these tracked paths change:

- `src/tools/video-editor/lib/config-utils.ts`
  - Deletes the private `getSanitizedMediaTrimProps` formula at old lines 43–58: 16 physical lines.
  - Adds one compatibility re-export at new line 43:
    `export { computeMediaTrim as getSanitizedMediaTrimProps } from '@banodoco/timeline-composition/evaluation';`
- `src/tools/video-editor/lib/config-utils.test.ts`
  - Adds the public evaluator import and the reviewed 20-vector compatibility assertion block: 28 lines.
  - All pre-existing assertions and inputs remain unchanged.

Net diff: 29 insertions, 16 deletions. No player, Root/root, audio, pin, package, lockfile, runtime, compiler, or call-site file changed. Existing `VisualClip`, `AudioTrack`, and time-grid callers still import the old helper name through the compatibility export.

## Public signature and behavior compatibility

The immutable public12 declaration is:

`computeMediaTrim(clip: Partial<Pick<TimelineClip, 'from' | 'to'>>, fps: number): { trimBefore: number; trimAfter?: number }`.

The narrow probe checked both assignments against the current App `TimelineClip`-based legacy signature (`Pick<TimelineClip, 'from' | 'to'>`), and passed with no diagnostics. The direct old-formula comparison covered all 20 reviewed inputs: omitted, half/sub-frame, rational FPS, negative/zero/nonfinite endpoints, equal/reversed endpoints, and zero/negative/nonfinite FPS. It passed 20/20, including omission of `trimAfter` and the legacy arithmetic for unusable FPS values.

## Immutable package identity

- App pin remains `vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz` in `package.json` and `package-lock.json`.
- Artifact SHA256: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.
- Archive regular-member count: 77/77.
- Tests used a private extraction of that artifact and an owned cache; the shared App node_modules was not used as package evidence (it resolves stale Composition `0.0.10`) and no shared dependency/cache file was modified.

## Tests and checks

Successful targeted command, run with the private12 overlay, private `TMPDIR`, `--configLoader bundle`, `--no-cache`, one worker, and no file parallelism:

```sh
TMPDIR="$OWN_CACHE" node node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader bundle --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/config-utils.test.ts \
  src/tools/video-editor/lib/time-grid-conformance.test.ts
```

Result: exit 0; 2 files / 62 tests passed. This is the nearest helper control and preserves the existing positive assertions; it does not repeat the reviewed 211-test graph.

The standalone inline Node probe comparing the deleted formula with private12 `computeMediaTrim` passed: 20/20 vectors, package version 0.0.12.

The narrow `tsc -p` signature probe passed with no diagnostics. `git diff --check` passed. Final scope audit found exactly the two paths above; `node_modules` was restored to the shared read-only symlink after testing.

Not run per brief: full/project typecheck, full suite, build, browser, render, socket/live service, install, or broad 211-test graph.

## Ledger update proposal (manager applies after integration)

Do not mark any ledger row `DELETED` in this worker. After the manager integrates this exact two-file delta and light-review confirms the integrated tree, update the existing D08 row in `scratchpad/orch/design/deletion-ledger.md` by appending evidence equivalent to:

> Current-root candidate `3599fc49` -> candidate tree `9b3a0a81`, exact two-file public trim-helper deletion: private 16-line formula removed from `config-utils.ts`, compatibility re-export retained, 20 old-vs-public12 vectors pass, nearest helper controls 62/62 pass, current public12 artifact SHA `0a7b6152` with 77/77 members. Existing VisualClip/AudioTrack/time-grid callers remain on the old public App name. This closes only the App trim duplicate subunit; D08 stays `in-progress` for the remaining evaluator/audio/cap work and is not marked deleted by this worker.

The ledger must retain the broader D08 row and its existing open claims; this proposal does not close D08 as a whole.
