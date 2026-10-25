# D73 / D139 / D140 validation

Available bytes before private controls: `5,212,770,304` (admission
requirement >= 5,000,000,000; source floor 4,600,000,000; stop 4,000,000,000).

Passed:

- `/home/user/work/venv-agent/bin/python -m unittest discover -s ops-d73-exact-nodes -p test_recipe.py` — **7 tests passed**. Both named rows reached run-mode stub exit 17 once; five refusal cases per row had zero new calls and no output directory.
- `TMPDIR=<private /tmp> PYTHONDONTWRITEBYTECODE=1 ./ops-d73-exact-nodes/dry-check.sh --controls` — **7 tests passed**.
- `env P4_D73_MANIFEST=/tmp/poison-manifest P4_D73_REQUEST_ID=poison-id P4_D73_EVIDENCE=/tmp/poison-evidence P4_D73_AGENT_PATH=/tmp/poison-agent /home/user/work/venv-agent/bin/python -m unittest discover -s ops-d73-exact-nodes -p test_recipe.py` — **7 tests passed**; row `env -i` prevented hostile external D73 variables from bypassing admission.
- `/home/user/work/venv-agent/bin/ruff check ops-d73-exact-nodes` — **All checks passed!**
- Private-TMPDIR Python compilation of `check.py`, `pre-dispatch.py`, and `test_recipe.py` — **passed**.
- `bash -n ops-d73-exact-nodes/dry-check.sh ops-d73-exact-nodes/suites.conf /home/user/work/agent/tools/p4-d73-pinned-launch.sh` — **passed**.
- `git diff --check` — **passed**.
- Read-only protected hash comparison against Agent 2eca — **all five exact**.
- Read-only Runtime lock census — source f103, producer `astrid-runtime`, 15 files, **all canonical hashes match**.
- Exact row spelling census — both canonical names match one row; tested alternate spellings match zero rows.
- `env -u D73_MANIFEST TMPDIR=<private /tmp> PYTHONDONTWRITEBYTECODE=1 ./ops-d73-exact-nodes/dry-check.sh --source-check` — **expected exit 1**, status `NOT_READY`; printed all required missing manifest keys, missing current receipts, absent central rows, fresh-result gaps, and interpreter/schema readiness gap.

No real product imports, collection, interpreter preflight, product body,
service, request-test request, central request, installation, registry/kit
change, Store/child/core operation, acquisition, credentials, Git write, or
full suite ran. No production guard relaxation was made; authentic later
launcher preflight behavior remains unchanged after valid admission.
