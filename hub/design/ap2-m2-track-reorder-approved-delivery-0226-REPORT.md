# App M2 track-reorder approved delivery

## Result

Blocked. The independent `dormant-contract-review0222` did not approve the
exact `source0221` candidate; it issued a terminal HOLD. Per the task
instruction, no repair, merge, activation, pin change, or consumer wiring was
performed.

## Review decision

The reviewer held candidate commit
`1611384358c846ac42b98c38c7f9a6e447d17b77` (tree
`798534e22841e4ba3ea64948a394b6bb9782df3e`) for two source-contract defects:

1. `src/tools/video-editor/commands/trackReorderCapture.ts:85-89` records
   `parent/collection:track` as an ID array. Agent's `track.reorder@1` read
   guard requires the collection-shape object with `members` and `config`
   presence states.
2. The helper emits `resolved: ["parent"]`, but the ACKed non-singleton Agent
   operation requires `resolved: []`; bare `parent` is not a valid
   `ScopedId`.

The review found the rest of the dormant boundary correct and confirmed zero
live callers outside the two new files. Because approval was a prerequisite,
the candidate is not remote-merge ready.

## Tree/base

- Delivery worktree: `ce7152ee4bd5c2dc07454d18200d3be8225ca391`
- `hub/timeline/app/tl/integration`: `ce7152ee4bd5c2dc07454d18200d3be8225ca391`
- Candidate inspected: `1611384358c846ac42b98c38c7f9a6e447d17b77`
- Delivery worktree changes: none

## Live callers changed

None. No files were changed in this delivery worker.

## Evidence

The independent reviewer reported:

- Candidate focused Vitest plus track-management neighbor: 36 tests passed.
- Reviewer-side track-management neighbor: 28 tests passed.
- ESLint and candidate `git diff-tree --check`: passed.
- App TypeScript: baseline exit 2 on unrelated existing diagnostics; no
  diagnostics for either new track-reorder file.
- Caller search on the candidate: no callers outside
  `trackReorderCapture.ts` and `trackReorderCapture.test.ts`.

No delivery merge, browser/socket test, full suite, generation, Runtime
acceptance, pin, or activation was run. A HOME_STATUS file was not present;
the current App2 `STATUS.md` and `INBOX.md` were read.

## Next step

The source worker should repair only the two envelope claims above, update its
focused assertions, and obtain a fresh independent approval for the resulting
exact commit/tree. Then a delivery worker can repeat the prescribed merge
forward from the latest HOME integration base.
