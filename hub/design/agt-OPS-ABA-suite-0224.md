Implemented candidate-only harness registration.

**Candidate:** [tests/suites.conf.candidate](/home/user/work/wt/agt-OPS-ABA-suite-0224/tests/suites.conf.candidate)

```text
agent authoring-current8ea-nodes env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-8ea0766f" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/wt/rt-pin-8ea0766f ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110 ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 -m integration
```

Checks:

- Exact environment preflight: passed.
- Exact single-node collection: `1 test collected in 2.01s`.
- Candidate row: 811 bytes, SHA-256 `962906266ee294a590958a4bcd5d4d7c1fda8dbcf9fc205f4e16ccbf3089d102`.
- Live registry baseline preserved: 140 rows, SHA-256 `5175381ee16327ec214a0f7c49b4081d920a2d7801b87b014349358d5245b8a3`.
- Original function body SHA-256: `a00b763f1aeaf57cb3b04199a73b34ca17440396ff44f54aeee3041442122936`.
- `bash -n -s < tests/suites.conf.candidate`: passed.
- `git diff --check`: passed.

The integration body was not run, and the live ORCH registry was not modified. Commit message and `DONE` marker were written.