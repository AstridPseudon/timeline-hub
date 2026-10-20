# Gate 5 scenario map (M2) — coverage and minimal additions

Gate 5 (PLAN §6): App edit → intervening Agent edit → lost ACK → newer local edit → exact retry → restart/reload → undo; preserved intent asserted.
Read-only review. Paths: `app/` = `/home/user/work/app/tests/e2e/local/`, `rt/` = `/home/user/work/runtime/tests/`, `ag/` = `/home/user/work/agent/tests/`.

## A. Step → existing coverage

| # | Gate-5 step | Existing coverage (file:line) | Status |
|---|---|---|---|
| 1 | App edit A, accepted, ACK held | `app/three-products.spec.ts:840` "M1 real gesture" → `prepareDependentMoves` :784 (drag A, `wire.posts[0]` accepted, attempts==1) | Covered |
| 2 | Intervening Agent edit | `three-products.spec.ts:846` `astrid.commitCaptured(… track C …)` on base A (disjoint). Conflicting variant: `:969` (Agent moves same clip to 6) in "M1 real dependency conflict" :953 | Covered (split across two tests) |
| 3 | Lost ACK | `three-products.spec.ts:666` `faultFirstCommit` (commits in Runtime, `route.abort` on held response); `loseAck()` :695, called :849 | Covered |
| 4 | **Newer local edit AFTER lost ACK** | B is dragged in `prepareDependentMoves` :800–:830, i.e. **before** `loseAck()` at :849. Order in test is A → C → B → lostACK → reload → restart → recover → retry | **Order gap** (B precedes lost ACK) |
| 5 | Exact retry | `three-products.spec.ts:881` `wire.posts[1]` equals `posts[0]` (same body and key); conflict variant :977. Runtime: `rt/test_timeline_commit_integration.py:298` (`replayed == accepted`, `forbidden` provider patch), `rt/test_timeline_commit_acceptance.py:180` identical retry after restart | Covered |
| 6 | Restart / reload | `three-products.spec.ts:851` `page.reload()`; :859 `harness.restartRuntime()` (`app/support/harness.ts:493`, returns `oldInstanceId`); reopen + `Recover saved edits` [data-owner-id] :877–:879 | Covered |
| 7 | Undo | `three-products.spec.ts:910` UI `Undo` button; inverse body asserted :912–:917. Runtime: `rt/test_timeline_commit_integration.py:298` tail (`door-undo`), `ag/tests/sdk/test_timeline_commit_provider_runtime.py:93` inverse+redo after restart | Covered |
| 8 | Preserved intent asserted | B commands equal original intent (:887), B at 7 (:890) with C track kept (:891, :924), no legacy POST (:944) | Covered |

Legacy tests that look like gate 5 but use the retired snapshot-save path (`SAVES`, not in `e2e-m1-gesture`): `three-products.spec.ts:403` "concurrent edit … acknowledgement is lost … keeps its draft" and `:573` "Runtime restart with the App open". Their intent is the closest old match; their commit-path successors are :953 (conflict) and :840 (restart). Under M2 they must be `it.fails`/xfail with a requirement comment, not deleted.

## B. Minimal additions

| Need | Owner | Addition | Exact name |
|---|---|---|---|
| Gate-5 ordering (B after lost ACK) | App | New case in `three-products.spec.ts`. Split `prepareDependentMoves` so the caller can run `loseAck()` + wait for `outcome.kind === 'retry'` before the B drag (add an optional `ackLostFirst` or a `beforeBDrop` ordering flag; do not change the existing M1 test). Assert B is unsent (`wire.posts.length === 1`) and queued behind A. Then reload → restart → recover → exact retry → B rebased at 7 → UI Undo. Title must start `M1 real` so `e2e-m1-gesture` (`--grep 'M1 real'`) picks it up. | `M1 real gate 5: intervening Agent edit, lost ACK, newer local edit, exact retry, restart and undo keep intent` |
| Open product question | App | Whether the mounted editor accepts a new gesture while the owner is in `retry` (pending A, ACK unknown). The plan says B queues behind A; the test should assert that, and fail (not skip) if the UI blocks it. | — |
| Runtime restart hook | Runtime / harness | **None new.** `harness.restartRuntime()` exists (`app/support/harness.ts:493`) and `/v1` handshake exposes `runtimeInstanceId`. | — |
| Lost-ACK fault injection | App (test-only) | **None new in Runtime.** Client-side `route.abort` in `faultFirstCommit`. Runtime already simulates it at door level (`rt/test_timeline_commit_integration.py:298`). | — |
| Runtime-side gate 5 chain | Runtime | Already covered by `test_real_door_lost_ack_restart_exact_retry_never_executes_provider`. No change. | — |
| Agent CLI side | Agent | Already exercised: App journey uses real `astrid` CLI (`app/support/astrid.ts:194` `commitCaptured`). No change. | — |
| Legacy tests :403, :573 | App | Mark `it.fails` (strict) under M2 with comment naming gate 5 + M2 legacy removal, if they fail once legacy save is removed. Do not delete. | — |

Runtime needs nothing new for gate 5; the only missing piece is the App ordering case.

## C. Commands (central service, from the orchestrator's `tests/suites.conf`)

Run from a worker whose meta repo is `app` (or `integration:app`):

```
# App: named suite; picks every test whose title starts "M1 real" (includes the new gate-5 case)
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test <app-worker> e2e-m1-gesture) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test $R

# App: whole three-products file (adds legacy :403/:573; expect failures unless xfail-marked; heavy, once only, after last change)
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test <app-worker> full-e2e-three-products) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test $R

# Runtime door lost-ACK chain (gate 5 at Runtime level)
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test <runtime-worker> commit-integration) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test $R

# Agent CLI/provider restart + restore/redo (in opaque-preservation-integration)
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test <agent-worker> opaque-preservation-integration) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test $R
```

Run order: `e2e-m1-gesture` first (fast, targeted). Request `full-e2e-three-products` at most once, after the last change. Each `request-test` needs the worker's own name or `integration:app` as the target.

## D. Caveats

- Ordering in the existing M1 test is A → C → B → lost ACK, not the gate's A → C → lost ACK → B. The existing test is not changed; the new case is additive.
- Coordination doc says the Retry control is `Retry exact request`; the spec (`:974`) and the later handoff use `Retry save` with `data-testid=timeline-command-retry`. Use the spec's names.
- This review ran no tests. Everything above is from reading the files and grep.
