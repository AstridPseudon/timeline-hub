# U2 upstream review: FAIL

Reviewed commit `8a2677cd793a8d5abbcd3b0afd992d231e8aef09` against PLAN §3 U2 and the contract approval gate.

## Findings

1. **FAIL — the harness commit is ancestry-only.** Its parents are `a086cc6db7928dc4a3516d304dd9a472b050f1cf` and `9ec1eae349affda35da8b1dc6b5d37e12627f37e`, but its tree is `93de0323c7cce6fa4a6473aa68ef2f967d0e6b8f`, exactly the same tree as `a086cc6db`. `git diff a086cc6db 8a2677cd7` is empty. Parentage does not establish that upstream landed.

2. **FAIL — upstream behavior is not present in the result.** Against the upstream parent, the expected changes include modifications to `astrid/sdk/timeline/publish.py` and `edits.py`, removal of `commands.py`, `commit.py`, `native_checkout.py`, `sync.py`, and changes to `astrid_runtime_client/generated.py`, `runtime.lock.json`, and `artifacts.json`. The result retains the first-parent versions of all of these paths. Therefore preservation of upstream `publish.py`/`edits.py` behavior inside native paths cannot be demonstrated; the required merge resolution never happened.

3. **FAIL — generated artifacts/client are not from the upstream merge tools.** The result has the first-parent tree, so the upstream-side generated client, artifact manifest, and lock changes were not landed. The passing checks below only validate the unchanged baseline and are not merge acceptance evidence.

4. **FAIL — contract approval gate not met.** A resolved upstream merge tree is required before U2 can be accepted against the approved contract. The requested R4 control-doc directory is not present in the accessible Agent checkout, so its absence was not treated as approval evidence. The escalation record confirms the merge preparation was blocked by read-only `ORIG_HEAD.lock`; the harness nevertheless recorded the unresolved two-parent commit. I did not merge or repair it.

## Checks

- `PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_publish_connection.py tests/sdk/test_timeline_native_frontends.py tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py tests/packs/timeline/test_edit_verbs.py tests/packs/timeline/test_cli_commit_trim.py` — **FAIL during collection**: `ModuleNotFoundError: No module named 'runtime_protocol'` from `tests/conftest.py`.
- `make ruff mypy PY=/home/user/work/venv-agent/bin/python` — **FAIL at Ruff**: `current=2157 baseline=2159`; the Make target stopped before mypy because Ruff improved by 2 and requested baseline locking.
- `make mypy PY=/home/user/work/venv-agent/bin/python` — **FAIL**: 13 errors, including missing `yaml` stubs and a NumPy stub syntax error under the configured interpreter.
- `PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — **PASS**: `artifacts.json is current`.
- `PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json` — **PASS**: `ok runtime.lock.json`.

No full, browser, or live-socket suites were run.

## Recommended next steps

Start again from `tl/integration` / `a086cc6db` after an approved Codex merge-preparation path can update `ORIG_HEAD` and resolve the actual upstream tree. Regenerate the Runtime client and artifacts with their repository tools, then rerun this review and the mandated checks. Do not merge or repair `8a2677cd7`.
