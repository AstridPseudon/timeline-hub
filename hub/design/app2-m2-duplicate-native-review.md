# App2 M2 duplicate native review

Decision: `REQUESTCHANGES` for the five-file source delta at `85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c..a2e6bde1c823aee15601dfa5f11baea2dca3c3f5`.

## Scope and source result

The delta is exactly the permitted five added files:

- `src/tools/video-editor/commands/occurrenceDuplicateCapture.ts`
- `src/tools/video-editor/commands/occurrenceDuplicateGesture.ts`
- their two focused tests
- `src/tools/video-editor/commands/fixtures/recipe_m2_app_occurrence_duplicate.json`

Positive existing fixtures were not changed. The helper has the intended single occurrence scope, two reserved created identities, immutable basis, original command guards, collection membership/order selections, isolated copied authoring state, and no graph publication.

The blocking defect is record parity for raw occurrence roots. In `occurrenceDuplicateCapture.ts:160-184`, the copied occurrence is made with `copy(row)` and only `occurrence_id`/`shot_id` are changed; present `stable_deep_link` and `output_identity` therefore remain the source values in `result.record.writes`. The repaired Agent `68a51203310eb7c1bad343e50a42cf75c46c5321` derives destination roots from the compiled destination shot/revision/occurrence before `create_entity`. Direct comparison of the same actual TS-produced command showed:

```text
TS record == Agent record: False
TS: output_identity .../occurrence/occ-0/output/final-video
Agent: output_identity .../occurrence/occ-copy/output/final-video
TS: stable_deep_link .../shot/chapter-shot/revision/shot-1/occurrence/occ-0
Agent: stable_deep_link .../shot/shot-copy/revision/authoring-shot-revision-44fb.../occurrence/occ-copy
```

The fixture test at `occurrenceDuplicateCapture.test.ts:51-72` checks the later `after_document` compiled projection, which normalizes these values and consequently masks the incorrect occurrence-create record. It does not prove the TS record matches Agent's native record or that the local authored bundle has destination roots before publication. Repair the helper and add/adjust the focused assertion so the actual record and raw destination roots match Agent while absent source roots remain absent.

Non-blocking parity checks passed: created IDs and read/binding/selection structure matched Agent; nested metadata, task/history/association/output-record/unknown values are preserved; the copy is isolated; serialized retry retains one reserved body; refusal paths are atomic.

## Evidence

Focused Vitest, with the ESM `__dirname` compatibility preload needed by this checkout's runner configuration:

```sh
NODE_OPTIONS='--import=data:text/javascript,globalThis.__dirname%3D%22%2Fhome%2Fuser%2Fwork%2Fwt%2Fap2-m2-duplicate-native-review%2Fconfig%2Ftesting%22' \
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --configLoader=runner --maxWorkers=1 --no-file-parallelism \
src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts \
src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts
```

Result: 2 files passed, 40 tests passed.

Actual TS-to-Agent probe used the TS `captureOccurrenceDuplicate`/`finishOccurrenceDuplicate` result and Agent source `68a512...`, not a reconstructed expected command:

```text
validated/executed: PASS
record command exact: True
raw projection exact: True
reload guarded inverse exact: True
command sha256: fb341fc784eb919796e5d65b6f2e8331239b3e8d77e6d61884c3ae5a4db91abb
```

The read-only private Agent recipe lane also passed:

```text
63 passed in 4.20s
```

No full, browser, localhost, live-socket, Runtime, dependency, shared-cache, source/shared-consumer, generated, pin, ledger, or new-test edits were made.

## Current-root port and gate

`CURRENTROOT_PORT: HELD` and `GATE: HELD`, independently of the source decision. Current App root is `05b6b488d` (the relevant shared seam files are unchanged from `85efd0ffa`), but the current root does not contain either native helper file. The shared proposal at [handoff-ap2-m2-duplicate-capture-resume-shared.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-duplicate-capture-resume-shared.patch) therefore depends on landing the five-file source unit first, then applying refreshed shared-session/editor wiring. `git apply --check --verbose -p6` against this source-equivalent root did not apply cleanly: return hunks failed in `commitSession.ts` and `useTimelineCommandSession.ts`; the import/consumer hunks failed in `useTimelineState.types.ts` and `AstridTimelineEditor.tsx` (the `useTimelineState.ts` hunks did locate). Do not approve the old patch/cohort wholesale.

After the source repair and refreshed port, the separate App gate still needs canonical consumer coverage: actual commit/reload, raw immutable occurrence identities, guarded undo/redo, exact retry body/idempotency identity, outbox/restart behavior, and zero legacy duplicate writer/task traffic. The existing graph publication path and legacy `duplicateShotGroup` branch remain unretired.

