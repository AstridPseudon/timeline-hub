# Dormant `track.reorder@1` App capture review

## Verdict

**HOLD — do not approve App commit `1611384358c846ac42b98c38c7f9a6e447d17b77` (tree `798534e22841e4ba3ea64948a394b6bb9782df3e`) as the exact dormant source contract yet.** The smallest correction is confined to the new helper and its focused test; no generated, Runtime, session, Provider, serializer, pin, or published-artifact work is needed.

The comparison target is the ACKed Agent source `c1ae9e93d31c1c091b93c952ae803059a890bf61` (tree `a54be6e2269e191c032496b3b73cfcf761d7402e`).

## Blocking findings

1. `src/tools/video-editor/commands/trackReorderCapture.ts:85-89` records the wrong state for `parent/collection:track`. It emits `present(value: refs)`, where `refs` is the ID array. Agent's `collection.tracks` selection reads this reference through the collection-shape guard: the required value is an object containing `members: present([])` and `config: present({})` (with presence/absence preserved), matching the existing App collection-read convention. On Agent execution, the candidate's read claim therefore does not match the current state and is refused before the reorder handler runs. Replace this read value with the exact track collection shape; do not weaken the guard.

2. `trackReorderCapture.ts:103` constructs the command through the existing App `MoveRecording`, whose constructor initializes `resolved` to `[command.select]`. The resulting capture has `resolved: ["parent"]`. Agent registers `track.reorder` as a non-singleton operation, so its exact captured command has `resolved: []`; moreover, bare `parent` is not a valid `ScopedId` under the ACKed schema. Set the dormant command's `resolved` to `[]` before returning/capture-claim comparison, as the existing non-singleton structural capture pattern does.

The rest of the contract is bounded correctly: `order` and `expected_order` are complete unique same-owner permutations; raw rows are rearranged by identity without reconstruction; stale order/identity and malformed, missing, duplicate, foreign, or non-array lane-bearing input refuse before mutating the caller; and the helper has zero live callers.

## Scope and tree checks

- The commit adds only `trackReorderCapture.ts` and its focused test (269 lines); no generated type/schema, DTO, store, port, API, session, Provider, serializer, pin, or activation change.
- `git grep` on the committed tree found no callers outside the two new files for `trackReorderCapture`, `finishTrackReorder`, `executeTrackReorder`, or `track.reorder`.
- No code edits were made by this review. The current published pin remains untouched and does not contain this operation.

## Evidence

Producer worker evidence:

```text
node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/trackReorderCapture.test.ts \
  src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts
2 files passed; 36 tests passed

node_modules/.bin/eslint src/tools/video-editor/commands/trackReorderCapture.ts \
  src/tools/video-editor/commands/trackReorderCapture.test.ts \
  --report-unused-disable-directives --max-warnings 0
passed

git diff --check
passed
```

Reviewer-side existing track-management neighbor control:

```text
node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts
1 file passed; 28 tests passed
```

The producer's App TypeScript command exited 2 on the existing integration baseline (including unrelated `useRenderState.ts` and `config-utils.ts` diagnostics); it reported no diagnostics for either new track-reorder file. The reviewer also verified `git diff-tree --check` on the candidate and found no output. No full, browser, localhost/socket, generation, Runtime acceptance, or actual consumer gate was run, as required.

## Next step

Repair only the two dormant command-envelope claims above, update the focused assertions to compare the Agent collection shape and `resolved: []`, then rerun the same focused builder and track-management controls. Re-review the resulting exact commit/tree before any future generation or activation proposal.
