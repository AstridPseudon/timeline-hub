# Transcript two-fix contract recheck 0351

## Verdict

**APPROVE exact source commit `bbbe3788be06d4be35d7fd219f4d4ca7b9e16076`**
(`af350a5344d1b542904f5acf0b4a1388822d3729`), parent
`bac1fa0dad486b4b6d41cfc8682ee01fb4cac875`.

The source is limited to:

- `src/tools/video-editor/commands/transcriptAssociateCapture.ts`
- `src/tools/video-editor/commands/transcriptAssociateCapture.test.ts`

## Review findings

- The new-pin check compares `exactPin(args.document, 'new')` with the
  hydrated `source.pin` before projection/writes, returning `capture_mismatch`
  atomically for the pinA/source.pinB case.
- The clip path now matches Agent `53c2c6f95632bf104b8bb13698e7a262822ecfdb`:
  `parent.clips` is selected only when populated, or when the config mirror is
  absent/empty; an empty primary with populated `config.clips` writes the
  authored config collection.
- The compact mirror regression asserts the complete recorded command reads,
  expectations, authorship, dependency, and write records. Its expected
  dependency/write shape matches the Agent command for the same case.
- The swapped-pin regression asserts refusal and unchanged input.
- The commit contains no other semantic, assertion, dormancy, live-caller, or
  pin changes. The live-caller scan found no callers beyond the dormant helper
  exports and focused test.

## Evidence

The source worker recorded both new regressions failing on untouched `bac1fa0d`
(swapped pin accepted; empty-primary case wrote `parent.clips`) and passing after
the fix.

Passed on the exact source commit:

```text
TMPDIR=<worker temp> npx vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/transcriptAssociateCapture.test.ts
1 file, 7 tests passed

TMPDIR=<worker temp> npx vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/transcriptAssociateCapture.test.ts src/tools/video-editor/data/typed/importTranscriptIdentity.test.tsx src/tools/video-editor/lib/project-transcript-host.test.ts src/tools/video-editor/data/typed/timelineBundle.test.ts
4 files, 54 tests passed

npx eslint src/tools/video-editor/commands/transcriptAssociateCapture.ts src/tools/video-editor/commands/transcriptAssociateCapture.test.ts --max-warnings 0
passed

npm run typecheck:strict-islands
passed

git diff --check
passed
```

No product edit, browser/socket/HTTP, full suite, activation, or unchanged-test
replay was performed by this review.

## Next step

The corrected source may replace donor `bac1fa0d` after this approval. Keep the
helper dormant until the separately required consumer and normal Door proof.
