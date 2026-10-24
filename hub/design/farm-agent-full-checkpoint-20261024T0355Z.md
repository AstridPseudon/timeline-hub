Ask: Agent credits exact nodes / Owner: Agent / By: 2026-10-24T05:00Z

I could not get the checkpoint count. The one full run failed at collection, so zero tests executed, which counts as a FAIL. I wrote the reason to `BLOCKED`, did not create `DONE`, and edited no repo files.

## What was tested
- **Agent `tl/integration` head:** `8657e83653f48c935f52f209516456bcb5a36282`, tree `b5cbc40265d89b422c0478945256c662684b03b3`.
- **How I got the head:** I read it from `/home/user/work/agent`, which is the repo the test service runs. I did not re-fetch the hub, since I can't fetch. The hub clone has no `tl/integration` ref for Agent.
- **Exact-SHA checkout:** `request-checkout` created `/home/user/work/wt/agt-pin-8657e836` (detached, KEEP).

## What failed
1. **`request-child-venv venv-agent-child-fullckpt <sha>`** was refused. `/home/user/work/bench-store/owner.json` does not exist (`FileNotFoundError` in `bench_store.py:135`).
2. **`request-runtime agent-remotion-fullckpt <sha>`** was refused. The preflight failed with `missing_prerequisite=registration:template-or-exact-source-identity`.
3. **`request-test integration:agent full`** (id `agent-full-1024035157-25730`) failed with exit 4 in 10 seconds. The command was `/home/user/work/venv-agent/bin/python -m pytest -q -n 3`.
   - Collection stopped with `ModuleNotFoundError: No module named 'runtime_protocol'`, raised from `tests/conftest.py`, then `astrid/core/pack/source_setup.py`, then `astrid/core/foundation/atomic_io.py:16`.
   - The `agent full` line in `suites.conf` sets no `PYTHONPATH` or `ASTRID_RUNTIME_CHECKOUT`, so no Runtime checkout is on the path.

## Classification
| Item | Class |
|---|---|
| Child venv and runtime refusals | environment (dispatcher and bench-store provisioning) |
| `runtime_protocol` import error at conftest | harness (suite definition) |
| Product failures | none observed; no test ran |

There are no passed, failed or errored nodes to list. Because nothing ran, this says nothing about the 267 Agent failures, so I can't say how many are still open.

## What I did not do
- **No workaround:** I did not edit `suites.conf` or retry, because the brief says one run and no workarounds.
- **No design file:** `design/farm-agent-full-checkpoint-<UTC>.md` and the raw junit file were not written, because the harness refuses design/ writes from workers. The junit file doesn't exist anyway: collection aborted before any results were produced. This report is the deliverable.

## Next steps for the owner
- Fix the `agent full` line in `suites.conf` to add `ASTRID_RUNTIME_CHECKOUT` and a `PYTHONPATH` that includes a Runtime checkout. The `agent` lines for `commit-integration` and `client-cutover-integration` already use `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`.
- Repair or initialise `/home/user/work/bench-store` and the runtime registration so child venvs and runtimes can be provisioned.
- Re-dispatch the checkpoint once both are fixed.
- The test service caches by source tree, and tree `b5cbc402…` has no cached full result, so the rerun will execute.

I wrote `commit-msg` (`chore: no changes`) to the orchestrator path.
