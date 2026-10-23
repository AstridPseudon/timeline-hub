# A4 independent mounted transcript persistence review — FAIL

Reviewed `tl/app-A4-transcript-mounted-review-1921` at source SHA
`e5072135702b6c052f0eca97e99e0c9839896947`, tree
`9dd1c782a231f047aafaaa917ff6ee207fa98e96`, against PLAN §3 A2/A3/A4,
contract §§1–5, and the author brief. The candidate is exactly one added file
of 351 lines on `6e04a9a9a7`; `git diff --quiet 6e04a9a9a7 HEAD --
':!src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx'`
passed. No source, existing test, config, environment, generated file, kit,
pin, lock, or Git mutation was made by this review.

## Findings

1. **FAIL — the refusal case is an accidental retry, not A2 refusal handling.**
   The new transport returns a 409 body containing only `code`, `message`,
   `request_id`, and `details.reason/path/hint` (candidate lines 178–181).
   It omits the genuine v2 failure envelope required by the contract:
   `details.status`, `base`, `current`, `conflicts`, structured `code`, and
   `suggested_command`; the task also requires the actual head pair. With
   `details.status` absent and reason `dependency_changed`, the real client
   classifier falls through to `unknown` (`src/integrations/runtime/client.ts`
   lines 220–234). `localSaveSession` therefore records `retry`, not
   `rejected`, and its rollback path is never exercised (lines 102–121 and
   183–200). The test explicitly expects this outcome: `retry` and the
   optimistic transcript association still visible (candidate lines 337–339),
   with a message saying the transcript saved while the timeline association
   is unsaved (line 329). PLAN A2 requires a refusal to roll back or revalidate
   against the actual head with a user-facing message. This test proves neither
   and should not qualify the refusal path.

2. **FAIL — the accepted response is not a complete genuine v2 envelope.**
   The mock builds it from `acceptedCommit` and mutates only the canonical
   document, digest, commands, status, and receipt key (candidate lines
   191–201). The fixture's `data` has no authoritative v2 `steps` or effective
   `merge_mode` (fixture `timelineCommitFixture.ts` lines 70–85), although the
   contract requires both in accepted/merged replies. The test checks selected
   request fields and local adoption, but never validates response `steps`,
   `merge_mode`, `receipt.result`, or the full accepted reply. Thus the
   accepted path demonstrates serialization through the consumer, not a full
   Runtime-v2 reply binding.

3. **Coverage remains intentionally bounded and is not whole transcript
   parity.** The test does not mount the old config-mirror fallback, collision,
   shared-row ownership, or declared association-read cases. The author
   correctly reports these as unsupported/uncovered rather than inventing a
   `transcript.associate` operation or metadata authority. The existing
   detached capture tests and implementations remain byte-identical, but they
   cannot substitute for mounted persistence proof for those cases.

## What did pass

The accepted test does exercise the real mounted chain:

`useProjectTranscriptHost.associate` → `commitData(..., { save: true })` →
`useTimelineSave` local capture → `createLocalSaveSession` → durable
`commitOutbox` → `RuntimeDataProvider.commitTimeline` → generated client
`commitTimeline` transport. It asserts the canonical commit route, exact base
revision/publication pair, `doc.patch`, submitted step patch, serialized wire
body, idempotency header presence, preservation of raw/null/absent and sibling
planes, canonical head adoption, and empty outbox intents after acceptance.
There is no new `transcript.associate` producer; the only occurrences in the
new file are negative assertions.

The author-reported config-mirror/collision/shared-row/association-read gaps
are honest uncovered scope, not acceptance evidence. Keep A4/P1 and coverage
on hold until the refusal uses a full genuine Runtime-v2 envelope and proves
rollback or head revalidation with a message.

## Verification

- `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx src/tools/video-editor/lib/project-transcript-host.test.ts src/tools/video-editor/data/typed/importTranscriptHandoff.test.ts src/tools/video-editor/commands/transcriptAssociateCapture.test.ts` initially hit the repository config's ESM `__dirname` startup error; no files were changed.
- `node --import 'data:text/javascript,globalThis.__dirname=process.cwd()+"/config/testing"' node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx src/tools/video-editor/lib/project-transcript-host.test.ts src/tools/video-editor/data/typed/importTranscriptHandoff.test.ts src/tools/video-editor/commands/transcriptAssociateCapture.test.ts` — **4 files, 52 tests passed**.
- `flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit` — **passed**.
- `flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit` — **passed**.
- `flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -b --noEmit` — **passed**.
- `node_modules/.bin/eslint src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx --max-warnings 0 --report-unused-disable-directives` — **passed**.
- `git diff --check 6e04a9a9a7 HEAD` and `git diff --check` — **passed**.

No full, browser, live, service, seed, P1, or benchmark suite was run.
