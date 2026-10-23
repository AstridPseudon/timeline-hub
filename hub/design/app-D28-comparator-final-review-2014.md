# D28 comparator final audit — PASS

## Verdict

**PASS.** The corrected `app-D28-App18607-safe-comparator-2001.md` now
satisfies the finite 1956 matrix and resolves the concrete completeness gaps
identified by the independent 2005 FAIL. This review is report-only and uses
retained artifacts; it does not change the author report or make a new
environment-equivalence or causal claim.

## Concrete verification

The retained run remains the actual direct-service 18607 run: exactly 1 PASS /
1 FAIL, 744 seconds, raw custody 26,440 bytes / 62 lines. Case 1 starts at
source line 1055 and passed in 27.4 seconds (execution log line 9). Case 2
starts at line 1223, failed at the expected-post assertion on line 1255, and
the failing `afterEach` starts at line 1043. The Agent move, HTTP 409 refusal,
and App rollback/message assertions were unreached. These boundaries are
preserved without assigning cause.

The corrected report now returns the retained public custody facts that 2005
identified:

- Node executable:
  `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node`
- Node/npm: `v20.19.4` / `10.8.2`
- Remotion project:
  `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830`
- CLI-only installed origins for `astrid`, `astrid_runtime`,
  `runtime_protocol`, and `astrid_runtime_client` are returned under the
  retained public `.../venv-agent-child-app-p1-787-2a9-1829.partial.../lib/python3.13/site-packages/`
  paths. Actual daemon Python and provider/module origins remain
  `NOTCAPTURED`.
- Body-command presence: `NODE_PATH=false` (explicit `env -u`),
  `NODE_OPTIONS=true`, `PYTHONPATH=true`; requested `ASTRID_*` and `VITE_*`
  presence remains `NOTCAPTURED`.
- Playwright path/version and exact build command/dist path remain
  `NOTCAPTURED`; the retained invocation is present and the mode is correctly
  bounded as direct hosted dist with build skipped.

The final application-row projection remains `NOTCAPTURED`, correctly: the
retained diagnostic line/source-range hashes are not a final application-state
projection. Selected source identities are explicitly not synthetic `%H/%P/%T`
snapshot evidence, with `%P` and the synthetic tuple unavailable. Retained
route/method/status observations are not promoted to health, realm,
authorization, connectedness, mounted equality, or causal ownership. The
full-v2 caller/reply boundary and STOP denial remain unchanged.

## Checks and disposition

`git status --short`, `git diff --check`, and `git diff --stat` were clean.
Retained safe packet, raw-log metadata, Remotion receipt, and provision report
were checked read-only and required paths were present; raw bytes were not
printed or rewritten. Tests/typecheck/lint are N/A for this read-only review.

No remaining FAIL or report split is required. ProofSol1950 remains the owner
of environment-equivalence and causal disposition. No live probe, alternate
setting, browser/body/service access, or product change is authorized by this
review.
