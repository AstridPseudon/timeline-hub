# Launch environment validation (Track A1)

Launch checks validate the environment passed to each child. Ambient values omitted by that projection neither fail validation nor split its context key. The ordinary resolver, idle observation, bootstrap reuse and renderer regeneration share this rule through `probe_context` and `_registry_context`.

## Boundary evidence

Paths and line numbers below refer to this change.

| Previously refused ambient names | Why they cannot reach the validation/render children |
| --- | --- |
| `PYTHONUSERBASE`, `PYTHONNOUSERSITE`, `PYTHONSAFEPATH`, `PYTHONPYCACHEPREFIX`, `PYTHONPLATLIBDIR`, `PYTHONCASEOK`, `PYTHONUTF8`, `PYTHONCOERCECLOCALE`, `PYTHONSTARTUP` | None is in the Node/schema key lists (`astrid/core/rendering/remotion_runtime.py:197`), registry key selection (`:425`), or safe base/propagated selection (`astrid/core/subprocess_env.py:57`, `:90`, `:168`, `:202`). |
| `PYTHONEXECUTABLE`, `__PYVENV_LAUNCHER__`, `PYTHONHOME`, `NODE_OPTIONS`, `NODE_PATH`, `NODE_ICU_DATA`, `OPENSSL_CONF` | The same three selections omit every name. The Python executable is an explicit argument and is content-bound; it is not selected from these ambient values. |
| Every `DYLD_*` and `LD_*` name | No prefix wildcard is admitted by any of those selections. |
| Every `GIT_*` name, including `GIT_CONFIG_GLOBAL`, `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` | No `GIT_*` entry is in those selections, including the old interactive exceptions. The registry child and its Git descendants inherit only the selected registry environment. |

The exact Node environment is passed at `remotion_runtime.py:876`; schema environments at `:885` and `:915`. The complete selected registry mapping goes to discovery at `:724` and generation at `:800`. The context and its canonical key are constructed from these projections at `:862`. `_validated_runtime` reconstructs the same context at `:1041`.

Render transport filters its backend at `astrid/core/rendering/transport.py:430`. The generator and render CLI use `build_child_subprocess_env` at `astrid/packs/rendering/rendering/renderers/remotion/run.py:482`, `:1327`, `:1332`. Explicit additions at `:1184` contain temporary paths, owner render settings, the selected schema path and composition source; none reintroduces any refused ambient name.

The run-astrid launcher still carries the caller environment (`astrid/installer/launcher.py:132`). Bootstrap reuse (`astrid/sdk/host_bootstrap.py:1544`), host idle context (`astrid/core/execution/generic_host.py:6202`) and worker readiness (`:7889`) all reach the same projection checks. A redundant in-process registry recomputation in launch-bound regeneration could start Git with the caller environment. It now uses the expected state after the validator has rechecked the complete recorded corpus and output bindings (`run.py:447`); cache and output drift checks remain.

## Inputs that remain checked

Safe base values retain type checks. Renderer registry selectors and import paths retain absolute-path checks; generator checks only selectors it receives. Errors name the variable and give a correction. Installer `PYTHONUTF8` was the same ambient/projection case: the test now accepts it and compares identical contexts; installed tools retain `PYTHONIOENCODING=utf-8`.

Manifest `command.env`, required environment and declared passthrough can deliver the old refused names to a worker before Python starts. `_validate_remotion_worker_environment` (`remotion_runtime.py:411`) therefore refuses those names in the built worker environment, both at launch projection (`generic_host.py:1915`) and actual child construction (`:7789`). Its error names every offending variable and says to remove it from the three declaration sources. Existing interactive Git exceptions stay supported. No ambient-only refusal remains for an alleged effect outside the child environment.

## Focused validation

Use a temporary HOME/cache, `ASTRID_RUNTIME_DOOR_PORT=17341`, agent/runtime PYTHONPATH, Python 3.11 and the lightweight pytest/jsonschema/PyYAML/filelock dependencies. The host tests additionally need Pillow, requests/httpx and the installed timeline-schema package. Runtime and Runtime client must be importable from the isolated test interpreter's site-packages for the subprocess adapter test, since its child deliberately filters ambient PYTHONPATH. No real Astrid installation or live Runtime is needed.

No platform skips were added. Existing lane exclusions (integration/native/live tests) stay in the normal pytest configuration. Test counts and CI conclusions are recorded in the delivery report.

Ruff 0.12.0: original branch 2,200 versus merge base 2,197. The four new findings were local.py import ordering and three broad catches; another finding had already disappeared elsewhere on the branch. Fixes reduce the count to 2,196; the count baseline is updated. Optional network discovery also handles truncated HTTP responses.

The result-manifest registry conformance test fails identically on merge base `8b6ed2116f` and the original branch: the registry has `music.duck` but the output-result exemption list does not. This is left unchanged.

Final focused local results: 388 passed, 0 failed, 0 skipped; 282 deselected by existing lanes or focused name selection.

| Selection | Passed | Deselected |
| --- | ---: | ---: |
| `tests/core/rendering/test_remotion_registry_git_env.py` | 18 | 0 |
| `tests/packs/rendering/test_render_export_task_adapter.py` | 138 | 1 |
| `tests/stage1/test_host_bootstrap_manifest_luna.py` | 14 | 0 |
| `tests/journeys/test_journey_plumbing.py` | 87 | 2 |
| `tests/test_installer_tools.py` | 14 | 0 |
| `tests/packs/test_vibecomfy_local.py` | 10 | 0 |
| `tests/test_generic_host.py` (launch/worker/idle/readiness selections) | 103 | 225 |
| `tests/packs/rendering/test_remotion_backend.py -k launch_bound` | 4 | 54 |

The separate result-manifest conformance case had 1 failure on each revision (original branch and merge base), both the same missing `music.duck` exemption. The minimal test dependency command emits an unknown pytest `timeout` option warning because pytest-timeout is not among those dependencies. A separate VibeComfy check with pytest-timeout installed passed all 10 tests without warnings. Tests used a fresh temporary bytecode cache after rapid same-size edits exposed stale cached test bytecode.
