# Post-canary dead-helper sweep

## Result

The bounded sweep found no newly dead private helper, import, or registration
in the owned App paths. The deleted `compiler-canary.ts` imported only public
types from `@astrid/editor-sdk`; all of its private helpers were defined in
that deleted module and disappeared with it. No remaining App source imports
the deleted module or its symbols.

I removed the one newly stale strict-debt registration from
`eslint.strict-debt.js`:

```diff
-  "src/tools/video-editor/lib/compiler-canary.ts",
```

This is the exact previously approved hunk. No threshold or other debt entry
changed.

## Retained consumers

The public/shared surfaces formerly imported by the canary remain live and
were not changed:

- `TimelineOps`: `useTimelineOps.ts`, `extensionContextFactory.ts`, and
  `proposal-runtime.ts` use the public mutation contract.
- `SourceMapEntry`: `source-map-runtime.ts`, `source-code-navigation.ts`, and
  `timeline-reader.ts` use source-map persistence and navigation.
- `GeneratedObjectMeta`: `timeline-reader.ts` reads generated-object metadata;
  the SDK source-map contract and its tests retain the host metadata helper.
- Proposal, reader, snapshot, patch, and extension-context types remain used
  by their corresponding runtime adapters and SDK contracts.

The remaining `com.example.compiler-canary` strings are inert extension-ID
fixtures in retained project-data tests, not imports or registrations. No
test was retired in this sweep, so no new behavior mapping or approval was
needed. The prior 59-test canary retirement remains covered by its separately
approved deletion packet.

## Verification

Passed:

```text
TMPDIR=<private temporary directory> ./node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/lib/source-map-runtime.test.ts src/tools/video-editor/lib/source-code-navigation.test.ts src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/lib/timeline-patch.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts
6 files, 439 tests passed

TMPDIR=<private temporary directory> ./node_modules/.bin/eslint eslint.strict-debt.js --max-warnings 0
passed

node --check eslint.strict-debt.js
passed

git diff --check
passed
```

No browser, full, localhost, live-socket, pin, API, framework, or central
suite was run.

## Decisions and status

- Kept all public/shared source-map, SDK, navigation, and native project-data
  code and tests because they have real consumers.
- Removed only the stale private canary strict-debt entry.
- Kept the broad ordinary row OPEN; `useTimelineOps` still has the central
  snapshot fallback for unsupported ordinary families.
- No blockers for this bounded cut. HOME's separate native bootstrap proof
  and other ordinary-row work remain outside this task.

Recommended next step: merge the one-line strict-debt cleanup through the
normal App integration flow; no further canary sweep is indicated unless a
new caller or registration appears.
