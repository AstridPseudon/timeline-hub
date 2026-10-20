Implemented the Gate6 audio comparison transplant.

Changed only:

- `cases.ts`: compares real Player capture PCM with the same CPU export PCM, then rejects planted half-gain audio.
- `canvas.test.ts`: verifies comparator reachability and positive-before-negative ordering.

Passed:

- `audio-join.test.ts`
- `canvas.test.ts`
- `tab-audio.test.ts`
- ESLint
- `git diff --check`

TypeScript triage found only pre-existing diagnostics; no new-line diagnostics.

No browser/render/full/physical qualification was run. Handoff artifacts, patch, commit message, report, and `DONE` are in the worker directory.