# App label reconciliation final review (r2)

Date: 2026-10-20 UTC

## Verdict

**APPROVE, bounded to the reviewed label-reconciliation candidate and exact
source tree below.** The two prior independent-review holds are fixed. No new
label, identity, timing, lifecycle, or assertion-integrity finding was found.

This is not approval of a latest full App qualification: project TypeScript,
full, browser/live-socket, build, and install checks were not run as required
by the brief.

## Source identity and cumulative scope

- Reviewed `HEAD`: `5404ca470eed1e8532fdcdeeb3b29c5da9b446e0`
- Reviewed tree: `6348970c380ec63ab41404b57de188f126483cbf`
- Prior candidate: `8a79a7bb9416302f36b6a8c104444ff609dff5e0`
- Integration reference: `0d5009e18bee8e29f894dabf5db501a0fcea750f`
- `git merge-base HEAD 0d5009...`: `d12d0909746c552dee6dac7b5d8459e8e1f27679`
- Cumulative `git diff --binary 0d5009...HEAD` SHA-256:
  `c52b13fbd07402e9e1abceef2c32c9d1ea51199e97d2176c0505ab0392ad91e5`
- Final hold-fix commit diff SHA-256:
  `8a63fdbc9c49c7343f3314f25b8dcce8d0ad3d6012765a5464b164bfe3cf39a4`

The final hold-fix commit changes only the raw `clips` carrier type and the
two lifecycle expected references. The review worker made no App product or
test changes; the worktree was clean after verification. App-owned move,
label, `None`, delete, name, automatic, and App2 port sections were not
modified by this review. Integration application of the divergent cumulative
branch is outside this read-only review and remains unverified.

## Prior holds confirmed fixed

1. `timeline-data.ts:279` now declares `extras` as an existing
   `Pick<TimelineConfig, 'clips' | ...>`, truthfully carrying the raw authored
   clips used at `rowsToConfig`.
2. The lifecycle acknowledgement assertion now uses the assembled input
   `savingEdit.resolvedConfig` (`...lifecycle.test.tsx:174`), and the
   independent canonical-read assertion uses `initial.resolvedConfig`
   (`...lifecycle.test.tsx:296`). Neither captures `player.config` as its
   expected oracle.

`rowsToConfig` preserves an existing clip's authored label by own-property
presence, including runtime absent/null/opaque values; metadata-derived labels
remain display-only. New clips may use supplied metadata. Production row-edit
funnels pass the raw current config carrier. `assembleTimelineData` continues
to derive readable MAIN names separately into `resolvedConfig` and row
metadata. The no-source-track output projection continues to return the exact
input config reference; source-track filtering remains unchanged.

## Twelve expectation mappings audited

All twelve original failure cases remain one-for-one, with no skip, `fails`,
deleted case, field whitelist, or weakened behavior assertion:

| Case | Truthful expected input/reference | Preserved behavior coverage |
| --- | --- | --- |
| save 1 | exact assembled display projection | raw `data.config` identity |
| save 2 | exact unprojected resolved-input signature | display projection differs from identity bytes |
| save 3 | exact repaired resolved-input oracle | pinned-group order and geometry |
| save 4 | unchanged inverse stable-signature expectation | raw absent-label round trip |
| lifecycle 1 | `localEdit`, `savingEdit`, `acceptedClosure`.resolvedConfig | deferred ACK, asset entry, registry identity, labels |
| lifecycle 2 | `afterA` / `afterC`.resolvedConfig | original base-R, head sequencing, observed C |
| lifecycle 3 | `initial` / `next`.resolvedConfig | 149ms/1ms timing boundary |
| lifecycle 4 | exact initial assembled input | metadata-only certification, C notice, clear-only-target |
| lifecycle 5 | `initial.resolvedConfig` | independent canonical-read failure/recovery |
| lifecycle 6 | `localB.resolvedConfig` | paused coalescing and superseded-A absence |
| lifecycle 7 | `initial` / `localB`.resolvedConfig | playing coalescing and superseded-A absence |
| lifecycle 8 | `acceptedPending.resolvedConfig` | scope remount, committed-A label, zero timers |

The original opaque, absent, readable-name, timing, head, race, late-ACK,
draft, unavailable-target, and metadata-only assertions remain present.

## Verification

Approved private13 graph, checked by realpath before the run:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/full-main574-public13-8bd8f741/private13/node_modules`

It resolved separately from `/home/user/work/app/node_modules` and provided
Composition 0.0.13, React 18.3.1, Remotion 4.0.509, Vitest 4.1.5, and Vite
5.4.21. The worktree-local module link was restored to the shared install
after the run; no shared files were changed.

Exact focused command (with private TMPDIR, snapshot preload, runner loader,
no cache, one worker):

```sh
TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-label-final-fix-review-r2/runs/private13-verify/tmp-cohort \
NODE_OPTIONS="--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs" \
node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/full-main574-public13-8bd8f741/private13/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/timeline-save-utils.test.ts \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx \
  src/tools/video-editor/lib/timeline-data.test.ts \
  src/tools/video-editor/data/timelineOutputProjection.test.ts
```

Result: **4 files passed, 57 tests passed, 0 failed**. `git diff --check`
passed and the worktree was clean afterward.

## Limits

Not run: project TypeScript, full suite, browser/e2e, localhost/live sockets,
build, install, or any shared dependency/cache mutation. This review does not
claim latest full-suite green or certify the merge of the candidate onto the
`0d5009` integration tip.
