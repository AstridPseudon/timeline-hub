## Report — app-P2-caller-whole-path-1130

Investigation completed read-only. No product, test, config, pin, lock, or source files changed. Worktree remains clean.

### Exact bounded result

- `ACTUAL26414`: **FAIL**, exit 2 in 2s.
- Failure boundary: D21 preflight, `Agent-source-or-tree` and `runtime-source-tree-lock-toolchain-markers`.
- Hosted build, beforeAll, seed, selector collection, mounted readiness, and all 8 original P2 gestures were **NOTRUN**.
- No daemon identity or product behavior is inferred.

### Complete source/admission map

- App source `d6ed8cbda122…`, tree `542b772e6dee…`, parents match the retained pure-product checkout.
- P2 Agent checkout:
  - source `333b44b1a1b8…`
  - actual tree `1094bf3662c…`
  - parent `079580ca46…`
  - clean and detached.
- Actual P2 row still expects Agent tree `2deab1a149…` — the old Agent079 tree. This is the confirmed deterministic mismatch.
- Runtime checkout is correct:
  - source `37eb6c7bdb79…`
  - tree `be4114705127…`
  - clean.
- Child receipt/key `188546b73edd…` is valid for Agent333b + Runtime37eb:
  - provision status `passed`
  - four client hashes and client identity `18f0ef33b9…` match
  - import origins are physically inside the child root
  - source/runtime/client markers match.
- Reused Runtime entry `5ca5c561…` and receipt `agent-remotion-app-ready-079-37eb-0258` are stale for P2:
  - `.astrid-agent-source-commit=079580ca…`
  - env and receipt also identify Agent079.
  - P2 requires Agent333b, so this guard must fail closed.
- Passing P3 row `23226c27…` correctly remains Agent079 + Runtime37eb and must not be rewritten.

The caller preparation artifact confirms the stale reuse: its replacement set rebases Agent checkout/child values but leaves the `REMOTION` runtime identity on the old Agent079 runtime. No relaxed guard is appropriate.

### Production caller evidence

The retained App path is intact:

`useTimelineCommandsService` → persisted `localSaveSession` outbox → `dataProvider.commitTimeline` → `operationHost.transmit` → Runtime commit route.

Relevant source behavior:

- Full base pair is carried: `base_revision_id` and `base_publication_id`.
- Request preserves commands, steps, reads, merge mode, label, source, rationale, group ID, and `dry_run`.
- HTTP sends the exact saved body with `Idempotency-Key`.
- Accepted responses retain canonical document, digest, commands, authoritative steps, IDs, publisher, receipt, and `accepted`/`merged`/historical `rebased` statuses.
- Conflict/invalid details remain surfaced without overwrite behavior.

### Commands run

- `git diff --check` — **PASS**
- `git status --porcelain=v1 --untracked-files=all` — **clean**
- No targeted/type/lint/full/browser/backend/provision reruns, per brief.

### Required next step

Sol1130 should rebind only the P2 caller artifacts to:

1. Agent tree `1094bf3662c…` instead of `2deab1a149…`.
2. A Runtime37eb artifact/receipt whose source marker and environment explicitly bind Agent333b.

Do not relabel the existing Agent079 Runtime receipt or rerun `26414` until both source-derived controls are satisfied.