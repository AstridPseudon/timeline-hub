# Commands and results

All commands ran in `/home/user/work/wt/app-D127-lifecycle-source-sol-1705`, with shared dependencies read-only. Scratch is `/tmp/w-dc5a187df6`. No full suite or localhost/browser/native/tour/recovery/service body was run.

| Exact command | Result |
| --- | --- |
| `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python TSX_DISABLE_CACHE=1 /opt/node20/bin/node --import tsx --test --test-name-pattern='D127|D105 launch ownership' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` | PASS, 3 passed, 2 selector exclusions; 53 actual helper-generated cases, 16 flag combinations, 16 retention pairs plus negative discriminators. |
| `/opt/node20/bin/node node_modules/eslint/bin/eslint.js tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts --report-unused-disable-directives --max-warnings 0` | PASS, exit 0 on final source. |
| `flock -w 60 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json --pretty false` | PASS, exit 0 on final source, serialized. |
| `/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit -p tsconfig.node.json --pretty false` | PASS, exit 0. |
| `git diff --check` | PASS, exit 0. |
| `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 NODE_COMPILE_CACHE=/tmp/w-dc5a187df6/node-cache /opt/node20/bin/node --import tsx /tmp/w-dc5a187df6/probe-differential.mjs` | PASS, exit 0: unchanged previous validator accepts 8/rejects 4 original projections; corrected validator accepts all 12 and all 53 new matrix cases. Actual functions transpiled with only test registration suppressed in this inspection wrapper, separately from the real node:test run above. |
| `/opt/node20/bin/node --version` | v20.20.0. |
| `realpath node_modules` | `/home/user/work/app/node_modules`; no installs or shared cache writes. |
| `df -B1 .` | Initial final-source admission: 4,999,151,616 bytes, shortfall 848,384. Later 5,039,894,528 bytes allowed D78. Latest: 5,028,909,056 bytes, current shortfall 0. |
| `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/w-dc5a187df6/write-evidence.py` | Writes and checks the required bounded evidence outputs and exact preservation mapping. |

The first new matrix invocation omitted `ASTRID_RUNTIME_CHECKOUT`, so the harness default sibling checkout did not exist. It failed before loading helper source; corrected the invocation to the qualified checkout. The next invocation exposed a test-author arithmetic mistake (40 generated boundary combinations + 12 callbacks = 52, not 92). Corrected that count, then added the missing original completed-without-handler callback, yielding 53 final cases. No behavior assertions were weakened in response to those setup failures.

D78 initially gated by disk, then admitted after availability rose to 5,039,894,528 bytes. Exact command:

`ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-070dfc5e ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python PYTHONDONTWRITEBYTECODE=1 TSX_DISABLE_CACHE=1 NODE_COMPILE_CACHE=/tmp/w-dc5a187df6/node-cache /opt/node20/bin/node --import tsx --test --test-name-pattern='D78 bootstrap' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts`

PASS: 1 passed, 4 selector exclusions, exit 0. This existing watchdog control has no sockets and was run directly; qualified Runtime's existing helper is unchanged 6c9. It preserves default 20 seconds and existing explicit 2-second option.

Exact reviewed-4ee normal-hook bootstrap: **NOTRUN**, infrastructure-blocked. `tests/suites.conf` contains no command referencing `p2-runtime-phase-bootstrap.test.ts`, nor a named generic App node selector suite. `targeted` is Vitest, and `e2e-harness` runs different files. The existing real bootstrap requires localhost and the user requires central service execution. Registering/changing that service file is outside this worker's write scope; no substitution, suite injection, new collector, direct localhost run, or broader suite was attempted. Disk is no longer the blocker (latest shortfall 0). No test timeout/budget changed and no external helper copy was created.

A repeated combined Node runner stalled after TAP version with no further growth. It was interrupted (exit 130) before retrying. A cache-disabled retry and a direct node:test invocation also stalled and were interrupted. Temporary diagnostics localized the stall to the pre-existing unlabeled aggregate arithmetic assertion when mutating queue duration of a completed case. Direct transpiled callbacks passed. The final mutation preserves aggregate queue+handler arithmetic while contradicting the exact observed queue boundaries, so it reaches the explicit boundary discriminator; the original arithmetic assertion remains byte-identical. All temporary diagnostics were removed. The final real Node runner passes 3/3 selected tests in 1.08 seconds. This is a narrowed mutation for the intended boundary predicate, not an inferred runner/cache fix. Final lint, serialized App tsc, node tsc, differential probe and diff check pass after that adjustment.

Runtime 23-pass evidence and original 160-predicate custody are reused unchanged from `app-D127-leaf-retention-author-1606-targeted-1025160952-28551` and `design/app-D127-leaf-combined-review-1630-assertion-custody.json`. These are reused evidence, not a new Runtime qualification. Prior source-conflicting candidate remains FAIL. Final independent review is required.
