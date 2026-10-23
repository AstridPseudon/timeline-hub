# A4 mounted composition review — 2008

## Result

PASS for this bounded three-file composition review. The branch remains HOLD: this does not establish P1 GO, complete A4 parity, or authorization to remove the retained legacy behavior.

## Scope and identity

Candidate: `tl/app-A4-mounted-reviewed-compose-2003` at `da7f25f0546ada65c224c650488a79a9ff0e1440`.

Held base: `6e04a9a9a757eceeca7e7e563c5efb160f5e2fcb`.

The complete candidate delta is exactly these three additions:

- `src/tools/video-editor/hooks/useTimelineTrackManagement.persistence.test.tsx`
- `src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx`
- `src/tools/video-editor/hooks/useTimelineCommandsService.persistence.test.tsx`

Exact donor blob checks passed:

- Track donor `tl/app-A4-track-mounted-return-1938`, reviewed by `app-A4-track-final-review-1949`: `e307e5ea351d927456aee9493ddc27d43076d8ed`.
- Transcript donor `tl/app-A4-transcript-mounted-return-1930`, reviewed by `app-A4-transcript-final-review-1941`: `8d223d33d4b89f300a7ca536ffc40e905f2b499b`.
- Prepared-media donor `tl/app-A4-after-mounted-return-1954`, reviewed by `app-A4-after-mounted-final-review-1958`: `626128c0210deab78f650a4620ad846bdcd96cbe`.

The transcript donor is correctly materialized at `lib/project-transcript-host.persistence.test.tsx`; the earlier hook-shaped name is not present.

All ten files already changed by the held base are byte-identical to `6e04a9a9a7` (four travel-between-images files, `media.test.ts`, `VideoEditorProvider.tsx`, `importTranscriptHandoff.test.ts`, `useTimelineState.types.ts`, `useTimelineTrackManagement.test.ts`, and `project-transcript-host.test.ts`). No outside file changed and the worktree is clean.

## Mounted-path review

The three witnesses exercise the intended mounted chain through `useTimelineSave`/the persisted outbox and `RuntimeDataProvider`; the runtime client delegates to the generated `WorkspaceClient` transport.

- Track management covers exact request path/body and idempotency key, canonical accepted adoption with receipt/steps, and a structured 409 using `details.current`, preserving rejected intent and rollback state.
- Transcript host covers the actual import/association host, exact serialized request and key, complete accepted `data` plus `receipt`, canonical adoption, and refusal classification/message with pending request retention.
- Commands service covers the actual prepared-media caller, guarded command serialization, canonical accepted result/receipt integrity, and a real structured conflict using `details.current` with rollback, retained intent, and user message.

The union includes the original `trackReorderCapture`, `parentAfterAnchorCapture`, and `transcriptAssociateCapture` behavior tests unchanged. No test-control skips or focused-suite weakening were found. The reviewed independent findings remain bounded: raw positive/refusal preservation, same-order operation-record behavior, and broader reconciliation/preview differences are still gaps, not silently credited.

## Verification

Environment: Node `v22.22.0`, Vitest `4.1.5`.

- `NODE_OPTIONS="--require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-A4-transcript-review-1815/vitest-runner.cjs" node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/hooks/useTimelineTrackManagement.persistence.test.tsx src/tools/video-editor/hooks/useTimelineCommandsService.persistence.test.tsx src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx src/tools/video-editor/commands/trackReorderCapture.test.ts src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts src/tools/video-editor/commands/transcriptAssociateCapture.test.ts` — PASS, 6 files / 34 tests.
- `flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 bash -c 'node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit --pretty false && node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit --pretty false && node node_modules/typescript/bin/tsc -b --pretty false'` — PASS.
- `node node_modules/eslint/bin/eslint.js src/tools/video-editor/hooks/useTimelineTrackManagement.persistence.test.tsx src/tools/video-editor/hooks/useTimelineCommandsService.persistence.test.tsx src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx --max-warnings 0` — PASS, zero warnings.
- `git diff --check` — PASS.

No full, browser, HTTP/live-body, service, seed, benchmark, or P1 suite was run, per the brief.

## Next step

Keep the branch on HOLD pending the original P1 GO and the remaining A4 coverage work. Preserve all old tests and implementations; do not merge this review branch or claim blanket A4 completion from this bounded PASS.
