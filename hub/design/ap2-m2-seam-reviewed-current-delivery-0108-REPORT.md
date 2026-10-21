# Dormant visual seam project-data delivery

## Result

The independently approved dormant App packet is preserved exactly as
candidate commit `bce8bab72d03e12d2cbfb055d76a5ea04f474f68`, tree
`f9bc16ce6b08c830cac814feee7b20e9d659fd6e`.

Its exact two-file delta is:

- `src/tools/video-editor/commands/visualSeamProjectDataMember.ts`
- `src/tools/video-editor/commands/visualSeamProjectDataMember.test.ts`

The files are byte-identical to the reviewed candidate. Their blob hashes
are `828bbb78b9684e5f0ff0d2d0e26dfcd2cca70ea9` and
`0f0c05f98edcfe95c971091835c66fceb2854596`, respectively.

The builder remains dormant and uses the existing private392
`project-data.write` carrier at
`parent.config.app.visualSeamContract[key]`. It excludes derived `report`
from authored writes and retains the reviewed opaque-report, order, absence,
old-value guard, atomic refusal, and replay assertions. No current-row,
shared source, `useTimelineState`, `useTimelineOps`, provider, schema, pin,
or wire surface was changed.

## HOME and merge-forward

Latest HOME was `813a85106ecb4abbaf224081abe6c33b8dab0df7`, tree
`2a19a78bb1bdfb3fd779f568a1b513b094318982`. The two approved files are not
present in that HOME tree. The prescribed command was attempted:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/merge-forward ap2-m2-seam-reviewed-current-delivery-0108 tl/integration
```

It failed before changing the worktree because Git could not create
`ORIG_HEAD.lock` in the read-only worktree metadata (`rc=128`). There were no
conflicts and no Git mutation. HOME automatic merge handling is required.

## Product callers

There are no product callers. Search found references only within the two
packet files themselves (implementation and tests); no UI, state, ops,
provider, or live writer imports the builder.

## Verification

- `node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/visualSeamProjectDataMember.test.ts src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/hooks/useTimelineState.visual-seam.test.ts` — **PASS**, 3 files, 16 tests.
- `node_modules/.bin/eslint src/tools/video-editor/commands/visualSeamProjectDataMember.ts src/tools/video-editor/commands/visualSeamProjectDataMember.test.ts --ext ts --max-warnings 0` — **PASS**.
- `node_modules/.bin/tsc --noEmit --pretty false` — **PASS**.
- `git diff --check HEAD^ HEAD` — **PASS**.
- Candidate delta inspection — **PASS**, exactly two added files, 207 lines; no extra worktree changes remain.
- The retained private392 real-member proof (`PASS1`) was not rerun, as directed. Prior review evidence remains 16 App tests and 17 Agent tests; the separate real proof remains the recorded one selected passing case.

No full suite, browser, live socket, activation, pin, schema generation, or
new real proof was run.
