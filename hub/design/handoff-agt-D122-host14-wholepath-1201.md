# D122 REG14 whole-path read-only investigation

## Verdict

The retained `ALL14:14FAIL:34.87s` run is a genuine registry-discovery child
bootstrap failure, not a root failure at the terminal `RemotionValidationError`
wrapper. All 14 original selectors have the same first cause:

```text
ModuleNotFoundError: No module named 'runtime_protocol'
```

The retained child stderr shows the import failing at
`astrid/core/rendering/remotion_runtime.py:26` while executing the registry
discovery child. The wrapper then reports `original_wait_exit_code=1` at
`astrid/core/rendering/remotion_runtime.py:700`, phase `registry_discovery`.
The retained receipt still has `retained_set_final_census_complete=true` and
`custody_admitted=true`; those are downstream custody facts, not evidence that
the child completed registry discovery.

## Exact retained provenance

- Composition run tree: `5ab5191a296980a0a6bcd1178ab6902d6478a148`.
- Agent candidate: `bae5ab76f0acbf08b2d92d9f770fcf3dbe95f2fd`, tree
  `d5c0d544f25062b6c15de32cf71be573a22964ce`.
- Runtime: `369ffa7c00bd3d45c610fac7651ff79e7a283a1a`, tree
  `9bf331d68df8c966e8927a3f083ba03687803c99`.
- Test source SHA-256: `08dfa8dcafeb80c347923630864a29d58dea97e257428e204fc316567795161b`.
- Runtime profile: Node `v20.19.4`; composition `0.0.14`; lock
  `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`;
  archive `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`;
  registry `d609b44b37d724358a33405e9d8539008fd1ac30bc2f0d9746575c3fbadaac96`.
- Retained run request/snapshot/extension/summary/log SHA-256:
  `a3c792408b4a31dbacce8b68473b8a1f3f3979d59f92267e4311fc8f62a570fe`,
  `f00c6d0bf79c7c8de41fa56342aa07adf91f243b1d7d5bc074953127181ed114`,
  `eb3e6214345957b69db16e9207c8e5b9755b6390fd838be23fb6b4f15a0d1605`,
  `967e4469aec3414f3dfb28bd06a2f23c0d5acb16eef89076c0ee834037648202`,
  `16110f8813839455f03516288f3fdb88f5b0fdf796234adb5e10fa30aa4d63d6`.
- Representative retained stderr SHA-256:
  `da119565d5448f18b6297eebb2626490dbbb56761e6a9146769641b6d8b928c9`.

The retained command parent environment was:

```text
PYTHONPATH=/home/user/work/wt/agt-pin-bae5ab76:/home/user/work/wt/rt-pin-369ffa7c
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-369ffa7c
ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/wt/rt-pin-369ffa7c
PYTHONNOUSERSITE=1
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules
```

The registry child command in the retained receipt is the `venv-agent` Python
`-c` probe that sets `sys.path[0]` to the rendering pack and inserts the Agent
root. Its stderr traceback is retained under `/tmp/astrid-probe-logs/` and
ends at `from runtime_protocol import platform`.

## Launch-to-failure path

1. `ensure_pack_host()` calls `_prepare_render_validation()` before the fake
   host `popen` in each original test.
2. Candidate `astrid/sdk/host_bootstrap.py:778-793` creates the host env and,
   after the first environment repair, removes `PYTHONNOUSERSITE`.
3. Candidate `astrid/sdk/host_bootstrap.py:830-845` asks
   `_launch_worker_probe_environments()` for source-mode Remotion worker envs.
4. Candidate `astrid/core/execution/generic_host.py:2064-2065` derives
   dependencies using `dependency_pythonpath()` and starts from the filtered
   `build_child_subprocess_env()` result. The source-mode native variant at
   `:2109-2112` reconstructs `PYTHONPATH` from the Agent package root,
   dependency roots, and admitted pack roots. The Runtime checkout is not an
   admitted dependency root merely because it was in the parent `PYTHONPATH`.
5. Candidate `astrid/core/rendering/remotion_runtime.py:748-775` launches
   registry discovery. The child imports `runtime_protocol` at line 26 and
   exits 1 before `_registry_observation()`; `_require_completed_probe()` then
   raises at line 700.

`build_child_subprocess_env()` intentionally excludes arbitrary `PYTHONPATH`
from its base mapping; the source-mode worker projection must explicitly admit
the Runtime import root. This is why the parent command’s Runtime path does not
prove child availability.

## Passing comparison

The actual upstream14 record was the central run
`rt-D118-upstream23-0951-d118-upstream23-targeted-1025095559-19404`: 15 PASS,
1 FAIL, 0 ERROR, with all 14 same-body host rows passing. It used pristine
Agent `08e6b905114a3ee2b05c3e7980421f26b4abf15c` and Runtime
`d4f496ec4fbcae7a1f3a51d47ed5147c561117ad`, and a private overlay first on
`PYTHONPATH`:

```text
/tmp/w-860e2ab8b6/d118-upstream23/overlay/site-packages
/home/user/work/wt/rt-pin-d4f496ec
/home/user/work/wt/rt-pin-d4f496ec/packages/python
/home/user/work/wt/agt-pin-08e6b905
```

The retained upstream child-origin evidence says the overlay resolved
`runtime_protocol` and all required origins only to the pristine Agent/Runtime
roots. The crucial difference is the admitted private Runtime overlay, not the
original 14 test bodies or the Remotion profile.

The core30693 route was also source/profile-authenticated and used Node
`v20.19.4`, profile archive `819acf...`, lock and registry hashes above, but it
ran Agent `120d71202a9ebafa99011aec417cfca6d67fafc2` / Runtime
`1daca2a33f6d7b10053e07c539a54843e3984e19` and its 14 host rows failed at the
earlier unsupported-override guard. Its 8,823 PASS result and passing registry
probe/readiness tests demonstrate the profile is not globally unusable, but do
not qualify these 14 whole-path cases; the retained D122 run is the first
post-`PYTHONNOUSERSITE` result and fails later at child import.

## 14-case accounting

All rows are `REG14`, body-equal to pristine upstream, and fail at the common
child import. The exact retained selectors are:

1. `test_bootstrap_stops_on_correlated_terminal_registration_failure`
2. `test_startup_budget_polling_preserves_identity_and_original_cleanup[None-25-ready-True-25-None]`
3. `[None-None-ready-False-300.0-None]`
4. `[120-25-ready-True-25-None]`
5. `[120-None-ready-False-120-None]`
6. `[120-1-terminal-False-1-None]`
7. `[120-1-foreign_pid-False-1-None]`
8. `[120-1-foreign_birth-False-1-None]`
9. `[120-1-foreign_instance-False-1-None]`
10. `[120-1-foreign_source-False-1-None]`
11. `[120-None-exit-False-1-None]`
12. `[120-400-ready-True-400-400]`
13. `[120-None-ready-False-150.3-30]`
14. `[120-None-exit-False-1-30]`

## Narrow causal repair / ownership

The production follow-up should repair the existing source-mode child import
projection so the authenticated Runtime source/package root is admitted to the
registry child (or use the already-proven private overlay mechanism), while
retaining the strict environment and origin guards. It should not alter
`remotion_runtime.py:700`, weaken validation, change the 14 tests, or treat the
terminal wrapper as the root fault. The product follow-up is owned exclusively
by `agt-D122-host14-source-1201`; this worker made no source or suite change.

## Verification

Static-only investigation; no pytest, lint, full suite, browser, render body,
profile acquisition, or instrumentation was run. The retained original14
bytes and retained provenance were read-only.
