# AP2 M2 selected existing runner: current 0844 binding

## Result

Retained exactly one owned selected runner, copied from the immutable 0724
artifact and stored at:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-existing-runner-current-bind-0852/artifacts/run-owned-selected-final95.sh
```

Its empty durable lease marker is alongside it at `artifacts/KEEP`. No App
product/spec/harness file, shared helper, pin, role, launcher, framework,
source authority, grant, or dependency was edited. No actual selected run was
performed.

## Exact binding delta

The runner's whole-file SHA-256 changed from the retained 0724 artifact
`dcda1b820fa2feb68db6ae99b56cdc8cd4277016c3eaf939a5ded423c9b25ee0` to:

```text
266212583458c600bc3248401b40cb9cba5bc4c66068b3b5e65e0503b0405238
```

The only changes are these bindings:

| Binding | 0724 | final 0844 |
| --- | --- | --- |
| owned record / KEEP | `workers/ap2-m2-selected-actual-path-four-custody-fixes-0707` | `workers/ap2-m2-selected-existing-runner-current-bind-0852/artifacts` |
| App source HEAD | `ba02c8f246ec61cd65d178a1ada686788df3fdab` | `a50ca4a0172cce9c73ce3c040290bf9479098b0f` |
| App source tree | `7fe8c15b56da9944ae31e8273d41d3ceb21b3677` | `92391f9a57dd38ce327b0a63990725053ea34601` |
| App base / HOME ancestor | `42b0c6c8434e2c491f8dbdf00a210ed755e41a95` / `fa887b5689d7ad44957021080f74d13a9d0c4e30` | `32b74fdea165816226b6f0727a16817a6a1a79c3` / `a3ddc2997e6460bab77d1e4ef7c1ac98ee21ad65` |
| harness SHA | `af61e605e1930ae061506a317008d670c7c1be01511c7c1a57188a6a91cc0465` | `1585677bafef583110e86a04a4490a968a8db499b0e9d566c6b890eab228ce6c` |
| shared helper expected SHA | `d9a691dcaafd7d544a467445a3a020a9ad3d02afc1d527870f00be6948fea848` | `a0ed2bd7d6688799f22bc8f17f89631c603e4e692a8d5e71f3ee3b26437b27b3` |

The last row is a runner-side custody correction, not a helper edit: the
unchanged current helper is `a0ed2bd7…` as recorded by the 0844 freeze. The
helper contains zero `final95:selected` roles and retains exactly its existing
`final95:parent` and `final95:bootstrap` roles. The 0724 `d9a691…` expectation
was stale; leaving it would not bind the runner to the current unchanged
helper.

All other bindings are unchanged: selected spec SHA
`10250fa44db4e2d4423f8d06258105df267e3ba4e29700d700bb1d3182a6def1`, Vite
config `5f26c8fa…`, discovery proxy `93989e63…`, Agent
`6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree `2ed2b8a1…`, Runtime and
producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / tree `d3a290b…`,
76-artifact manifest/version, Composition graph, Node/Vite/Vitest/Playwright
versions, origin, credential FILE, argv, cleanup, and all refusal controls.

## Source and assertion custody

The final source is committed App `a50ca4a0172cce9c73ce3c040290bf9479098b0f`
with tree `92391f9a57dd38ce327b0a63990725053ea34601`; its direct parent is
the required HOME32b ancestor `32b74fdea165816226b6f0727a16817a6a1a79c3`
with tree `a3ddc2997e6460bab77d1e4ef7c1ac98ee21ad65`. The source worktree was
clean.

The selected spec is byte-identical to the approved original: its SHA is
`10250fa44db4e2d4423f8d06258105df267e3ba4e29700d700bb1d3182a6def1`, and
`git diff --quiet 8e9975005d18c6278000ab4c8cc8b18291d03e12 HEAD --
tests/e2e/local/three-products.selected-param-dev.spec.ts` passed.

The exact original conversion mapping remains the one approved in
`ap2-m2-selected-mount-precondition-conversion-review-0315-REPORT.md`: the
initial `page.goto()` boundary, the first reload after P2/source removal, and
the second reload before draft recovery each replace the original
`expectConnected(page)` wait with the existing same-origin `expectAppMounted`
wait, all with the original 20-second timeout. That review explicitly records
that same-origin DEV has no hosted RuntimeConnectionGate status pill and that
the selected timeline, clip, parameter, P1/P2, refusal, draft, lost-ACK,
restart/reload, exact retry, undo, and zero-legacy assertions remain. No
absent hosted status-pill check was substituted and no assertion was weakened.

## Reverse-diff proof

`diff -u` from the 0724 runner to this runner showed only the owned-record
path, App source/base/harness identities, and the current helper digest above.
Applying that diff in reverse to the final runner and comparing bytes with the
0724 artifact passed:

```text
reverse apply + byte comparison: PASS
```

The shared helper check also passed directly: current helper SHA
`a0ed2bd7d6688799f22bc8f17f89631c603e4e692a8d5e71f3ee3b26437b27b3`,
`final95:selected` occurrences `0`, existing parent/bootstrap role matches
present.

## Final bounded preflight

Syntax and the final bound preflight passed:

```sh
RUNNER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-existing-runner-current-bind-0852/artifacts/run-owned-selected-final95.sh
sh -n "$RUNNER"                                      # PASS
SELECTED_FINAL95_MODE=preflight "$RUNNER" \
  /home/user/work/wt/ap2-m2-selected-existing-runner-current-bind-0852
```

Result: `CHEAP PREFLIGHT PASS`, all 11 aggregate checks passed. This included
source ancestry and exact spec bytes; final95 Agent/Runtime/producer and all
76 artifacts; locked Composition graph; exact Node/Vite/Vitest/Playwright
resolution; helper/driver syntax and origin/credential scope; exact title,
budgets, argv-related assertions and reload count; short physical paths and
single-copy/private-graph controls; wrong role/tree/pin/path/argv/zero-test
refusals; wrong artifact-version refusal; and exact one-test Playwright list1.

The preflight created no build, browser, daemon, socket, install, service, or
actual-run state; its temporary root was cleaned by the retained runner trap.

## Independent custody handoff bodies

The preflight body above is the exact executed body. The retained runner's
run-mode body is syntax-checked but deliberately not executed here; central
custody supplies two clean, physically distinct roots matching the final
source tuple:

```sh
RUNNER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-existing-runner-current-bind-0852/artifacts/run-owned-selected-final95.sh
SERVICE_CAPTURED_APP_ROOT=/absolute/clean/service-captured-app-root
PROTECTED_APP_KEEPER=/absolute/clean/protected-app-keeper
APP_KEEPER_ROOT="$PROTECTED_APP_KEEPER" SELECTED_FINAL95_MODE=run \
  "$RUNNER" "$SERVICE_CAPTURED_APP_ROOT"
```

The run body retains the exact one-dispatch launch-only stub boundary,
wrong-source/hash/pin/path/list/version refusals, protected keeper checks,
credential/origin guards, and cleanup/exit propagation from 0724/0730. It was
not submitted to the central service. The prior 0730 central result remains a
HOLD at the Runtime handshake (`unauthorized: invalid bearer credential`), not
a selected behavior qualification; no retry or relabeling was performed.

## Checks not run

No browser, build, daemon, localhost/live socket, actual selected case, full
suite, dependency install, or central service run was performed. No App source
test execution was added because this task explicitly requires the final bound
preflight only.
