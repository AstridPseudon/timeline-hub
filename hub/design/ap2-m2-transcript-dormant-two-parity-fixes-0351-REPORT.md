# App2 transcript dormant parity fixes

## What changed

- In `src/tools/video-editor/commands/transcriptAssociateCapture.ts`, the
  command's exact new `DocumentPin` is checked against the supplied hydrated
  source pin before the command's recorded projection work. A swapped command
  pin/source pair now refuses with `capture_mismatch` and leaves the input
  bundle unchanged.
- The parent clip write now follows Agent's `parent_clip_path` rule: a
  populated `config.clips` is authored when `parent.clips` is an empty array;
  no empty-primary-to-derived-mirror write is produced.
- Added two regressions in
  `src/tools/video-editor/commands/transcriptAssociateCapture.test.ts`,
  including explicit command reads/claims, dependency, and write assertions
  for the mirror case.

## Evidence

The two new tests were red on the untouched `bac1fa0d` baseline: the swapped
pin was accepted and the empty-primary case wrote `parent.clips`. They are
green after the two source-only corrections.

Passed:

- `TMPDIR=<worker temp> npx vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/transcriptAssociateCapture.test.ts` — 1 file, 7 tests passed.
- `TMPDIR=<worker temp> npx vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/transcriptAssociateCapture.test.ts src/tools/video-editor/data/typed/importTranscriptIdentity.test.tsx src/tools/video-editor/lib/project-transcript-host.test.ts src/tools/video-editor/data/typed/timelineBundle.test.ts` — 4 files, 54 tests passed.
- `npx eslint src/tools/video-editor/commands/transcriptAssociateCapture.ts src/tools/video-editor/commands/transcriptAssociateCapture.test.ts --max-warnings 0` — passed.
- `npm run typecheck:strict-islands` — passed.
- `git diff --check` and base diff check — passed.
- `rg` live-caller scan — no callers beyond the dormant helper exports and focused test.

No full, browser, HTTP/socket, activation, host/CRUD/persistence, generated,
or broader matrix suite was run, as directed.

## Decisions / blockers

No decision beyond the settled HOLD0344 review was needed. The exact Agent
path rule was taken from `native_transcript_association.py` and
`_command_state.py` at Agent `53c2c6f9`. Nothing is blocked.

## Next step

Independent review can recheck this two-file branch before any dormant helper
consumer or pin adoption is considered.
