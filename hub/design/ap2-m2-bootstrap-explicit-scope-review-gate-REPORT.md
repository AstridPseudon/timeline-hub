# AP2-M2 bootstrap explicit-scope review gate

## Verdict

**BLOCKED — prerequisite locked-graph wrapper rerun failed.** No bootstrap gate was queued. The required prerequisite report is
[/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-locked-graph-wrapper-owner-rerun-REPORT.md](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-locked-graph-wrapper-owner-rerun-REPORT.md>).

## Earliest causal result

The exact locked wrapper was run once by the owner rerun and exited `2` because the real App project typecheck exited `2`. The ordinary Node/TypeScript probe passed (`0`), but the wrapper's 10 genuine current App diagnostics remain. The failure occurred before any bootstrap browser test could execute:

- `src/tools/video-editor/commands/elementCapture.ts:236` — `TS2345`
- `src/tools/video-editor/commands/elementGesture.ts:89` — `TS2345`
- `src/tools/video-editor/commands/elementGesture.ts:93` — `TS18048`
- `src/tools/video-editor/commands/elementGesture.ts:112` — `TS2345`
- `src/tools/video-editor/commands/genericPatchCapture.ts:306` — `TS2345`
- `src/tools/video-editor/commands/occurrenceDuplicateCapture.ts:83` — `TS2322`
- `src/tools/video-editor/commands/occurrenceDuplicateCapture.ts:195` — `TS2345`
- `src/tools/video-editor/commands/occurrenceDuplicateCapture.ts:199` — `TS2345`
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx:49` — `TS2345`
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx:50` — `TS2345`

The prerequisite report records no missing dependency, broken graph symlink, writable graph mutation, or deleted `/tmp` dependency. Therefore this worker did not race the reproduction and did not submit another locked test.

## Read-only source recheck

The current branch is clean at helper commit `252da0590` (`test(app): repair bootstrap timeline scope helper`) with no additional changes.

- `tests/e2e/local/support/timeline-scope.ts` defines a test-only `TimelineScope` requiring both `projectId` and `timelineId`; `timelineBase` interpolates both explicitly.
- `three-products.spec.ts` defaults existing seeded callers to `harness.seed.projectId` and `seed.timelineId`, preserving the seeded harness scope.
- The bootstrap test passes the observed created project and selected timeline as an explicit scope to `history`, removing the prior spread-object workaround and closing the undefined `seed.projectId` path.
- The original bootstrap assertions remain present and exact: observed project/timeline ID and non-shot selection; create-before-init order; Runtime `/v1` statuses; zero legacy snapshot traffic; one history entry with `previous: null`; `timeline.init` then two `track.create` records; exact retry after reload/restart; guarded `timeline.inverse`; preserved original track name; and zero legacy traffic after retry/undo.
- `timeline-scope.test.ts` directly covers both seeded and created-project path construction.

## Tests

Not run in this worker. The task requires stopping when the locked-graph-wrapper-owner-rerun report is not PASS; consequently no local driver/browser/socket test and no central target gate was started. The required target command was therefore **not** submitted:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-bootstrap-explicit-scope-helper-fix \
  <unique narrowed bootstrap-only App integration suite>
```

## Next step

The owning App work must classify/fix the 10 real project typecheck diagnostics and obtain a PASS from the locked wrapper owner rerun. Only then should this exact helper candidate be re-reviewed and, if still clean, queued for its one bootstrap-only central result.
