# Ordinary native CLI review — APPROVE WITH INTEGRATION REQUIREMENTS

Approve bounded candidate **`346e14bd0dbed20d1aa55f3a0c4fcff00e76f004`**, based on **`6a595224`**, for composition onto current **`7970544b`**. No blocking semantic source finding or PLAN disagreement. No product fixes or generated/pin edits made.

- Complete five-file diff inspected. Existing ordinary grammar and native subparsers preserved; only ordinary `--dry-run`, `--idempotency-key`, `--json` added. Existing positive hold/duration, clear and other detached tests still pass. No existing test edited, skipped, weakened, or converted from success to refusal.
- Native trim uses unchanged `6a595224` capture/interior policy and one `TimelineSession` durable outbox. Exact body/key persist before POST. Original guards, pending suffix and original-base retry survive; no JSON-diff writer, refreshed pending claims, second outbox or new DTO. Lookup maps raw parent/occurrence ownership explicitly, without decoding display IDs.
- Independent candidate probes: **174 passed in 11.80s**. Additional actual CLI golden/relevant-conflict probes: **2 passed in 1.47s**. Golden records/output agree; relevant peer trim produces a real replay conflict retaining pending command/base/flight/body/key and the complete outbox file on identical retry. Current publication redo/history probes: **12 passed in 2.88s**.
- Verified actual central summary/snapshot/log and source: candidate tree **`8eb174e86ca81816424b8a94cc23d4e242545025`**, normal pinned Runtime **`94114269d1ce23ab3224d7eca5a85138ce2b5fed`**, **5 passed in 12.89s** (`...identity-pin94114269-integration-1020111607-32126`). Exact-candidate pair evidence reused, not rerun; service/store reopen is not process-kill recovery.

Required merge composition with in-flight frontend **`bdf88327`**:

1. `cli.py::_cmd_commit_edit`: retain BOTH ordinary `edit` callback/`NotImplemented` fallback and native `sheet` dispatch, draft validation, preview/unchanged rendering and edited-file diagnostics. Keep both keyword options and existing batch/command/undo/move paths.
2. Keep ordinary `_cmd_edit`/`_configure_edit` additions AND native frontend show/apply additions. `sync.py` changes are separate functions: retain new `trim` AND frontend `commit_many(..., base=None)`/`_stage(..., base=None)` original-sheet-basis fence. Only these two product paths intersect the frontend patch.
3. Preserve **`5430a971`** publication redo dispatch/options/help/test and current checkout/history/recovery code. Both candidates have older bases: apply narrow changes, never copy their whole trees. Preserve current sheet client-aware history lookup; prior frontend review identifies two old-context lines needing adjustment.
4. Regenerate `cli-surface.json` and `artifacts.json` from the combined source through their owners. Read-only checks currently fail: surface says **`timelines edit: changed`**; artifact says **catalog changed**, with both flagged files byte-identical to `6a595224` (pre-existing). No manifest edits performed here.

Ordinary candidate `git apply --check` passes against current integration; source and worktree diff checks pass, assigned repository stays clean. No actual merge or combined qualification. No M2/all-writer-retirement claim: ordinary duration/params/clears, occurrence trim, compound edits and existing detached paths remain live. Next: compose preserving history, regenerate manifests, then targeted mixed-outbox/ordinary/native-sheet/redo and central named pair qualification. No full requested or run.

[Detailed report, exact commands, development probe failures and limits](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-cli-ordinary-native/notes/report.md).
