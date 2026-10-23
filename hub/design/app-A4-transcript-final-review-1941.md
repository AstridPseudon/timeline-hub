# A4 transcript cumulative first-return independent review — FINALPASS

Reviewed `tl/app-A4-transcript-mounted-return-1930` at `b167101f37` cumulatively against `6e04a9a9a7`, PLAN §3 A2/A3/A4, contract §§1–5, and the 1921 brief. The cumulative tree adds exactly one file, `src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx` (428 lines); the three other required target tests and all production code are byte-identical to `6e04a9a9a7`.

## Result

PASS. The return fixes both findings from the 1924 FAIL without changing product code, existing tests, configuration, generated contracts, pins, locks, or environment.

The test uses the genuine mounted chain:

`useProjectTranscriptHost.importTranscript` → `commitData(..., { save: true, semantic: true })` → `useTimelineSave` → `useTimelinePersistence`/`TimelineLocalSaveHandoff` → `createLocalSaveSession` → durable `commitOutbox` → `RuntimeDataProvider.commitTimeline` → generated `WorkspaceClient` POST.

The accepted case verifies the serialized commit route, App source binding, exact `r0/p0` base pair, label, `atomic` merge, `dry_run: false`, `doc.patch` command, created list, step identity/intent/tags/ordinals/patch, omitted reads, raw null/absence and sibling/order preservation, canonical `r1/p1` adoption, and no invented `transcript.associate` or metadata authority. The returned v2 envelope is complete for this accepted path: data status/base/previous/accepted/rebase fields, digest, commands, identity map, provider/compiler versions, effective `merge_mode`, label/source, canonical closure, authoritative steps/dependencies, and receipt fields. It explicitly asserts `receipt.result === data`.

The refusal mock is a genuine structured 409 conflict with `details.status`, `reason`, `code`, `path`, `hint`, `suggested_command`, `base`, actual `current`, and structured `conflicts`; it intentionally has no mandatory `details.head`. The real classifier reaches `conflict`, not unknown/retry. The mounted session visibly rolls back to canonical `r0/p0` with no transcript association/bundle, returns the user-facing “Timeline association is still unsaved” message, and retains the rejected outbox record with the exact serialized commit path, body, and idempotency key. The fixture’s actual current head is `r0/p0`; no intervening writer is claimed by this narrow case.

The existing association-read, config-mirror fallback, collision/shared-row ownership, and operation-record gaps remain honestly uncovered and unchanged. No new authority, operation, reads claim, or whole-A4 parity claim was introduced. P1/coverage remains on hold as directed.

## Verification

- `node --require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/dirname-preload.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx src/tools/video-editor/lib/project-transcript-host.test.ts src/tools/video-editor/data/typed/importTranscriptHandoff.test.ts src/tools/video-editor/commands/transcriptAssociateCapture.test.ts` — PASS, 4 files / 52 tests.
- `node_modules/.bin/eslint src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx --max-warnings 0 --report-unused-disable-directives` — PASS.
- `flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit --pretty false` — PASS.
- `flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit --pretty false` — PASS.
- `flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -b --noEmit --pretty false` — PASS.
- `git diff --check 6e04a9a9a7..HEAD` and `git diff --check` — PASS.
- No full, browser, live, HTTP/service, seed, P1, benchmark, or control suite was run.

## Blockers and next steps

Nothing blocks this review. Keep P1/coverage on hold; merge only through the orchestrator’s normal queue after this review. Preserve the documented legacy gaps until an approved mounted caller/provider contract supplies those semantics.
