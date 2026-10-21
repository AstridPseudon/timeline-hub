# AP2 M2 selected cold-mount approved gate

## Result

The one authorized cache-disabled central gate ran against the clean App tree
`1fac6ae549909acc9763a008eb7ca7e767bbf659` (HEAD
`0bcf2efe1e286de4951bbb823c938770a30d7a10`) and failed before selected P1
admission. The existing truthful source guard is present:

```ts
export const expectConnected = (page: Page) => expect(page.locator(UI.status)).toHaveAttribute('data-state', 'connected', { timeout: 20_000 });
```

No selector, connected-state expectation, seed ordering, credential path,
admission path, journey assertion, fallback writer, or product source was
changed for this gate.

## Preflight

The one private workspace preflight passed:

```text
TMPDIR=<private /tmp directory> SELECTED_WORKSPACE_PREFLIGHT_ONLY=1 sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh /home/user/work/wt/ap2-m2-selected-cold-mount-approved-gate-0055
selected DEV private workspace preflight: ready
```

It passed the existing frozen Agent8130/Runtime2c4 commit/tree checks, public
Composition13 graph/archive checks, private workspace create/inspect checks,
shell syntax check, clean-source check, and disk floor check. Temporary files
were removed by the EXIT trap.

## Central gate

Request:

```text
request-test ap2-m2-selected-cold-mount-approved-gate-0055 ap2-m2-selected-real-p1-history-fixture-fix --no-cache
```

Result:

- ID: `ap2-m2-selected-cold-mount-approved-gate-0055-ap2-m2-selected-real-p1-history-fixture-fix-1021005412-27230`
- Exit: `1` / fail, 97 seconds
- Build: passed; test collection selected exactly one test
- First failure: `tests/e2e/local/three-products.selected-param-dev.spec.ts:45`
- Assertion: real `[data-testid="runtime-connection-status"]` did not appear
  with `data-state="connected"` within 20 seconds

The retained sanitized Playwright context shows the real App mounted its
existing `Workspace Runtime is unavailable` panel with a retry action and the
configured editor origin. This is no longer the prior 5-second cold-mount
observation, but the selected journey still did not reach P1. The retained
causal trace is at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace`

Central result log:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-selected-cold-mount-approved-gate-0055-ap2-m2-selected-real-p1-history-fixture-fix-1021005412-27230/log.txt`

The earlier sanitized causal failure from gate `13123` remains documented in
`ap2-m2-selected-mounted-ready-causal-source-0049-REPORT.md`: boot shell and
empty root while the real Vite graph was loading. No selected P1/P2 history,
after-removal, refusal, dirty-draft, lost-ack, restart, exact-retry, reload,
undo, or zero-legacy assertion is claimed from this run.

## Checks and disposition

- `git diff --check` — passed.
- `sh -n .../run-central-selected-p1.sh` — passed.
- Private workspace preflight — passed.
- One central `--no-cache` gate — failed as above.
- No local browser/socket run, retry, full suite, pin, activation, system
  substitution, expected-failure change, assertion weakening, or fallback cut
  was performed.

The task is blocked at real Runtime connection readiness before P1; the next
step requires orchestrator direction on that connection failure. No further
run is authorized by this task.
