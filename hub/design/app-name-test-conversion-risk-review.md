# App M2 embedded shot-name test conversion risk review

## Decision

**APPROVE** `48fc0432a27a27156589a0837cad25b63da3cb70c` for the bounded
embedded shot-name test conversion.

This is a read-only review. No App product files, tests, lockfiles, branches,
or refs were modified.

## Review scope and findings

- The three converted pre-existing `ShotEditorView` name cases retain the
  original inputs exactly: `My older name`, `My name`, and `Renamed`.
- Each missing-authority case now checks the visible refusal error, zero
  canonical adapter publication, zero legacy/Supabase name mutation, and an
  unchanged canonical graph. The existing `useNameEditing` refusal test still
  checks exact dirty-draft restoration and that the form remains open.
- Each corresponding success case submits the same input through the supplied
  occurrence-owned `shot.set` port and checks occurrence capture, exact
  `{ values: { name }, clear: [] }` finish arguments, the `shot.set` selector,
  and submission. It also checks no canonical or legacy mutation traffic and
  preserves the opaque input graph unchanged.
- The parameterized settings half, including raw opaque-field, Runtime payload,
  and load/reload-related assertions, remains unchanged. The canonical settings
  row remains explicitly open as required.
- The source deletion is bounded to the explicit placed context identified by
  `canonicalComposition && canonicalOccurrence`. The standalone/unplaced
  `updateShotNameMutateRef` project method remains.
- The native test double uses only fields asserted by the existing
  `ShotSetCapturePort`/`EditCommand` contract; no fictional closed-wire field
  was introduced. No skip, xfail, or unrelated assertion deletion was found.

## Evidence

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/travel-between-images/pages/ShotEditorView.test.tsx
PASS — 1 file, 22 tests

git diff --check HEAD^ HEAD
PASS
```

Not run: unchanged full65, full suite, browser/e2e, localhost/live sockets,
TypeScript, install, build, or shared dependency/cache writes.

## Remaining boundary

The whole settings row remains open and was not expanded by this review.
