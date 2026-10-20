# App parent-delete routing final review

## Verdict

**APPROVE** the corrected source candidate for the bounded parent-owned delete
route. This is a read-only review; no product files or ledger rows were
changed. The candidate is commit `29564148789ef00a8c28ea44d7ba87faf19d1602`
with tree `7b86b7aff415007f679c29ffa71a1d16f8551e24`, directly on
`4a782eb03caba7e4df1225f054d8091911354848`.

## Routing review

The prior regression was real. The canonical shot projection constructs a
display ID such as `occ-1:child`, but separately records the authoritative
identity on the projected clip:

- `ownerRef: occurrence:occ-1`
- `clipRef: occurrence:occ-1/clip:child`
- `rawClipId: child`

`pinnedShotGroups` is a separate grouping representation; an occurrence child
does not need to be a pinned-group member. Therefore the old single-clip,
`!isPinnedGroupMember` condition could send an ungrouped occurrence display ID
to parent-only `clip.delete` capture, which correctly rejects the occurrence
target and prevented its existing writer from running.

The corrected shared predicate is
`src/tools/video-editor/commands/clipDeleteGesture.ts:14-34`:

1. reject targets listed in `config.pinnedShotGroups`;
2. require one existing resolved display row;
3. use the existing canonical `ownerRef` and `clipRef` bindings, rejecting
   either one when it identifies an `occurrence:` owner.

It does not parse or infer ownership from the display ID. Parent rows without
projected occurrence metadata retain the existing parent capture path. No
post-capture or post-submit fallback was added.

The same predicate is used by all three delete ingresses:

- `useClipDeletion` (`useClipDeletion.ts:38-47`): occurrence/group targets
  retain `applyRowsEdit` and parent targets alone use native capture;
- `useTimelineOps` (`useTimelineOps.ts:291-301`): occurrence targets use the
  existing `commitData` path, while missing-target behavior keeps the prior
  capture identity guard;
- public `createTimelineCommands().deleteClip`
  (`useTimelineCommandsService.ts:857-864`): occurrence/group targets retain
  `applyValidatedMutation`.

The original group-delete positive at
`src/tools/video-editor/hooks/useClipEditing.test.ts:261` is byte-identical
to `4a782eb03` and its assertion passed. The original browser success and
same-property conflict cases are also byte-identical to `4a782eb03`; source
discovery still lists exactly the two parent-delete cases. No group, multi,
occurrence, or prepared-media native qualification is claimed.

## Verification

The affected 48-control cohort was rerun from an archived copy of this exact
tree using an own private12 dependency overlay and own cache. The two private
Vitest binaries matched the verified private12 source hash
`39db22f579acf5639bbb17a261408debbde03f4692c0c439e77e7f13aeba74d6`.
The runner preload was the existing `__dirname` compatibility preload; no
shared `.vite` or `.vite-temp` directory was used.

```sh
cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-routing-final-review/notes/private12-source
VITEST_CACHE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-routing-final-review/notes/private12-cache \
  node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-routing-final-review/notes/private12-runner.cjs \
  node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/hooks/useTimelineOps.clipDelete.test.ts \
  src/tools/video-editor/commands/clipDeleteCapture.test.ts
# 2 files passed; 48 tests passed; exit 0.
```

The exact native S2 parent-delete golden is included in
`clipDeleteCapture.test.ts`; its fixture is SHA-256
`091bc1c7fa9c57583dde8fcc6d6af9226513bf4f214369ef0892cc1db492f0aa` and the
test passed unchanged.

```sh
VITEST_CACHE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-routing-final-review/notes/private12-cache \
  node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-routing-final-review/notes/private12-runner.cjs \
  node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/hooks/useClipEditing.test.ts \
  -t 'allows explicit full-group deletion through the shot menu path'
# 1 passed, 20 skipped; exit 0.
```

```sh
node node_modules/eslint/bin/eslint.js \
  src/tools/video-editor/commands/clipDeleteGesture.ts \
  src/tools/video-editor/hooks/clip-editing/useClipDeletion.ts \
  src/tools/video-editor/hooks/useTimelineCommandsService.ts \
  src/tools/video-editor/hooks/useTimelineOps.ts \
  src/tools/video-editor/hooks/useTimelineOps.clipDelete.test.ts \
  --max-warnings 0
# exit 0, no diagnostics.

node node_modules/playwright/cli.js test --config playwright.clip-delete.config.ts --list
# exactly 2 tests in 1 file; discovery only, no browser execution.

git diff --check 4a782eb03..HEAD
# exit 0.
git diff --exit-code 4a782eb03..HEAD -- tests/e2e/local/clip-delete-command.spec.ts
# exit 0: original real success/conflict source unchanged.
git diff --exit-code 4a782eb03..HEAD -- src/tools/video-editor/hooks/useClipEditing.test.ts
# exit 0: group-261 source unchanged.
```

## Deferred central two-case command

Do not schedule or run this from the worker. After the root gate, execute it
through the central browser service from the clean corrected App checkout. It
uses the current Agent `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, Runtime and
producer `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, client13/public12, and a
short TMPDIR. The cache identity was computed by the candidate launcher and
binds this exact App tree plus launcher/helper bytes.

```sh
cd /home/user/work/wt/app-m2-parent-delete-routing-final-review
env -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST \
  NODE_PATH=/tmp/app-coherent-deps12/node_modules \
  TIMELINE_CURRENT013_SHORT_TMPDIR=/tmp/tl13-e2e-7b86 \
  TMPDIR=/tmp/tl13-e2e-7b86 \
  TIMELINE_CURRENT013_RUN=1 \
  TIMELINE_CURRENT013_APP_TREE=7b86b7aff415007f679c29ffa71a1d16f8551e24 \
  TIMELINE_CURRENT013_AGENT_SHA=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 \
  TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
  TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source \
  ASTRID_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  TIMELINE_BUNDLE_AGENT_HEAD=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 \
  TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
  TIMELINE_CURRENT013_CACHE_ID=parent-delete-tree7b86b7aff415007f679c29ffa71a1d16f8551e24-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-client13-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-runnerda7944483b16fbd6f880a4958c4761eb62b17dae894b63ee5aec8cf3c3088abf-helper82ff12281994e3bce006d643fc2b090ef356784c6854b959e82c87caf3347901 \
  npm_config_cache=/tmp/tl13-e2e-7b86/npm-cache \
  PWTEST_CACHE_DIR=/tmp/tl13-e2e-7b86/pw-cache \
  PLAYWRIGHT_OUTPUT_DIR=/tmp/tl13-e2e-7b86/output \
  PYTHONDONTWRITEBYTECODE=1 \
  node scripts/testing/current013-parent-delete.mjs
```

That launcher delegates only the two `clip-delete-command.spec.ts` cases:
lost ACK/reload/restart/exact retry/inverse restoration and held-request
same-property conflict/draft retention. This command is prepared evidence,
not a browser result. No full suite, project typecheck, build, browser,
localhost/socket, or install was run in this review.
