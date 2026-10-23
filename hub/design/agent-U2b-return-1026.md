# U2b return after independent 1019 review

## Result

Corrected the four source-backed findings from the independent review of
`55c1e7aa7` without changing the Timeline contract, Runtime/Composition pins,
generated clients, or product writer ownership.

## Changes

- Removed exactly the three accidentally committed bytecode artifacts:
  - `tests/core/rendering/fixtures/__pycache__/owned_tree_backend.cpython-313.pyc`
  - `tests/core/rendering/fixtures/__pycache__/transport_backend.cpython-313.pyc`
  - `tests/sdk/fixtures/selected-param-legacy/__pycache__/generate.cpython-313.pyc`
- Removed the reintroduced
  `tests/packs/rendering/test_timeline_inspector_viewer.py`. The current
  approved dead-inspector cut (`c1a1d4fdb` / the earlier transitive deletion)
  removed both that private viewer and its test. The upstream lane/skip-policy
  merge changed/reintroduced the test while the product remained deleted; the
  actual source conflict therefore means preserve the approved deletion. No
  viewer product was restored and no test was converted into a skip.
- Removed the extra EOF blank lines from:
  - `tests/packs/runpod/conftest.py`
  - `tests/test_runtime_correctness_inventory.py`
- Replaced the stale `GenericPackHost._publish_assembled_timeline` test. That
  route was intentionally removed by the native assembly cut; the test now
  exercises the existing requester `publish_authoring_proposal` commit caller.
  It retains the meaningful behavior assertions: one canonical commit,
  producer attempt/fence binding, the admitted project/timeline and base pair,
  one ordinary `rendering.render` task, and no local `save`/`invoke` route.
  The old lease-token assertion was not ported because the surviving requester
  commit caller does not receive or consume a host lease token. No legacy
  writer or fake executor was restored, and no xfail was added.

## Tests and checks

Passed:

- `/home/user/work/venv-agent-child-f1012-installed/venv/bin/python -m pytest -q tests/packs/video_editing/test_runtime_publication_chain.py -k 'requester_commit_publishes or legacy_assembler_admission'` — **2 passed**.
- `/home/user/work/venv-agent-child-f1012-installed/venv/bin/python -m pytest -q tests/test_lanes.py tests/test_lane_registry.py tests/test_skip_policy.py tests/test_skip_guard.py` — **55 passed**.
- `test ! -e tests/packs/rendering/test_timeline_inspector_viewer.py` — passed.
- `/home/user/work/venv-agent-child-f1012-installed/venv/bin/python -m pytest --collect-only -q tests/packs/rendering` — **1510 collected, 41 deselected by lane**; the deleted inspector test was absent and collection succeeded.
- `make PY=/home/user/work/venv-agent/bin/python ruff` — **Ruff 2149/2149**.
- `make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy` — **Mypy 1912/1912**.
- `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json` — `ok runtime.lock.json`.
- `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — `artifacts.json is current`.
- `/home/user/work/venv-agent/bin/python scripts/reshape/check_repo_hygiene.py` — passed (exit 0).
- `git diff --check HEAD` — passed.
- `git merge-base --is-ancestor 74f3f7ed HEAD` — passed; live tip is an ancestor.
- Protected client/lock/composition-pin path comparison — unchanged.

One broader targeted command was intentionally not treated as green:

- `/home/user/work/venv-agent-child-f1012-installed/venv/bin/python -m pytest -q tests/test_runtime_correctness_inventory.py tests/packs/runpod/test_worker_process.py -m 'not integration'` — **44 passed, 4 failed**. The four failures are the existing inventory test's requirement for the absent `docs/runtime-correctness-m3-inventory.md`; this task only fixes its EOF finding and does not restore the retired document or alter unrelated coverage.

The first attempted `make ... mypy` with Python 3.13 environments lacked YAML
stubs and used an incompatible NumPy stub; the repository's Python 3.11
typecheck environment then passed the required 1912 baseline. The first Ruff
attempt used Ruff 0.16 and was not the pinned baseline environment; the pinned
Ruff 0.12 command passed 2149/2149.

Not run per task restrictions: full suite, browser/native 14/58 suites,
HTTP/live-socket suites, and duplicate full journeys. No shared install was
modified, no daemon was started, no generated artifact or pin was regenerated,
and no D17 content was imported.

## Final scope

The final worktree delta is limited to the three named `.pyc` deletions, the
approved inspector-test deletion, the two EOF fixes, and the requester-path
test correction. No protected client, schema, lock, or Composition pin paths
are changed.
