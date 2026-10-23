# P1 raw trim requalification

- Base: `914afe21a449e379484977f16481099ffcc61e72` (`hub/tl/app-A2-trim-clear-fix-r3`); original corpus source `45642677bc781b1d6bc3f375f108c27aef64227e`.
- Only changed file: `src/tools/video-editor/hooks/p1RawHandoffCorpus.test.ts`.
- Before edit, trim `for`/`until` removals passed. The exact remaining oracle mismatch was only `parent_revision.revision_id` and `parent_revision.content_digest`: semantic-executor output metadata versus local pre-acceptance `parent-1` / `sha256:f8784c8e1fe293ff4ac0a5f3017a0d320c837fe66ab388ccdb30b54fbe72dcbf`.
- The test now compares the complete authored payload closure exactly (parent, shot, internal-timeline payloads), while separately requiring original project/timeline/base revision/base digest. All five deltas and before values, opaque/null/absent/order/mirrors, no-send, and outbox guards remain.
- Local targeted command: raw handoff plus neighboring handoff tests pass (`20 passed`); the eight unchanged corpus provenance checks fail only because sandbox `spawnSync git EPERM` blocks `execFileSync('git', ...)` at `p1FeasibilityCorpus.test.ts:36`. Central targeted service result: all 3 files and 28 tests pass; log `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-P1-raw-trim-requalification-0210-targeted-1023021118-25902/log.txt`.
- `node node_modules/typescript/bin/tsc --noEmit`: pass. ESLint targeted: pass. `git diff --check`: pass.
- Production caller is not mounted: `useTimelineState` → `useTimelineSave` stages the original read, but persistence receives no `localDocumentSave`; non-test source has no handoff/session constructor. The outbox chain is test-local evidence only.
- Full v2 request/reply fields, authenticated preview/history, and accepted/merged Runtime activation remain unverified. No H3 GO/P4 DONE claim.
- Next owner: App A2/integration to mount the durable handoff/session and connect v2 transport; central/service or owner to disposition the unchanged provenance check.
