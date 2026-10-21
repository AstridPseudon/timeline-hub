# App ordinary-batch producer actual 0518 — result action

## Decision

**Prerequisite blocked; no product verdict and no cut prepared.** The one
new approved actual reached the central test service but failed before build,
browser launch, test collection, or producer-body execution. This is an
environment/setup command-contract failure, not an actual assertion failure.

The ordinary-batch row remains open. No legacy writer/helper can be retired
from this result because zero body assertions passed and zero live-caller
qualification was obtained.

## Exact source and central evidence

- App integration worktree at task start: `bc6f9dd39c7e5154ddf075cb87b7202cf5702e65`, tree `4cd13d09b7cffd60612d8521f1a2921ca4e762d2`.
- Frozen actual source keeper: `/home/user/work/wt/ap2-m2-producer-frozen-delta-luna-resume-0453`.
- Frozen source HEAD/tree: `17d2518c341c47a2d8634047b400399886da3a2a` / `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`.
- Approved wrapper: `scripts/testing/run-producer-public13-list.sh`, SHA-256 `87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0`.
- Approved external gate: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh`, SHA-256 `460d097995bd1d09938aeea54daeb6699030a20289eda78929132185961f26e7`.
- Central result: `ap2-m2-producer-frozen-delta-luna-resume-0453-ap2-m2-producer-literal-hash-first-cause-repair-0516-actual-1021052003-6793`, exit 2.
- Result packet: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-producer-frozen-delta-luna-resume-0453-ap2-m2-producer-literal-hash-first-cause-repair-0516-actual-1021052003-6793/`.

The exact approved central command was:
`test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh | cut -d' ' -f1)" = 460d097995bd1d09938aeea54daeb6699030a20289eda78929132185961f26e7 && test "$(sha256sum -- scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh run`.

The immutable gate accepts only `preflight|list` (lines 10–13 of the gate)
and returned: `usage: .../final-keeper-gate.sh preflight|list`.

Thus the failure occurred at the gate’s mode validation. It did not reach
`build:hosted`, Playwright, the ordinary producer body, or any product
assertion. This is distinct from prior command failure `14393` and no-body
result `14352`; neither is used as producer evidence.

## Callers and code changes

- Changed live callers: **none**.
- Product source changes in this worktree: **none** (`git status` clean).
- Shared dependencies, pins, generated files, DTOs, stores, selectors,
  assertions, timeouts, retry behavior, and fallback ownership: unchanged.
- Potential bounded legacy cut: **none prepared**. The actual did not prove a
  family, zero legacy traffic, or one-to-one test mapping.

## Tests and commands

- Read settled plan, App2 `STATUS.md`/`INBOX.md`, and `/home/user/timeline-hub/hub/status/app.md`.
- Central actual wait command: `wait-test` with result ID
  `ap2-m2-producer-frozen-delta-luna-resume-0453-ap2-m2-producer-literal-hash-first-cause-repair-0516-actual-1021052003-6793`.
  **FAIL, exit 2 in 2s; gate usage error before body execution.**
- No direct-neighbor App tests were run: there is no code change to validate,
  and the permitted actual stopped before product execution.
- No browser/full/install/live-socket/source-copy command was run by this
  worker.

## Required prerequisite / next step

The manager/orchestrator must reconcile the reviewed actual command with the
immutable gate interface (`run` versus accepted `preflight|list`) through a
separately reviewed source/runner correction. Only then may a newly approved
single actual be considered; this result must not be relabeled as product
failure or success and must not trigger a retry or deletion cut.
