# Worker report

## What I did

- Read the settled plan and assigned brief.
- Ran the required no-socket inventory with the exact
  `/home/user/work/venv-agent/bin/python`: all 54 declared closure
  distributions were present; Agent `6efc815` and normal Runtime/client
  `95bd3c5f` sources were clean at their expected commits/trees; the fixture
  still matched reviewed launcher source `8f70`.
- Submitted exactly one central request using the named
  `wc10-installed-launcher-integration` suite and the required test selector.
- Updated the absolute proof report, added the matched-runner result, and sent
  the bounded Agent handoff through both design and hub inbox.

## Exact test commands and results

Preflight command:

```text
PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python - <<'PY' ... inventory DECLARED_CLOSURE, source commits/trees/status, and reviewed launcher diff ... PY
PASS: 54/54 distributions present; source/hash checks clean.
```

Single central request:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-wc10-matched-runner-one-execution-0318 wc10-installed-launcher-integration --files tests/test_wc10_installed_launcher.py::test_wc10_installed_normal_launcher_provider_bootstrap
```

Result ID:
`rt-m2-wc10-matched-runner-one-execution-0318-wc10-installed-launcher-integration-1021031824-22571`

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_wc10_installed_launcher.py::test_wc10_installed_normal_launcher_provider_bootstrap
exit=1; 1 failed in 31.26s
```

The run built/installed the three expected product wheels, launched the
installed Runtime, passed healthy status and isolated child health, and
persisted the project mutation. It failed at the unchanged
`create_project(...)["project_id"]` assertion because Agent's
`WorkspaceClient._call_generated` returns mutation results under an outer
`data`/`receipt` envelope. Timeline/provider bootstrap, canonical read,
no-legacy, and later custody assertions were not reached.

No full suite, browser, renderer, external model, publication, pin, merge, or
retry was run. No source or test edits were made. The central failed result's
retained temporary environment is not mine to delete.

## Decision / blocker

I treated the response-shape mismatch as a blocker requiring the Agent/test
owner to choose the authoritative existing contract. I did not change the
test to force a pass or claim installed provider/bootstrap proof.

## Next step

Agent/test owner should reconcile the existing mutation envelope with the WC10
assertion, then authorize any future execution separately. This task's one-run
budget is exhausted.
