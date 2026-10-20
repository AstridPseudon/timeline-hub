# App project-data private subprocess parity repair

Date: 2026-10-20 UTC

## Result

Repaired the bounded App capture helper only. The helper now mirrors Agent
0a's project-data recording order: it lets `object()` capture the three
container reads and does not pre-read the leaf. Those reads remain in the
complete local `CommandRecord`; the submitted `EditCommand` omits its
optional `reads` claim because Agent treats project-data container reads as
generated setup claims and rejects them when supplied as portable reads.

No dispatcher, activation, Runtime, public schema, endpoint, store, vendor,
dependency, timeout, or legacy-writer change was made.

The requested historical PLAN2/PLAN3/PLAN6, `scratchpad/luna/reports`, and
separate latest App/Agent status files were not present in this environment;
the top-level plan and available project-data handoffs were used.

## Private exact parity probe

Agent source was archived read-only from:

```text
commit: 0a774e4968f5a9728c4ee6b5bbbfe286e26f29a3
tree:   2f3eee4e9a7d37db80374b5e98d16f1e08082a35
```

The one private archive was created under this worker worktree, guarded by an
EXIT cleanup trap, and removed after each run. The initial standalone import
probe completed successfully (`imports-ok`). The old App carrier reproduced
the real failure under a 60-second external Python run:

```text
CommandError: submitted reads does not match authoritative capture
kind=capture_mismatch
```

This distinguishes the earlier five-second subprocess timeout from a bridge
startup/import failure. The bounded App fix was then checked with an actual
current TS-generated two-command carrier:

```text
project-data.write parent target=com.example.compiler-canary key=source value={version:1} mode=replace
project-data.write parent target=com.example.compiler-canary key=__dsl_sm__:sm-1 value={id:sm-1,sourceLine:3} mode=replace
```

The private Agent run executed the exact carrier through `execute`, generated
the full records, inverse, redo, and replay. Results:

```text
bundle_match=True
records_match_ignoring_submitted_reads=True
input_unchanged=True
inverse_restores_original=True
redo_restores_forward=True
replay_preserves_disjoint_key=True
mixed_refused=True
mixed_input_unchanged=True
forward records=2; inverse records=1; redo records=2; replay records=2
forward record read counts=[2, 0]
```

The record comparison ignores only the expected distinction that Agent adds
authoritative `command.reads` claims during acceptance; all other record
fields, including writes, guards, order, and full record reads, matched.

## Tests

Passed:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  src/tools/video-editor/commands/projectDataMember.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts
=> 16 passed

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  src/tools/video-editor/lib/compiler-canary.test.ts \
  -t 'project-data|source-map|source map|DSL source'
=> 6 passed, 53 skipped

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  src/tools/video-editor/lib/source-map-runtime.test.ts \
  -t 'project-data|persists|delete removes|updated'
=> 3 passed, 28 skipped

./node_modules/.bin/eslint src/tools/video-editor/commands/projectDataMember.ts \
  src/tools/video-editor/commands/projectDataMember.test.ts --max-warnings 0
=> passed

./node_modules/.bin/tsc --noEmit --pretty false
=> passed

git diff --check
=> passed
```

No full suite, browser, localhost, socket, Runtime HTTP, public pin, or
unchanged-tree broad test was run.

## Remaining boundary

The project-data member remains inert. Runtime's matched 89ed contract and
the paired App consumer/adoption gate are still required before activation,
legacy-writer retirement, or public qualification.
