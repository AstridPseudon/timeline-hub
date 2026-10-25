# Validation

## Passed locally

```text
bash -n ops-d73-exact-nodes/dry-check.sh                  PASS
git diff --check                                          PASS
python -m json.tool /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D73-exact-node-return-2127/evidence/readiness.json PASS
python -m json.tool /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D73-exact-node-return-2127/evidence/source-manifest.json PASS
ops-d73-exact-nodes/dry-check.sh --bind-check \
  /tmp/d73-central-a/d73-fake-central-a/d66 \
  /tmp/d73-central-b/d73-fake-central-b/d66               PASS
```

The binding check used two synthetic paths only; it did not create a service
request or write test output. Static inspection also confirmed both suite rows
start with `-m pytest -q`, use `D66_OUTPUT_DIR`, derive the parent request ID,
retain the exact 4+1 selectors, and keep `run --` direct.

The reviewed launcher, Runtime receipt, central runner scripts, and central
suite configuration were read-only inputs. Their SHA-256 values are recorded
in `source-manifest.json` and `readiness.json`.

## Not run by design

`--source-check` and `--controls` were not run because the eligible Agent
receipt and rendered D73 manifest are absent. No body, central request, live
service, provider/socket, install, full suite, or browser run was performed.
Historical 2036/2111 control results are not re-reported as fresh.

Ruff/pytest for the Composition repository are not applicable to this
source-only shell/recipe change. The Agent focused control pytest is an owner
step after exact source admission, not evidence available in this worker.
