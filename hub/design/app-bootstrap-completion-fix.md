# Bootstrap completion authority fix

2026-10-20. **KEEP; A1 source correction complete.** This remains an unwired local adapter/storage stage. Read PLAN and the independent review; no settled decision changed. No activation, Runtime forge/admission, or current provider-registration claim.

## Exact source and size

Worktree: `/home/user/work/wt/app-m2-bootstrap-completion-authority-fix`, branch `tl/app-m2-bootstrap-completion-authority-fix`; base `tl/app-m2-bootstrap-init-native-stage` at **f0112b846c1084b0902cdba091442cc840d8e88d**.

Final source = that base plus [source.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-completion-authority-fix/notes/source.patch), SHA256 **1460ea9a26c9540cf5050fa1c903e89fc191c2fd0c4fbba8f6102edd1ec0a409**. [Source audit](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-completion-authority-fix/notes/source-audit.json) records all four final file hashes/byte sizes.

| Changed file | Added/deleted lines | Final bytes |
| --- | --- | --- |
| `src/integrations/runtime/bootstrapInitialization.ts` | +79/-10 | 14,167 |
| `src/tools/video-editor/commands/commitOutbox.ts` | +6/-0 | 16,329 |
| `src/integrations/runtime/bootstrapInitialization.test.ts` | +208/-2 | 33,558 |
| `src/tools/video-editor/commands/commitOutbox.test.ts` | +72/-0 | 39,023 |

Total **4 files, +365/-12**; product **2 files, +85/-10**. Only the allowed adapter, existing owner retention and focused tests changed. No production caller/UI, package/root pin, server, wire, generated type or schema-file edits.

## Invariant and implementation

Completion requires the saved original native init intent and exact request, its scoped accepted result/receipt/revision-publication pair, the **same publication** in normal Runtime commit history, and the matching scoped immutable parent closure. A local `value.kind`, equal config, or today's head never supplies completion authority.

- The adapter checks the saved native three-command batch against the exact request, its original ready-base pair, scope/path and non-preview body. It checks accepted response commands/base, accepted revision and publication, scoped canonical document, both receipt copies and receipt result. It uses the same checks before accepting a new ACK, and validates the request before transmitting.
- Recovery searches the existing normal `listTimelineCommits` API through its cursors for the exact saved publication, then checks its revision, predecessor, receipt, recorded commands and provider/compiler/publisher metadata. Matching revision bytes under another publication do not qualify.
- The existing `getProjectParentCompositionRevision` immutable read must match project/timeline/revision, payload, digest and empty native-init dependency closure. The existing authoring-closure validator then opens that closure. No browser recomputation of acceptance hashes or provenance authority was added. These are existing generated API signatures passed through the source-only adapter ports.
- After historical proof, recovery still calls `loadLatest` for today's verified display basis. Later edits, complete undo and an equal-byte restore with a new publication remain successful without recapture/reinitialization or a requirement that today's head equal the init head.
- The existing strict outbox ACK transaction checkpoints `initialization = {intent, request, head, value}` in the **same owner record**, independently of rolling `accepted`. Later accepted edits/inverses preserve that original link. This is retained retry/link data, not a status authority, new journal or second store. Owners missing required original data fail closed and remain discoverable; no migration guesses completion from an older tag/result.
- Proof failure leaves the owner and retained data intact. Before ACK, malformed results keep the uncertain flight. After ACK, failed history/immutable proof keeps the complete original init checkpoint for another recovery attempt.

The new ACK clause is additive to creation retention, dependent `readyBase` and rejection handling. Existing render/placement continuation JSON, including a cancelled placement, survives init and later ACKs in a focused storage control. **Full D13/placement composition is not executed here**: when composing, keep this checkpoint, D13 render retention, placement acceptance linkage and dependent-base updates together in the same ACK transaction. Never choose just one branch's ACK block. The test proves opaque field preservation, not either other branch's admission lifecycle.

## Permanent counterexample and verification

All commands ran from `/home/user/work/wt/app-m2-bootstrap-completion-authority-fix` using the existing `/home/user/work/app/node_modules` symlink; installed Composition reports **0.0.10**, matching unchanged source Root10 pins.

First added the review counterexample using the **real generic outbox API**: store only `{kind: 'timeline-initialized'}`, release/reopen the owner, and offer pristine H0. Before the fix:

```sh
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts src/integrations/runtime/bootstrapInitialization.test.ts --maxWorkers=1 --no-file-parallelism
```

**RED: 1 failed / 20 passed**, because recovery resolved pristine H0 instead of refusing. [RED log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-completion-authority-fix/notes/red.log). The permanent assertion was not weakened. It now also checks owner retention and zero create/commit calls.

Final selection, after the last source/test change:

```sh
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitSession.test.ts src/integrations/runtime/bootstrapInitialization.test.ts src/integrations/runtime/createDefaultTimeline.test.ts --maxWorkers=1 --no-file-parallelism
```

**PASS: 5 files, 181 tests, exit 0; 10.64s.** [Final log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-completion-authority-fix/notes/targeted.log). The original **139 tests** remain included and passing; **42 new cases** cover marker-only completion, missing saved result, wrong scopes/base/commands/result/head/receipt, wrong or missing historical publication/recorded commands/metadata, immutable closure mismatches, paginated historical acceptance after edit/undo/equal-byte restore, later owner ACKs, atomic init ACK rollback/retry and continuation preservation. No skips, expected failures or weakened originals.

The adapter's original 20 test bodies and outbox's original test bodies are byte-identical; only their shared adapter mock gained the history/immutable read authority. `createDefaultTimeline.ts` and its entire test file are unchanged, preserving all original seven positives plus the existing additional headed-reuse positive. `bootstrapCapture.ts`, its tests, `commitSession.test.ts`, package/lock and the native golden are unchanged. Frozen golden source **31d02d45ad21f452724091b94b285478d00c9c21**, **15,448 bytes**, SHA256 **586f4b8ffc80a4d77162fdb739d9db6c469bda5827555c9de80f162950b0fc67**. Its App capture parity tests pass in the selection; no new native Python rerun is claimed.

```sh
node node_modules/eslint/bin/eslint.js src/integrations/runtime/bootstrapInitialization.ts src/integrations/runtime/bootstrapInitialization.test.ts src/tools/video-editor/commands/commitOutbox.ts src/tools/video-editor/commands/commitOutbox.test.ts
git diff --check
python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-completion-authority-fix/notes/source-audit.py
```

**All PASS, exit 0.** No lint diagnostics or whitespace errors. The audit enforces allowed-file scope and byte-identical original tests/golden/dependencies and saves the exact patch. Earlier edit-loop selections passed 21/1, 60/1 and 92/2; the final 181/5 selection supersedes them.

## Decisions, limits and next steps

The necessary init link belongs in the existing owner ACK transaction because `accepted` deliberately rolls forward. The discriminator only identifies adapter data; normal history plus immutable reads establish authority. Missing older saved inputs refuse completion and retain the owner, as required. No decision needed escalation and nothing blocks this bounded source fix.

All new tests use fake IndexedDB and mocked authority ports. This is a local adapter/storage counterexample and fix; it does not show Runtime accepted a forged command. No full, build, browser, tsc, install, sockets or central suite was run/requested. No current release/provider registration, actual server acceptance, real browser/disk crash durability, or combined D13/placement lifecycle was verified. No production import/caller of the reserve/resume seam was found outside its own file.

Recommended follow-up: review/land this bounded correction through the orchestrator; compose all existing ACK hooks without losing any continuation; then separately prove the official normal Runtime/Agent tuple with startup-registered native init, real Door create/H0/history/immutable closure admission, exact create/init retry through server/browser restart and lost/unpersisted ACK, later edits/undo/restore, headless same-ID repair, owner discovery/handoff and project metadata CAS. Production migration/zero-legacy traffic and release activation remain separately gated.

[Worker copy](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-completion-authority-fix/notes/report.md). `KEEP`, `commit-msg` and empty `DONE` are in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-completion-authority-fix`. No git commit/merge/rebase/checkout/push or ref mutation was performed; the harness owns the commit. No worktree build output or temporary artifacts remain.
