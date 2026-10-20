# App project-data Main merge/default/order lowering

Date: 2026-10-20 UTC

## Result

Implemented the inert App lowering in `src/tools/video-editor/commands/projectDataMember.ts`.

- Main `project-data.write` omitted mode is lowered as `replace`, matching the
  current Main compiler (`mode ?? 'replace'`).
- Main `merge` is lowered to one native closed `replace` write by recursively
  merging only the original guarded leaf value with the declared input. The
  native command still carries the original container and leaf guards; no
  whole-config diff or new guard is generated.
- Main's stable declared-order sort is applied before capture: explicit order
  ascending, ties by source index, then unordered operations in source order.
- Existing App safety boundaries remain: canonical outer keys, finite JSON,
  nested reserved-key refusal, malformed namespace refusal, limits, and
  mixed-batch atomic refusal. The member remains inert; no generic routing,
  Runtime activation, pin, DTO, schema, dependency, or public contract changed.

## Tests

Passed:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/projectDataMember.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts
=> 2 files passed; 17 tests passed

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/compiler-canary.test.ts \
  src/tools/video-editor/lib/source-map-runtime.test.ts \
  -t 'project-data|source-map|source map|DSL source|persists|delete removes|updated'
=> 2 files passed; 10 tests passed, 80 skipped

./node_modules/.bin/tsc --noEmit --pretty false
=> passed

./node_modules/.bin/eslint src/tools/video-editor/commands/projectDataMember.ts \
  src/tools/video-editor/commands/projectDataMember.test.ts --max-warnings 0
=> passed

git diff --check
=> passed
```

The new focused tests cover Main-vs-native merge/default/order output and
namespace key order, stale same-leaf refusal, disjoint replay preservation,
opaque/null/absence handling, unsafe input refusal, malformed namespace refusal,
and mixed-batch atomic refusal.

Private TS-to-Agent parity probe, run with a temporary private Agent archive in
this worktree and cleaned on exit, passed against both reviewed refs:

```text
hub/timeline/agent/tl/agt-m2-project-data-main-limits-fix (0a774e4...)
hub/timeline/agent/tl/agt-m2-full-carrier-projectdata-source (e010e6a...)
=> execute_bundle_match True
=> full records matched after ignoring only command-level submitted-read decoration
=> inverse_restores True
=> redo_restores True
=> replay_restores_forward True
```

No full suite, browser, localhost, live socket, Runtime HTTP, public pin,
dependency install, or activation test was run.

## Decisions and blockers

The current Main compiler is the authority for default and merge behavior:
project-data defaults to replace, while merge recursively combines only two
non-null object cells; arrays, nulls, absent values, and scalar cells replace.
The App retains its already-agreed stricter canonical-key and unsafe-input
preflight rather than widening native acceptance. Runtime392/native-door
qualification is still an external prerequisite, so this change intentionally
does not activate the member or retire the legacy writer.

Recommended next step: qualify this inert capture through the matched Runtime
392 provider/door pair, including accepted-record, retry, mixed-batch, stale
same-leaf, disjoint rebase, and inverse controls before consumer activation.
