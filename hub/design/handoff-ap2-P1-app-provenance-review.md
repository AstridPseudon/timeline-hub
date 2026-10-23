# P1 App provenance-fix independent review

Result: **FAIL**.

The committed repair correctly makes the declared `source.commit`, `source.path`,
and `source.sha256` check historical and immutable, but it removes the original
current-working-tree byte-integrity guarantee for real fixtures that the test
actually consumes. The H3 mixed App + Runtime + Agent chain remains authored-not-go
and unqualified; this review makes no H3 claim.

## Reviewed commit and scope

- Reviewed App commit: `d2fcf3ff4d680b5086d924bdf398a41fd0ea87ca`
- Diff: exactly one file, `src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts`
- Diff size: 10 insertions, 2 deletions
- No product, harness, session, outbox, schema, generated file, pin, dependency,
  launcher, provider, or test expectation changes were made by this review.
- Review worktree remained clean; no source or fixture bytes were modified.

The historical check is correct for provenance: `sourceSha()` at lines 33–38
hashes `git show <commit>:<path>`, and all eight corpus entry records resolve in
the local App/Agent object databases with their declared SHA-256 values. The
current App harness bytes intentionally differ from the historical declaration
(`b243b340177c2d905f841ec4c7307b03e7afd4f43f0096701c20bf132f202534` current vs
`2ba2164ba7fd2d76ccca94d0645e6b79236c85ab4e53e82e84ae1af250c7d815` declared),
which is the stale mutable-harness condition this repair was meant to handle.
The other seven entry fixtures currently match their declared historical bytes.

## Blocking finding: current fixture integrity silently disappeared

`expectSource()` at lines 48–51 now calls the historical `sourceSha()` and then
only asserts that the current path is truthy. It no longer hashes the current
file. That matters because the behavioral test imports the current App trim and
move fixtures at lines 8–9 and reads the current Agent split fixture through
`readSource()` at lines 73–76. A changed current fixture can therefore be the
actual behavioral input while the historical `git show` bytes still satisfy the
provenance assertion.

An isolated temporary-copy probe changed the current trim fixture's input
`parent_revision.payload.config.clips[0].from` from `2` to `999` without touching
the repository. Its result was:

```text
historicalSha: 4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152
currentSha: 4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180d5b06152
corruptedSha: f2a6a35ed71332695f335f30b6f6c94949e55b29b9e695bdf3f8c983fd17413b
gitShowHistoricalCheck: true
currentFixtureIntegrityCheck: false
corruptedInputValue: 999
```

The `currentSha` line above is the unchanged declared value
`4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152`; the
temporary corrupted copy is the `corruptedSha` value. Thus a git-show-only
assertion would accept the historical bytes while failing to reject the
corrupted current input. This violates the brief's explicit current-fixture
byte-integrity requirement.

## Required bounded correction

Keep both concerns explicit and separate:

1. Continue checking the declared historical bytes with `git show` for immutable
   provenance, including the mutable e2e harness declaration.
2. Restore a current-file SHA check for the real current fixture files consumed
   by imports and `readSource()`. The mutable harness must have an explicit,
   narrowly scoped historical-only treatment rather than making every current
   fixture integrity check inert. Do not refresh the declared digest, weaken or
   skip the behavioral assertions, or add a second executor/launcher/provider.

The documented environment requirement is that each corpus-declared commit/path
remain available to `git show`; a shallow repository or source archive without
those objects is unsupported and should fail explicitly. It must not silently
fall back to current bytes or turn the current-fixture check off.

## Exact verification

- `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts` — PASS, 1 file, 12 tests.
- `node node_modules/typescript/bin/tsc --noEmit` — PASS, exit 0.
- `node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts --max-warnings 0` — PASS, exit 0.
- `git diff --check` — PASS, exit 0.
- Read-only provenance probe over all eight corpus entry sources — PASS: every historical `git show` SHA matched its declared SHA; current-vs-historical mismatch is limited to the mutable App harness.
- Isolated temporary-copy corruption probe — PASS as a counterexample: historical check stayed true while the corrupted current fixture hash differed and the consumed input changed.

No full, browser, heavy, or central test-service run was requested.
