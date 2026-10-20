# APPROVE — automatic-placement outbox storage only

Reviewed 2026-10-20. Candidate **f89cc8da5ca34f395a8bd99afc552015bb60d6cd**, tree **6cbd005f896ab6314bdcfefcec186ffb0a4fc113**, against original render-storage **c195d1ee19464692712857d65648e91a9b93bee3**. Read PLAN first, requester-continuation appendix, port contract, candidate report, complete outbox source/tests, session tests/recovery/undo and bootstrap storage delta. No plan decision changed.

**APPROVE this bounded, inactive local-storage change. No blocking counterexample found in the candidate. This verdict does not authorize activation, legacy-writer deletion or a release.** Product source and tests remain unchanged by this review.

## Scope and evidence

The actual delta is two files: `commitOutbox.ts` +143/-3 (net +140; 517 final lines), `commitOutbox.test.ts` +362/-0 (1188 final lines). Three claimed-owner methods and one optional record array reuse database `astrid.command-outbox`, store `owners`, version 1. No second store, coordinator, background runner, DTO or generic trigger framework.

From `/home/user/work/wt/app-m2-auto-outbox-readonly-review`, physical `node_modules` resolved to `/tmp/app-m2-coherent-deps8/node_modules` after repointing only this worktree's ignored symlink:

```sh
node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitSession.test.ts
```

**PASS: 2 files, 79 tests, exit 0; 6.08s; start 07:34:32 UTC.** All original 67 cases are included. A Python source comparison against `git show c195d1ee19464692712857d65648e91a9b93bee3:<path>` additionally confirmed every original outbox-test line remains in order (826 → 1188) and the session test is unchanged (454 → 454). No original passing expectation was replaced with refusal, skipped, deleted or weakened.

```sh
node_modules/.bin/eslint src/tools/video-editor/commands/commitOutbox.ts src/tools/video-editor/commands/commitOutbox.test.ts
```

**PASS: exit 0, no diagnostics.** `git diff --check`: **PASS, exit 0**. Read-only source assertions also confirmed unchanged database/store/version, strict transaction options, and no owner deletion/clear path. No new counterexample test was needed. No full/build/browser/tsc/install/socket run or test-service request.

## Boundary review

Source references below use the reviewed worktree: `commands/` means `src/tools/video-editor/commands/`; bare line references continue to `commitOutbox.ts`.

| Requirement | Source and conclusion |
| --- | --- |
| Pre-POST storage; ACK-first | `commands/commitOutbox.ts:174-187,361-377`: finite detached required bindings, explicit autoApprove, nonempty unique birth IDs and canonical task route are frozen before the reservation promise resolves. New reservations refuse queued/pending ordinary edits. An exact existing reservation remains recoverable even if later edits exist. Tests cover missing fields, missing approval, abort-before-POST and unsaved work. The future caller must await reservation before sending; this module has no task sender. |
| Frozen original request and capture basis | Exact method/path/serialized body/key plus original revision/publication, closure, owner/anchor/lane/fallback/policy/output and IDs are retained and compared on repeat. Changed input refuses without replacing saved data. Storage never refreshes a head or computes placement from today's preview. Unknown admission outcome leaves the same reservation without a locator; exact retry bytes are available, although no actual task POST/replay was executed here. |
| Scope and ownership | `scopeKey`, `own`, `access` retain full realm/actor/project/timeline/owner separation, whole-claim browser exclusion and persisted generation checks on mutations. Detached inputs/results cannot mutate stored state. Browser locks are required unless explicitly injected by tests. Wrong scope, second claim, released claims and late superseded captures are covered. Authentication of the supplied identity remains the caller's responsibility. |
| Original task locator | `:379-394`: saved request must match exactly; project must equal owner scope; run/task IDs must be nonempty and immutable. Abort retains the previous reservation. This validates a local locator shape, not a Runtime result's authenticity. |
| Capture and atomic linkage | `:396-435`: selected pin is durably reserved first; capture runs after that transaction completes, outside IDB. The second owner transaction queues the original payload with the original head and links its new intent ID together, or queues zero on abort. Same-ID overlapping captures refuse. The final transaction rechecks claim generation. Lost callback completion cannot mutate a newly claimed owner. |
| Failure and cancellation | Durable capture failure retains original bindings/pin and a visible conflict; duplicates do not invoke capture again. Unsent linked-intent cancellation retains `placement.cancelled`; uncertain requests cannot be cancelled. A crash/abort before linkage or before failure persistence can rerun the pure capture with the same pin/IDs; it cannot duplicate a committed intent. No exactly-once callback execution is claimed. Cancellation of a task before capture is a future authenticated consumer/task-read obligation; storage does not itself cancel tasks. |
| Ordinary ACK, later B/C and inverse | `:465-478`: the normal ACK transaction writes `placement.accepted` before pruning the pending request/intent. Later rolling `record.accepted` updates do not overwrite the retained continuation acceptance. Lost/aborted ACK retries exact original commit bytes/key without running the builder. Existing D13 render continuation creation remains in the same ACK transaction. |
| Retention through undo/reload | No candidate mutator removes `placementContinuations`; `cancel` adds a terminal link and inverse is an ordinary new intent. Restart tests cover linkage before/after append, lost/aborted ACK, B/C and inverse followed by another restart/duplicate. No link-pruning/rearming path found. The inverse test proves local linkage retention with a mocked acceptance, not actual guarded Runtime undo. |
| Discovery | `:234-244`: realm/actor discovery can optionally filter project/timeline and returns task-only and accepted-only records, including their original scope. Full-scope matching is preserved. **Current `commitSession.ts:279` still filters to intents/pending**, so the editor does not yet expose or resume task-only/accepted-only continuations. This is a documented inactive consumer boundary, not completed reconnect behavior. |

## Original authority remains external

The request/input/pin/callback payload and `OutboxOutcome.kind` are finite local carriers. Neither JSON nor an `accepted`/other local kind certifies a canonical document, producer result, task attempt, scope or permission. Tests intentionally use opaque example pins and mock acceptance; they do not claim otherwise.

The candidate adds no inline provenance, credential, lease or synthetic task-attempt guard field. Reservation and locator inputs explicitly project their allowed top-level fields; extra credential/lease fields there are discarded. **Opaque nested JSON and serialized request bodies are not recursively credential-sanitized.** A future adapter must never pass credentials/worker lease authority inside them. It must validate authenticated scope, immutable closure/head, approved bindings/output, task/run/result and managed selection through existing official Agent/Runtime authority; use the Agent deterministic recipe with saved birth IDs; and validate normal responses before passing storage outcomes. Storage cannot prove a callback consumed its saved closure/IDs, cannot interpret arbitrary commands, and must not become that authority.

## Bootstrap and D13 composition

Read bootstrap candidate **f0112b846** and its parent delta without switching branches. It adds `{create:true}`, `reserveCreate`, project-only discovery and `accepted.creation = {payload, request}`. Its ancestor lacks D13; the whole-file diff against c195 therefore shows absent render support because of branch ancestry, not an intentional deletion in the bootstrap commit.

Composition is source-feasible but **not executed or qualified here**. Preserve both sides of the overlapping `list`, `append` and ACK changes: realm/actor optional-filter discovery subsumes bootstrap's project query; `append` must retain the create-basis guard and optional afterAcceptRender; ACK must both retain bootstrap creation data on a create acceptance and maintain D13/placement continuations before pruning. Keep the creation field in the compatible accepted type. Ordinary clone/read-modify-write retains existing finite JSON fields; do not replace owner rows with a whitelist or reset the database/version.

Concrete integration hazards to avoid: choosing the bootstrap file wholesale would remove D13/placement methods and retention; choosing this file wholesale would remove bootstrap reserveCreate/creation behavior. A bootstrap `reserveCreate` composed unchanged also considers a task-only owner with no intents/pending/rolling acceptance unused: tighten that precondition for retained continuations rather than reusing such an owner. The bootstrap branch's pre-existing `resolveRejected` can remove/replace queued work; if extended to linked placements, explicitly retain a cancelled/replaced terminal disposition so the continuation does not point forever to a removed intent. These are future composition obligations, not observed defects in the reviewed candidate, which exposes neither method. Require focused composition tests preserving legacy owner data, creation retry, D13 linkage and placement ACK/cancellation/restart before accepting that combined source.

## Specific lifecycle debt and qualification limits

Retention is deliberately conservative, **not bounded**: each continuation keeps request bytes, closure, pin, IDs, locator and terminal acceptance/value indefinitely; D13 retains its own accepted values too. Whole-owner JSON is cloned and rewritten on access, and `list` reads all owner rows before filtering. Accumulating task/completed/cancelled/conflicted records therefore increases transaction bytes, serialization/list costs and eventual quota pressure; repeated fresh empty owners also accumulate. Storage failure refuses before task POST rather than authorizing an unsafe reset. The review adds no retention framework, consistent with PLAN's deferred policy.

Before sustained activation, define a narrow authorized terminal checkpoint/quota policy that keeps durable deduplication/linkage for replayable tasks through undo/reload and pending retries. Deleting linkage merely because the queue is empty, the editor closed or undo succeeded is specifically unsafe. Bound retained immutable data rather than expanding this carrier into a second document/provenance ledger. Eviction/manual browser-data clearing and replay after cleanup remain unqualified.

The implementation requests IDB **strict** durability and resolves mutations on transaction completion. The repository fake IDB ignores durability and lacks native rollback; the existing test wrapper injects rollback/abort suppression for selected fault windows. Thus the passing tests establish local storage transaction ordering and modeled atomicity/recovery, **not real-browser fsync/power-loss durability**, actual browser-lock scheduling, Runtime acceptance/idempotency, provider/capture correctness, task/attempt fencing or real canonical reload/guarded undo/redo. They cannot activate automatic placement.

## Decisions, blockers and next steps

No product edits, plan deviation, new authority or discretionary judgment change. ACK-first and three existing-owner methods match the settled brief. No blocker to this storage-only approval.

Next: compose storage changes with bootstrap/D13 and prove data preservation; implement the separately scoped authenticated requester/reconnect adapter and Agent capture using original saved bindings; qualify the exact official Agent/Runtime/provider/client tuple with real task-admission and commit ACK loss/restart/replay, managed-output/task fences, canonical reload and guarded undo/redo before activation or writer retirement. No owner-film, macOS, full-suite, browser or release claim.
