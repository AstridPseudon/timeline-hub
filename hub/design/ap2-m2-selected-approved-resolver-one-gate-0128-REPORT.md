# AP2 M2 selected approved resolver one gate

## Result

The one approved central gate was run exactly once against App commit
`f490c60a11015c6bf1a80e167c3d7bea63aaed81`, tree
`5b9ec99d9670c5262b04c35bc9475379f9ef43be`. The selected journey was not
qualified: it failed before P1 at the existing connection-status assertion.

The browser could not find `[data-testid="runtime-connection-status"]` within
20 seconds. The trace shows the project and `Selected PARAM` timeline mounted,
but no connection-status element; the selected P1/P2 journey assertions did
not run. This is not evidence of a resolver refusal or of a native contract
failure after P1.

Central result:

- Test: `ap2-m2-selected-approved-resolver-one-gate-0128-ap2-m2-selected-real-p1-history-fixture-fix-1021013140-21610`
- Command: `sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh "$PWD"`
- Duration: 94s; exit 1
- Collection: 1 selected test in 1 file
- Hosted build: passed; 5,583 modules transformed, 46.09s
- Browser result: 1 failed, 0 passed; failure at `tests/e2e/local/support/app.ts:74`
- Trace: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace`

## Offline preflight

Before approval, only offline checks were run:

- `node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts` — passed.
- Playwright `--list` for the exact selected title — 1 test collected.
- `sh -n` on the existing central wrapper — passed.
- Exact tuple check — passed: Agent `8130a401...` / tree `236c3e57...`, Runtime `2c4ac180...` / tree `7ab412cc...`, Composition `0.0.13`, graph archive `895c628a...` containing Composition archive `9412ae25...`.
- `SELECTED_WORKSPACE_PREFLIGHT_ONLY=1` wrapper preflight — `selected DEV private workspace preflight: ready`.
- `git diff --check` — passed.

The canonical resolver custody review approved the exact candidate before the
central gate. No dependent run occurred before that approval. No retry, loop,
local browser run, full suite, or second central request was made.

## Source identity and scope

The worktree remained clean with 5,903 tracked files and no changed paths.
Selected source hashes are unchanged from the approved candidate:

```text
tests/e2e/local/support/harness.ts
05fa007055a42b121784559877ad31015bb477493fb02c6394d174eda37aef57
tests/e2e/local/support/selected-param-credential.test.ts
6a09d8f870ab87769dc5dcb818d50c539a82e659b1377911416f65beafb68402
tests/e2e/local/three-products.selected-param-dev.spec.ts
2cd9703de2282282a477f5661d600049c8507fb93df1ef0424a06e7978a8b6a0
```

No product source, assertions, pins, dependencies, generated files, or shared
worktrees were changed.

## Blocker and next step

The gate is blocked before P1 by the missing connection-status UI element. The
result does not justify changing the assertion, retrying the same source, or
claiming P1/P2/removal/refusal/dirty-draft/lost-ACK/restart/exact-retry/reload/
undo/zero-legacy behavior. The old pinned-source native-contract handoff to
matched current Agent `6ef` / Runtime `95bd` is not triggered because no P1
contract refusal occurred. The next step is a separately reviewed repair or
qualification of the existing connection-status surface, followed by a new
explicitly approved gate.
