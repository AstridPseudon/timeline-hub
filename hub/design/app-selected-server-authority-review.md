# Selected PARAM server-authority independent review

**HOLD** on App `b9c03ef5ba705312dc36f37f4b7b5fa7fd0a784c`, compared with `080a5743`. The decided server-authority route is sound; the implementation has reproducible inverse/cancel and recovery defects. No product edits. The real paired journey's outstanding status is not the reason for HOLD.

Read PLAN.md, the App INBOX 08:36 decision, the staging report and native-provider oracle. App has no repository AGENTS.md/CLAUDE.md/CONTRIBUTING file. Delta is 9 paths, 312 net product lines, plus tests. Review source stayed byte-unchanged and git status stayed clean.

## Blocking counterexamples

All four are ordinary failing assertions in this worker's external `notes/counterexamples.test.ts`, using the existing session, outbox and synthetic normal-port transport. No passing repository test was changed. These prove source behavior, not browser/native integration. The projection spy rebuilds timeline data from the supplied basis; ordinary preview omission in that spy cannot explain parameter failures because the ordinary suffix only moves the clip.

1. **P1 — inverse ACK with retained selected intent leaves stale authored state; explicit cancel and fresh capture do not recover it.** Accept selected seed 4→8 at P1. Pause undo of P1, capture/submit selected seed 9 while the inverse is unacknowledged, then ACK the inverse at P2. The persisted accepted closure contains seed 4; the selected suffix correctly remains unsent with its original false accepted-basis flag. However the last projection remains seed 8. `commitSession.ts:194` only projects acceptance with a suffix when the ACKed payload has `selectedParams`; `undo()` builds its inverse with ordinary-looking `after: bundle` at line 599. The inverse is therefore missed. Counterexample 1 expects 4, receives 8.

   Explicitly undo/cancel the remaining selected suffix. The session reports `saved`, the outbox is empty, and the display projects seed 4, but `undo()` restores the canceled draft's stale `before` at line 588. A completely new capture contains seed 8 and `acceptedBasisAvailable: false`, despite no pending work. Counterexample 4 expects seed 4/true, receives seed 8/false. The original false flag was not rewritten; the NEW capture is wrong because the working bundle and accepted bundle diverged. This can keep fresh selected edits unsent after the user explicitly canceled the dependent draft.

2. **P2 — reload loses an already accepted selected value in the projection when an ordinary suffix is rejected.** Pause selected 4→8, append move to 5, ACK selected P1, then return typed conflict for the ordinary move. Before disposal the session projects accepted seed 8 with the original suffix. Persisted acceptance is P1 and only the exact original refused move remains. Reopen at the actual current P1 basis and explicitly recover that owner. `claim()` reconstructs acceptedBasis from saved acceptance at lines 525–527 but projects the ordinary tail's old displayBasis at line 529. Seed becomes 4 again and remains there behind the conflict. Counterexample 2 expects 8, receives 4. The accepted server record and original move payload remain intact: this is a display/custody-of-local-state defect, not proven server data loss.

3. **P2 — canceling an ordinary tail misclassifies a remaining selected draft.** Pause ordinary move to 5; append selected seed 8 (original unacknowledged basis), then ordinary move to 7. ACK the first move, leaving selected+ordinary unsent. Explicit undo cancels only move 7 and correctly retains the original selected draft/false flag. Line 594 nevertheless publishes `dirty` with null error, instead of `pending` with the unsent-basis explanation. Counterexample 3 verifies the retained draft and single wire commit before failing on status. Retry would restore pending; cancellation itself removes the required explanation.

Recommended bounded correction: handle accepted inverse effects and selected effects consistently when retaining suffixes; rebuild the working bundle from accepted state plus remaining representable ordinary edits after cancellation; retain accepted selected results during recovery without recapturing or rewriting original suffix guards/basis; derive cancellation status from remaining selected intent. Preserve ordinary move/label positive request bodies. Promote these external regressions into the main suites when implementing the correction. Do not solve them by fabricating a selected after-state or changing the original false accepted-basis flag.

## What the source and focused checks support

- `selectedParamsCommand` checks finite JSON, target identity, exact pin/argument shape and clear collisions; it imports no validator. Literal values, expressions and raw16 reach the normal provider transport unchanged. Prefetch is optional, so browser read failure is not a schema-semantic refusal.
- Selected payloads persist `after: null`, original capture/display basis, pin, retained input tuple and realm. No selected optimistic patch is fabricated. The existing mounted projection test keeps accepted seed 4 until ACK and then installs accepted seed 8 together with a newer ordinary move, without legacy save traffic.
- The existing exact request reservation/outbox is unchanged. Focused tests cover lost ACK, byte/key equality on recovery, original V1 inputs/pin despite simulated V2/removal, native inverse requests, typed422/refused409/conflict409 draft+suffix retention, and a selected capture newly made after ordinary acceptance. The V2/removal fixtures here do not mutate a real Runtime.
- The permanently unsent original unacknowledged-basis branch remains correctly gated at lines 154–156. Inputs/realm stay local; wire body remains native commands/base/source. No new DTO, endpoint, task creation, routing heuristic, browser export, install, pin change or schema authority was introduced. Command identity uses the prepared selected payload metadata, rather than treating every ordinary `after` shape as selected. The inverse findings above are the uncovered limitation of that classification.
- No generic compound selected producer is exposed by this staged port: it builds one native command per intent. Accepted mixed selected/ordinary suffixes have focused coverage; arbitrary mixed native command batches and inverse-with-suffix now require the correction/regressions above, not an unsupported qualification claim.

## Frozen Agent provider verification

Read actual Agent `931d7ec56dadffc2efdc893fec80b4c4aadf8a8e` with git show and reran an unchanged private copy of the staging oracle. `commit.py:350` hydrates the exact schema_source through existing config_source/document_object ports; `:878–883` executes the original base before `:884–904` server replay. `commands.py:190–208` verifies recorder fields only when supplied and creates authoritative records when absent. `_scalar_commands.py:134` uses the single native Draft202012Validator on changed declared properties, preserving literal opaque values.

Oracle PASS: absent client recorder claims, native V1 max10 accepts 4→8 and records the exact schema dependency; raw16 refuses using retained V1 after mutable V2/removal and JSON reopening; inverse/redo produce 4/8. Actual refusal is 409/status=refused, not 422. The App separately tests typed422 transport handling. The portable build receipt is synthetic, DetachedRealm/DetachedPort are in-memory fixtures, and JSON reopen is neither process restart nor durable Runtime idempotency/custody evidence. No browser validation requirement is reinstated.

## Exact commands and results

CWD for every command: `/home/user/work/wt/app-m2-selected-server-authority-review`.

The private configs mirror the existing config with absolute imports, runner-compatible dirname, no cache/file parallelism, maxWorkers=1, and an alias to a private extraction of this worktree's existing Composition 0.0.12 tarball. Shared node_modules is Composition 0.0.10 and was only read. The private extraction/cache was removed after testing; recreate the extraction with `python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-authority-review/notes/prepare-test-env.py` before reproducing.

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-authority-review/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/integrations/runtime/retainedParamInputs.test.ts
```

Exit 0: **5 files / 188 tests PASS**, 15.03s; `notes/targeted.log`. This is an independent subset of the reported 232/8-file staging run, not a claim to have rerun all eight files.

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-authority-review/notes/vitest.counterexamples.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism
```

Exit 1: **1 file / 4 ordinary counterexample failures**, 3.32s; `notes/counterexamples.log`. An earlier iteration contained the first three failures; the final run adds explicit cancel→fresh capture evidence and verifies the persisted inverse acceptance has seed 4. No skip, expected-fail or test weakening.

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-authority-review/notes/native-provider-oracle.py
git diff --check 080a5743 HEAD
git status --short
```

All exit 0: native probe PASS (409 refusal), whitespace clean, worktree clean. Native output/result: `notes/native-provider.log`, `notes/native-provider-result.json`.

No full or central suite requested; no build, tsc, browser, localhost/socket, dependency installation, git mutation or shared dependency/cache writes. FULL21209 was left alone. No product tests changed. Review task is complete; HOLD is the review result, not a worker blocker. No KEEP marker.

**Next:** App owner fixes the three bounded source defects and ports the four red requirements into main's suites, preserving the original expectations. Then perform the separately outstanding matching-tuple real V1 8/raw16 after V2/removal/process restart, lost-ACK exact retry, inverse/reload and zero legacy traffic journey. D01 remains OPEN; this report does not close the writer or qualify real custody, durable restart or a browser journey.
