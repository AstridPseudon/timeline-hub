# App cap/current source composition

## Source identity

- Assigned cap source HEAD: `dca891972840f502c974fbf3c3b1d585855842c1`.
- Current-root merge parent: `ddd9e7824c7c0c08b1293132484f5ac52d1de3c3`.
- Three-way merge base: `c57dcc26162642f503532f143ceb96bb185273aa`.
- Clean merged source tree from `git merge-tree --messages ddd9e7824 dca891972`: `c404c633472c56413547e03f3378afafe4c61cf`.
- Harness commit/tree is pending; no commit, merge, rebase, checkout, push, or ref mutation was performed.

The worktree composition preserves the current shot-name9d9, seam6da report
preservation, App2 five-file typing repairs, None, Generic, Element, labels,
PCM, and MAINbebadd source. The reviewed cap unit's complete 30 paths are all
present. Three shared current/cap files were resolved by hunks:

```text
src/tools/video-editor/commands/commitSession.ts
src/tools/video-editor/hooks/useTimelineCommandSession.ts
src/tools/video-editor/hooks/useTimelineState.ts
```

No old whole-file overwrite was used. No new renderConfig/store/DTO/compiler/
editor behavior was added.

## Test evidence

The private runner used the approved public13 dependency overlay from
`app-m3-complete-stored-cap-producer-consumer-current-join/private13`, with
read-only dependency symlinks, `--configLoader=runner`, `--no-cache`, one
worker, no-file-parallelism, and an external cache directory.

Targeted command shape:

```text
env -u ASTRID_CHECKOUT TMPDIR=<worker-private-tmp> node --require <approved-dirname-preload.cjs> <private13>/node_modules/vitest/vitest.mjs run --config <worker>/vitest.private13.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism <21 cap/current/shot/None/seam/session test files>
```

Result: **21 files, 367 tests passed, exit 0**.

The producer-omission negative used the same private runner with the
`storedOccurrenceDurationMs` emission removed only in the transform plugin.
Result: **exit 1 as expected; both delivery tests failed with `expected 5 to
be 4`**. This negative remains evidence that the consumer does not invent the
derived cap.

Scoped ESLint (`--no-cache --max-warnings 0`) passed with exit 0. `git diff
--check` passed with exit 0.

One project typecheck was run under `/home/user/work/.app-tsc.lock` with
`NODE_OPTIONS=--max-old-space-size=4096`, using the private13 TypeScript binary.
It exited 2 with 10 diagnostics: four in the newly composed shot-name
capture source and six missing public13 Composition evaluation exports in
existing audio/config consumers. Those diagnostics are reported verbatim in
the worker report; this task did not redesign or weaken them.

## Review status

The derived-cap fallback peer review requested from Viewing remains **HOLD**.
This source composition does not claim that peer gate passed. No full suite,
browser, render, parity, install, or repeated full-706 run was performed.
