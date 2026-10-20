# Runtime text clear S2 current gate

Date: 2026-10-20 UTC

## Result

Ported the independently approved Runtime text presence and retained-legacy-custody unit from `e41f3d1e655a005904bbdc90f04b3ab825f4f225` onto current Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.

The approved scope is presence-aware event custody/readers, atomic clear/resurrection projection through the existing `shot.text_binding.rebound` event, exact retained legacy `text/plain` reuse validation, and the approved regression fixtures/tests. First-use text selection remains strict `text/plain; charset=utf-8`; no bytes or MIME are normalized.

No new schema, operation, endpoint, table, event kind, DTO, public artifact, caller-authority switch, client, metadata, view, connector, main, producer, F1, or F2 change was added. Native Agent full-schema qualification remains separate and is not claimed here.

## Source and tree identity

- Approved source commit: `e41f3d1e655a005904bbdc90f04b3ab825f4f225`
- Approved source tree: `de8f95b2ab0485b3a4d9625d60da3899307c0042`
- Approved comparison base: `8609333456b9537339ee1a5dfc7ffd9609242de8` (tree `2ae8508a1d3dac62e99c27056585eedc62bf5ff6`)
- Current worktree base: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Central snapshot of this uncommitted port: `211f9b2e0b05d25a0721d32d627433e25c38eefd`
- Source review: `scratchpad/orch/workers/rt-m2-text-clear-legacy-final-review/DetailedReport.md`
- Agent representation ACK: `scratchpad/orch/design/agent-text-binding-clear-ack.md`, SHA-256 `0c0e8e6903ff0eb255ba0f1872772439de5c0acfb20e5e9ca50b4eac20768a8a`

Ported files:

- `runtime_protocol/service.py`
- `runtime_protocol/timeline_commit_baseline.py`
- `runtime_protocol/timeline_commit_port.py`
- `runtime_protocol/timeline_commit_store.py`
- `tests/test_timeline_text_selection.py`
- `tests/legacy_text_binding_fixture.py`
- `tests/test_timeline_text_binding_clear.py`
- `tests/test_timeline_text_legacy_custody.py`

SHA-256 of the resulting files:

```text
b3ddfac477fb8dbcfd28307684940a5fce9d20d07d7c8f8c9bbcc5bf3432b6e2  runtime_protocol/service.py
481ed8a07080fe203293b25cf5651cb9ab28628e8432a86c42d1c861ea81395a  runtime_protocol/timeline_commit_baseline.py
0f4c98a92417f2d8bb8049d462bcd3405a3df9325de19647762cb0942e4dd6b1  runtime_protocol/timeline_commit_port.py
bbe8b20d3a21782b81195da17dbb1f3e44548ddbf37b3d86cfffa42e1245ccf6  runtime_protocol/timeline_commit_store.py
4396c9822cc121c9f25f9a3788e08d238e93564831458e8b766e9179ed1fd959  tests/test_timeline_text_selection.py
2f910bec11f6ab3e86f280c05482e0212b95ab577db2388df67692cd5c4499d4  tests/legacy_text_binding_fixture.py
0d5182efd4f0bc271d644f1ca2ec8cfc4b1a1c50ab5424299d080303efc52594  tests/test_timeline_text_binding_clear.py
382a9027a870ede5377bc0d452957728e737c0b48a2e392a1e5e7fe3d183e0fa  tests/test_timeline_text_legacy_custody.py
```

## Evidence

All commands were run with shared dependencies/caches read-only and without a full suite.

1. Local targeted cohort:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_text_legacy_custody.py tests/test_timeline_text_binding_clear.py tests/test_timeline_text_selection.py
```

Result: **69 passed in 45.01s**.

2. Required exact 233-neighbor gate, through the named central `restore-integration` lane with `--files`:

```sh
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_text_selection.py tests/test_timeline_text_binding_clear.py tests/test_timeline_text_legacy_custody.py tests/test_shot_text_bindings.py tests/test_timeline_history_boundaries.py tests/test_timeline_commit_restore_port.py tests/test_timeline_commit_baseline.py tests/test_shot_composition_runtime.py tests/test_runtime_control2.py::test_backup_restore_and_structured_export_verify_cas_and_sqlite tests/test_doctor_timeout_reporting.py tests/test_restore_history_fixture.py
```

Central request: `rt-m2-text-clear-s2-current-gate-restore-integration-1020115618-21033`.

Result: **233 passed, 1 deselected, 4 unchanged strict xfailed in 82.73s**.

3. Required commit integration gate, through the named central `commit-integration` lane with `--files`:

```sh
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/test_timeline_commit_integration.py tests/test_timeline_commit_integration.py
```

Central request: `rt-m2-text-clear-s2-current-gate-commit-integration-1020115852-11356`.

Result: **9 passed in 13.78s**.

4. Static checks:

```sh
git diff --check
python -m compileall -q runtime_protocol tests/legacy_text_binding_fixture.py tests/test_timeline_text_binding_clear.py tests/test_timeline_text_legacy_custody.py
```

Both exited 0. Compile bytecode was removed from the worktree afterward.

The first central attempt used the generic `targeted` lane, whose command lacks the required Agent checkout. It reported **226 passed, 1 deselected, 4 xfailed, 7 setup errors**; all seven errors were `Astrid checkout is unavailable: /home/user/work/wt/astrid`, not product failures. It was superseded by the passing named-lane request above.

The source review's two unchanged original legacy positive probes were recorded as **2 passed in 1.74s** against the exact approved source export. They were not rerun separately in this current worktree; the current local 69-test cohort and central gate include the approved legacy custody cases.

## Limits and next steps

- No full, browser, socket, or broad suite was run.
- The known baseline historical-pin latest-anchor asymmetry is unchanged and remains outside the claim.
- No native Agent full-S2-plus-text normal-generation pair qualification was run or claimed.
- Do not publish/promote artifacts, retire writers, cut over App, or claim native/overall completion from this Runtime unit alone.
