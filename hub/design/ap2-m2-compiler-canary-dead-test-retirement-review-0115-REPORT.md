# Independent compiler-canary dead-test retirement review

## Verdict

**APPROVED** for the exact candidate below. The private compiler-canary
producer and its 59 self-tests are dead and non-public. The candidate does not
remove a live caller, emitter, SDK export, registry entry, manifest entry, or
retained source-map/project-data/navigation behavior. The 59-test retirement is
one-to-one and every retired behavior is explicitly marked as gone with the
private canary.

## Exact candidate identity and scope

- Candidate commit: `645a5cc94c9730b5dc21757b4c90ad3b97944ae5`
- Candidate tree: `9ae9121c0aac4f2cdb385e7831c99d05aeeb100a`
- Parent commit: `813a85106ecb4abbaf224081abe6c33b8dab0df7`
- Parent tree: `2a19a78bb1bdfb3fd779f568a1b513b094318982`
- Changed paths are exactly:
  - `src/tools/video-editor/lib/compiler-canary.ts` (601 lines deleted)
  - `src/tools/video-editor/lib/compiler-canary.test.ts` (1,570 lines deleted)
  - `eslint.strict-debt.js` (the one stale canary entry deleted)

No retained source-map, navigation, project-data, patch, proposal, ownership,
or `useTimelineOps` source or test file differs from the parent. No replacement
API, DTO, adapter, fallback, schema, version guard, or test weakening was
introduced.

## Independent dead/private proof

I searched the parent tree and the candidate tree for the module path and all
compiler-canary symbols.

- Outside the deleted module and its own test, there is no import, re-export,
  `createCompilerCanary`, `createCompilerCanaryExtension`, `CompilerCanary`, or
  `CanaryDsl` reference.
- There is no dynamic `import()` or `require()` containing the module path.
- There is no extension registry, loader, pack, host assembly, public SDK
  barrel, or `config/governance/sdk-public-api-manifest.json` entry for the
  canary module or factory.
- The module's `@publicContract` comments do not make it public. It is not
  exported through `src/sdk/index.ts` and it is not in the public API manifest.
- The retained `SourceMapRuntime` surface is independently real: its public
  interface remains in `src/sdk/index.ts`, `config/contracts/registry.json`,
  and the public API manifest; `source-code-navigation.ts` consumes that
  interface in its active navigation implementation; and the source-map
  runtime persists entries through the retained project-data operations.
  `src/examples/command-extension.ts` also imports the source-map types from
  the public SDK barrel. The candidate does not alter any of these files.

The remaining textual hits are not canary callers: the active project-data
tests use `com.example.compiler-canary` as an inert extension-id fixture, and
`docs/cutover-inventory.md:1005` is an unrelated raw-grep false-positive
inventory row naming the old test path. Neither instantiates or exports the
deleted module.

## 59-test one-to-one ledger review

The parent test file contains exactly 59 actual `it(...)` declarations. The
0106 report contains exactly 59 ledger rows. A bidirectional name comparison
found no source test missing from the ledger and no ledger row absent from the
source test. Every row has the exact disposition:

`BEHAVIORGONE: private canary`

This is truthful because there is no live or public caller to preserve. The
retired tests cover only the private canary's JSON/DSL validation, snapshot
reading, proposal production, generated-object ownership, source-map stamping,
cleanup/recompile behavior, and its private import/call-boundary checks.

Distinct behavior that remains part of the active project is covered by the
retained controls, not claimed as a one-for-one replacement for the canary:

- `projectDataMember.test.ts`: native ordered source/source-map project-data
  writes, exact values and opaque siblings, replacement, namespace birth,
  malformed namespace refusal, guards, and atomic mixed-batch refusal.
- `source-map-runtime.test.ts`: source-map create, persistence, lookup,
  extension isolation, stale marking, deletion, granularity, positions, and
  lifecycle behavior.
- `source-code-navigation.test.ts`: source-to-timeline and
  timeline-to-source navigation, stale status, overlap, target selection, and
  round-trip behavior.
- `genericPatchCapture.test.ts`, `timeline-patch.test.ts`,
  `proposal-runtime.test.ts`, `managed-object-guard.test.ts`, and
  `useTimelineOps.test.ts` remain unchanged and retain their active native
  command/proposal/guard controls.

## Verification

The permitted targeted neighbor run passed:

```text
TMPDIR=<private temporary directory> ./node_modules/.bin/vitest run --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/source-map-runtime.test.ts \
  src/tools/video-editor/lib/source-code-navigation.test.ts \
  src/tools/video-editor/commands/projectDataMember.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/lib/timeline-patch.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts
```

Result: **6 files, 439 tests passed**.

These checks also passed:

```text
./node_modules/.bin/eslint eslint.strict-debt.js --max-warnings 0
node --check eslint.strict-debt.js
git diff --check HEAD^ HEAD
```

An attempted `--configLoader=runner` variant failed during Vitest config
startup because this repository's config uses `__dirname`; it was a harness
configuration incompatibility, not a test failure. The normal repository
configuration above passed.

No full suite, browser, localhost, live socket, or central gate was run.

## Follow-up

The orchestrator may land the exact candidate commit and close the corresponding
dead-file/dead-test ledger entry. Keep the retained public source-map runtime,
SDK surface, navigation implementation/tests, and native project-data tests;
do not remove the fixture-only `com.example.compiler-canary` strings as part of
this retirement. The stale cutover-inventory row is documentation residue and
is not a product or deletion-gate blocker.
