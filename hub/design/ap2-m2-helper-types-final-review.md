# ap2-m2 helper-types final review

Decision: **APPROVE SOURCE** for the five-diagnostic typing repair in
`elementCapture.ts`, `genericPatchCapture.ts`, and
`occurrenceDuplicateCapture.ts` at `bf485152f64d084f3bbdafa66fb2b586d2bb481c`.

This is a source-only decision for the three helper files. It does not approve
the App2 consumer/port wiring, behavior or writer retirement, Composition
package adoption, or any full/browser/socket gate.

## Scope review

The branch delta is exactly three helper source files. The repair only retains
validated values in typed locals, gives the duplicate compatibility `state.get`
replacement its `AgentState` return type, and narrows authored identity
fallbacks before stable identity construction. No behavior, record, guard,
cast, config, dependency, pin, test, or shared-install change was made by this
review.

## TypeScript differential

Real App check:

```text
./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false
```

Result: exit 2, 21 diagnostics. The five target diagnostics are absent:

- `elementCapture.ts:236` selector argument narrowing — absent.
- `genericPatchCapture.ts:306` `hold` passed to `clipHold` — absent.
- `occurrenceDuplicateCapture.ts:83` compatibility `state.get` return — absent.
- `occurrenceDuplicateCapture.ts:195` `documentId` for `stableOccurrenceDeepLink` — absent.
- `occurrenceDuplicateCapture.ts:199` `documentId` for `stableOutputIdentity` — absent.

The remaining 21 diagnostics are classified as follows:

- 11 diagnostics are the unchanged pre-existing App baseline (the baseline
  Composition/renderer/config diagnostics recorded by the strict differential
  report).
- 5 current consumer diagnostics are from the App2 element port, not these
  helper repairs: `elementGesture.ts:89,93,112` (three diagnostics) and
  `AstridElementParams.tsx:49,50` (two diagnostics). Git history shows the
  `elementGesture.ts` port was added and the `AstridElementParams.tsx` command
  path was introduced by `14ce9e9a0`; these are App2 consumer typing issues and
  remain outside this review.
- 5 current-only Composition/package-skew diagnostics are unrelated to the
  helper delta: `AudioTrack.tsx:15,16,18` and
  `compiledAudioSourceClock.ts:1` (two missing exports). The lockfile requests
  Composition `0.0.13`, while the shared read-only install reports `0.0.8`.

`npm run typecheck:strict-probe` also exited 0, but its strict-islands include
list excludes all three helpers and the relevant consumers; it is explicitly
not evidence for helper qualification.

## Focused evidence

```text
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts
```

Result: 3 files passed, 46 tests passed, exit 0.

```text
./node_modules/.bin/eslint src/tools/video-editor/commands/elementCapture.ts src/tools/video-editor/commands/genericPatchCapture.ts src/tools/video-editor/commands/occurrenceDuplicateCapture.ts --ext ts --max-warnings 0
```

Result: passed, exit 0. `git diff --check HEAD^ HEAD` also passed.

## Fresh current-TS native parity

Each probe generated its payload from the current worktree TypeScript helper,
then submitted that unchanged command to the frozen read-only Agent source
using `/home/user/work/venv-app2-native`:

- Element: command, full record, and resulting bundle exact; Agent validation
  and execution accepted.
- Generic patch: two commands accepted; command order, both records, and the
  resulting bundle exact; ordinals `[0, 1]`, writes were the expected
  `parent/clip:x::hold` and `parent/track:V1::label` writes.
- Occurrence duplicate: full record, occurrence root write, raw bundle,
  compiled projection, reload, guarded inverse, replay, and created-ID
  stability all exact. Command digest:
  `fb341fc784eb919796e5d65b6f2e8331239b3e8d77e6d61884c3ae5a4db91abb`.

The generic probe used a private temporary extraction of the repository's
0.0.13 Composition artifact because the shared install is 0.0.8; it did not
modify the worktree, lockfiles, or shared node_modules, and the temporary
overlay was removed afterward.

## Not run / limits

No full suite, browser, localhost, live socket, Runtime suite, consumer gate,
outbox/session gate, dependency installation, pin change, or source/test
mutation was performed. The five remaining consumer and five
Composition/package diagnostics must be resolved by their owning work before a
whole-App typecheck can be green.
