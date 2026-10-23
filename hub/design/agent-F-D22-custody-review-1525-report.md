# F-D22 custody/process/projection handoff

## Independent review F-D22-custody-review-1525

### Verdict

**PASS for the two test-harness changes only.** The reviewed commit is
`3ef951f3abd56a918b54b03226ec80e8b80155ab`, compared with
`58316fd6e0ce8a1fb3b2b3826ec71906d29080de`. Its exact product diff is limited
to these two test files; the newly tracked `report.md` and
`design/agent-F-D22-custody-1510.md` are evidence artifacts and are removed
from the product commit after this report is copied to the orchestrator.

The custody addition derives Runtime's source root from the already imported
`custody.platform.__file__`; it does not fabricate a root or add an arbitrary
import path. Under the review environment, `runtime_protocol.platform` came
from `/home/user/work/runtime` at Runtime commit
`9ce4242bc01f100bab9efc51032a73985cefb2b2`, while the Agent custody module
came from this worktree. The wrapper's existing `-I -S` stdlib-only control
launch and target restoration assertions remain unchanged.

The two projection additions copy only the supported ambient
`ASTRID_TIMELINE_SCHEMA_PYTHONPATH` value into each explicit fixture mapping.
The clean control environment omits that variable and the fixture retains its
absence. No environment allowlist, default projection, guard, timeout, or
product source bytes changed. No import injection defeating isolation was
found.

### Independent commands and results

Imported-origin/CLI probe:

```text
env -i HOME=/tmp/agt-F-D22-review LANG=C.UTF-8 LC_ALL=C.UTF-8 \
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  PATH=/home/user/work/venv-agent/bin:/usr/bin:/bin \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages \
  /home/user/work/venv-agent/bin/python -P -c 'import sys, astrid.core.execution.custody_broker as c, astrid.core.rendering.remotion_runtime as r, runtime_protocol.platform as p; print("cli",sys.executable); print("custody",c.__file__); print("platform",p.__file__); print("runtime",r.__file__); print("path",sys.path); print("schema",__import__("os").environ.get("ASTRID_TIMELINE_SCHEMA_PYTHONPATH"))'
```

Observed CLI was `/home/user/work/venv-agent/bin/python`; custody/runtime
modules were from this worktree; `runtime_protocol.platform` was from
`/home/user/work/runtime/runtime_protocol/platform.py`; and the schema path
was `/home/user/work/venv-agent/lib/python3.13/site-packages`.

Engine custody counterpart, central targeted service (the author command
representative was not repeated):

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-F-D22-custody-review-1525 targeted --files "tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[engine]"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test agt-F-D22-custody-review-1525-targeted-1023152629-4090
```

Result: **PASS**, `1 passed in 1.59s`, service exit 0. The service recorded
`/home/user/work/venv-agent/bin/python -m pytest -q`,
`PYTHONPATH="$PWD:/home/user/work/runtime:/home/user/work/agent-runtime-projection-0856/site-packages"`,
`ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`, and
`ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages`.
The service snapshot tree was `bdbc0f1d5cbb7ee5000af7ad8820df2a188857b7`.

Original projection nodes with the supported caller environment:

```text
env -i HOME=/tmp/agt-F-D22-custody-review-1525-original LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" PATH=/home/user/work/venv-agent/bin:/usr/bin:/bin ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages /home/user/work/venv-agent/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider tests/core/rendering/test_installed_registry_security.py::test_installed_native_readiness_context_must_match_projected_context tests/core/rendering/test_installed_registry_security.py::test_installed_actual_worker_environment_matches_launch_projection[command]
```

Result: **PASS**, `2 passed in 9.37s`, exit 0.

Original projection nodes with a clean caller environment:

```text
env -i HOME=/tmp/agt-F-D22-custody-review-1525-clean LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" PATH=/home/user/work/venv-agent/bin:/usr/bin:/bin /home/user/work/venv-agent/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider tests/core/rendering/test_installed_registry_security.py::test_installed_native_readiness_context_must_match_projected_context tests/core/rendering/test_installed_registry_security.py::test_installed_actual_worker_environment_matches_launch_projection[command]
```

Result: **PASS**, `2 passed in 10.03s`, exit 0.

Static and scope checks:

```text
Ruff current vs 583 baseline: custody 419 vs 419 findings after line normalization; projection 1 vs 1 output line (All checks passed); zero new findings.
/home/user/work/venv-agent/bin/python -m compileall -q tests/core/execution/test_custody_broker.py tests/core/rendering/test_installed_registry_security.py: PASS
MYPY_CACHE_DIR=/tmp/w-8974e5116d/mypy-cache PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline: PASS; current=1912 baseline=1912
/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json: PASS (ok runtime.lock.json)
/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check: PASS (artifacts.json is current)
git diff --check: PASS
git diff --quiet 58316fd6e 3ef951f3a -- astrid/core/execution/custody_broker.py astrid/core/execution/generic_host.py astrid/core/execution/process_group.py astrid/core/rendering/remotion_runtime.py: PASS
```

### Hashes and limits

Current reviewed test hashes are:

```text
b743e1edc49574dacd6a750d07fa6f9201519693309512b3b8b6184307a74610  tests/core/execution/test_custody_broker.py
fbe2476030da04776fe5c53a0bf0c999f0b438643b05b9af6ba32f2430de88d1  tests/core/rendering/test_installed_registry_security.py
```

Guard-product hashes are unchanged and match the reviewed branch's retained
source evidence: custody broker `83b7a8124e3f42f6ceffa966e22be8c5695a5434066be08c554b60fd69e57e94`, generic host `fc020cc2f6256642203fc4d36a9bb661265fa9a9589d386a46963528d11791d3`, process group `bce716c4c544f3247f189100c6fc74ab1decb2e7f9191196e92386959d5861b3`, and remotion runtime `84a495de2139c74b22c001094a3bb4d9252803f11715d7803054ecc2f9cc617e`.

The review did not run a full suite, broad D22 cohort, browser/live journey,
daemon, native14, or the five CPU/process nodes. Those seven managed/CPU nodes
remain **UNCONFIRMED** with no credit. The branch's overall D22 result remains
**FAIL**; this PASS approves only the two stale/inconsistent harness-input
corrections. No source fix was made.

## Decision

The D22 full result remains **FAIL**. This worker made and qualified two
test-harness corrections for two proven input roots. The seven CPU/process
nodes remain **UNCONFIRMED** and are handed to child-environment owner
`childenv1454`; no product custody or lifecycle source change is justified by
the retained evidence.

The corrected full inventory is 204 failures/errors: 17 child-probe, 87
child-import-or-recipe, 11 custody/process assertion, 2 fixture-declared-gap,
23 g5-inverse, 37 profile-fixture, 9 child-import, 1 d13-preflight, 7
r1-private, 2 g5-publisher, 2 g5-schema, 1 r3-docs, 3 d09-probe, and 2
r5-retired-route.

## Exact 11-node disposition

| root | nodes | evidence and disposition |
| --- | ---: | --- |
| custody wrapper fixture | 2 | The retained child stderr shows `sitecustomize` failing with `ModuleNotFoundError: runtime_protocol`; the target then runs without the network hook and records `denied=False`. The fixture now restores the exact imported Runtime source root in `PYTHONPATH`. The command representative passed; engine is the same corrected fixture path and was not rerun. |
| managed review / CPU process fixtures | 7 | The two managed-review nodes retain `observed=[]`; their trace includes the command child `runtime_protocol` startup failure. The five CPU nodes retain only absent process/shutdown markers, with no child stderr or argv proving a single cause. They remain unconfirmed; no source or assertion change was made. |
| installed registry projection fixture | 2 | Actual child context included the allowed propagated `ASTRID_TIMELINE_SCHEMA_PYTHONPATH`; the test projection omitted it because its explicit fixture mapping was incomplete. The fixture now carries that value when present. Both representatives pass with the original schema-path environment and with the clean environment control. |

Original safety assertions remain byte-for-byte unchanged. No timeout,
security rule, custody ownership rule, default projection, environment
allowlist, or product source was changed.

## Changes

- `tests/core/execution/test_custody_broker.py`: the existing wrapper fixture
  now includes `Path(custody.platform.__file__).parent.parent`, the exact
  Runtime source root already imported by the test process.
- `tests/core/rendering/test_installed_registry_security.py`: the two existing
  projection fixtures include the ambient schema path when the supported
  caller provides it; under a clean caller environment it remains absent.

These are stale/inconsistent harness inputs, not a relaxation of the guarded
behaviour.

## Test evidence

Central service request (one node, localhost/subprocess test):

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-F-D22-custody-1510 targeted --files 'tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[command]'
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test agt-F-D22-custody-1510-targeted-1023151223-24445
```

Result: **PASS**, `1 passed in 1.74s`, service exit 0. The retained service
argv used `/home/user/work/runtime` (the service's supported targeted Runtime,
not the full-run locked Runtime3b pair), so this is bounded fixture proof, not
a D22 full requalification. Its exact argv/environment remains in the result
summary.

Installed projection representatives, run directly because they do not launch
children:

```text
env -i HOME=/tmp/agt-F-D22-custody-1510-original LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" PATH=/home/user/work/venv-agent/bin:/usr/bin:/bin ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages /home/user/work/venv-agent/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider tests/core/rendering/test_installed_registry_security.py::test_installed_native_readiness_context_must_match_projected_context tests/core/rendering/test_installed_registry_security.py::test_installed_actual_worker_environment_matches_launch_projection[command]
```

Result: **PASS**, `2 passed in 10.19s`, exit 0.

```text
env -i HOME=/tmp/agt-F-D22-custody-1510-clean LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" PATH=/home/user/work/venv-agent/bin:/usr/bin:/bin /home/user/work/venv-agent/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider tests/core/rendering/test_installed_registry_security.py::test_installed_native_readiness_context_must_match_projected_context tests/core/rendering/test_installed_registry_security.py::test_installed_actual_worker_environment_matches_launch_projection[command]
```

Result: **PASS**, `2 passed in 11.72s`, exit 0.

Static checks: `git diff --check` **PASS**; `compileall` **PASS**. Scoped
Ruff reports **no new findings**: the installed projection file is clean, and
the custody file has the same baseline findings after line-number shifts.
Private mypy (`--follow-imports=skip --ignore-missing-imports`) reports the
same two pre-existing conditional-function-signature diagnostics at lines
1723 and 3534; neither changed line is implicated. No full suite or full
retry was requested.

## Locked evidence and hashes

- Full service: `agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679`.
- Full result: `185 failed, 16,733 passed, 4 skipped, 19 errors`, exit 1.
- Agent actual: commit `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`, tree
  `c4d72b065d6e68c92e4335120cc016cadf53b06a`.
- Comparison base: `58316fd6e0ce8a1fb3b2b3826ec71906d29080de`, tree
  `00c04a48841d95f5bf95dc604758767d2b065227`.
- Upstream comparison: `origin/main` / `74f3f7edba35230d0a01824eae7b663143e6aa5b`.
- Full row SHA-256: `9035bd9672c7186c440e4e3aaee15ae3dfbeaeb0192864f0a68b9f68cc212879`.
- Raw terminal log SHA-256:
  `e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`.
- Summary SHA-256:
  `5af68ba4480afbaba431db7007ea3dde7609fa73b0cdd4a0c71cc405e2fbb247`.
- Trace slice hashes: custody `a072ae3e16ad78d528da700de5bd9aceb281d36f0eeceebae72e303b06a0068b`; managed review `7f3d7936db47d4e3b9a210f9b07e684f7c1c647cc4fc9cc7c9eb62099dad0144`; CPU process `c99e15d6f4a7d8d883bfbd7e3f3bb399c61910fbd1dd6cecb1cb35321a18c312`; native projection `4d847eb7e2e8bc9fdcdf487b1daad26767380d2765325565d7a502d879032731`; command projection `d1ae19e17e7939ff98d8a70c879955d480cdf94cb62421f5b5eaae9fcd129528`.
- Current product source hashes are unchanged from 8c/583: `custody_broker.py` `83b7a8124e3f42f6ceffa966e22be8c5695a5434066be08c554b60fd69e57e94`; `generic_host.py` `fc020cc2f6256642203fc4d36a9bb661265fa9a9589d386a46963528d11791d3`; `process_group.py` `bce716c4c544f3247f189100c6fc74ab1decb2e7f9191196e92386959d5861b`; `remotion_runtime.py` `84a495de2139c74b22c001094a3bb4d9252803f11715d7803054ecc2f9cc617e`.
- Edited test hashes: `test_custody_broker.py` `b743e1edc49574dacd6a750d07fa6f9201519693309512b3b8b6184307a74610`; `test_installed_registry_security.py` `fbe2476030da04776fe5c53a0bf0c999f0b438643b05b9af6ba32f2430de88d1`.

## Handoff

`childenv1454` owns the remaining process-causality qualification. Use the
exact Runtime3b pair and preserve real PID, child stderr, argv/environment,
process cleanup, and shutdown-marker evidence. The five CPU nodes are:

```text
tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[False-False]
tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[False-True]
tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[True-False]
tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[True-True]
tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_cannot_close_unproved_real_attempt[observation]
```

Do not relabel them as preexisting, runtime-import, or product lifecycle
failures without that retained evidence. No additional full, environment
build, daemon, or broad cohort run is authorized by this handoff.
