# D73 / D139 validation

## Controls

- `TMPDIR=/tmp/w-d73-review-controls PYTHONDONTWRITEBYTECODE=1 ./ops-d73-exact-nodes/dry-check.sh --controls` — **PASS**; seven tests passed. Both named rows reached the private bounded stub with exit 17 and one call; source-SHA poison returned nonzero with zero additional calls and no poison body artifacts.
- `TMPDIR=/tmp/w-d73-review-controls PYTHONDONTWRITEBYTECODE=1 ./ops-d73-exact-nodes/dry-check.sh --bind-check /tmp/w-d73-review-controls/selected-ID/d66 /tmp/w-d73-review-controls/fork-ID/d66` — **PASS**; separate IDs/XML paths.
- `env -u D73_MANIFEST TMPDIR=/tmp/w-d73-review-controls PYTHONDONTWRITEBYTECODE=1 ./ops-d73-exact-nodes/dry-check.sh --source-check` — **expected exit 1**; status `NOT_READY`, source_ready false, body/preflight `NOTRUN`, 26 missing manifest keys, missing current receipts, absent rows, fresh-result gaps, and interpreter/schema need all reported.

## Production-path adversarial control

- Actual current `tools/p4-d73-pinned-launch.sh` with a valid private fixture plus duplicate `format` key — **FAIL**; return 0 and eight artifacts were created. This demonstrates that the production launcher does not reject duplicate keys.
- Actual current launcher with private preflight forced to exit 9 — **FAIL**; return 9 but five artifacts were created before the refusal. This demonstrates that launcher artifact creation precedes preflight.
- Static row audit — **FAIL**; `ops-d73-exact-nodes/suites.conf` calls the unchanged launcher directly, while `test-run` line 15 only performs the named-row awk selection and line 17 appends selectors. No production call to `check.py` exists.

## Static checks

- `/home/user/work/venv-agent/bin/ruff check --no-cache --config /home/user/work/agent/pyproject.toml ops-d73-exact-nodes/check.py ops-d73-exact-nodes/test_recipe.py` — **PASS** (`All checks passed!`).
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/w-d73-review-controls/pycache python3 -m py_compile ops-d73-exact-nodes/check.py ops-d73-exact-nodes/test_recipe.py` — **PASS**.
- `bash -n ops-d73-exact-nodes/dry-check.sh ops-d73-exact-nodes/suites.conf /home/user/work/agent/tools/p4-d73-pinned-launch.sh` — **PASS**.
- `git diff --check` — **PASS**.

## Read-only checks

- Current normal Agent 41ad and Runtime f103 clean checkout identities, trees, parents, origins, and Runtime lock source commit were verified. The current Agent/Runtime receipt files are absent, so receiving cannot be ready.
- Selected4 and fork1 test files, launcher, focused launcher-control file, and `tests/helpers/runtime.py` are byte-identical to the 2eca source. `vendored_runtime_commit()` reads the f103 `runtime.lock.json`; selected4 `use_runtime()` receives the launcher-selected Runtime checkout.
- Runtime lock has producer `astrid-runtime`, 15 canonical entries, and all 15 file hashes match. Only lock source provenance differs from ab1e.
- Changed-file scope is four files under `ops-d73-exact-nodes`; `dry-check.sh` is unchanged from the source branch parent. No product/test/launcher/registry/pin files were modified.

No real imports, product tests, collection, interpreter preflight, provider body,
request, installation, Store, child/core, acquisition, credentials, Git writes,
or full suite were run.
