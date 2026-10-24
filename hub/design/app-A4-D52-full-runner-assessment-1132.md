# A4/D52 read-only assessment — PASS

Base: `e8a593e1d38d9e84207de1f97806b535ec1a1a8f`, tree `c94c46704d0265c0a1d2217e84992a6532420ef5`.

Verdict: mixed file. `timeline-save-utils.ts` is live; only the command-runner section of its test is retired executor behavior. Do not restore the executor export.

Evidence:

- Repro command:

  `./node_modules/.bin/vitest run src/tools/video-editor/lib/timeline-save-utils.test.ts --config config/testing/vitest.config.ts --no-cache --no-file-parallelism`

  Result: expected collection failure, `TypeError: createTimelineCommandRunner is not a function` at line 203; 0 tests collected.
- Current `commands/index.ts` and `src/tools/video-editor/index.ts` export no runner functions.
- No non-test production caller/export of `createTimelineCommandRunner`, `runTimelineCommands`, `applyTimelineCommandEffect`, or `createTimelineCommandRegistry`.
- Runner references are test-only: `timeline-save-utils.test.ts`, `commands/runner.test.ts`, `commands/media.test.ts`, and one `sha256.test.ts` assertion.
- Frozen R4 did have production runner edges; A4 commits `ce7a48e`, `b2a546f`, `9c9c180`, and `7c225a3` intentionally removed those edges.
- `timeline-save-utils.ts` remains imported by live mutation, media, trimming, polling, history, transcript, data-kind, commit, patch, and save paths.

Assertion inventory:

- LIVE: `timeline-save-utils.test.ts:237-953` — 79 `expect` expressions covering source edits, stable signatures, CAS media placement, assembly/repair, registry/snapshot reconstruction, themes, pinned groups, polling, defaults, and null handling.
- LIVE: `:1124-1137` — 4 App opaque-data preservation assertions.
- RETIRED executor-only: setup `:89-203` plus `describe('timeline command runner core')` `:955-1121` — 5 test declarations and 28 assertions for validation, dry-run inverse metadata, executor undo, atomic rollback, and `compat_partial`.

Proposed PR-sized cleanup:

1. Delete `src/tools/video-editor/commands/runner.ts` and `runner.test.ts`.
2. Remove only the executor imports/setup/block from `timeline-save-utils.test.ts`; retain all live sections above.
3. Remove only the `applyTimelineCommandEffect` import and test in `sha256.test.ts`.
4. Remove only the legacy-runner parity bridge in `commands/media.test.ts:13-24`; retain direct prepared-media behavior assertions.
5. Retain `timeline-save-utils.ts`, `media.ts`, `MEDIA_COMMAND_DESCRIPTORS`, `commands/types.ts`, D31 transcript behavior, and the full C0 v2 request/reply path.

No source, test, config, ledger, or design files were changed. `git diff --check` passed and the worktree is clean. Existing e8a typecheck/lint proof remains applicable because source is unchanged. Commit metadata and `DONE` marker were written.