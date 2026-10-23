# F-D22 exact actual-integrated custody proof

## Verdict

**PASS, scoped to the exact three requested nodes on the actual integrated
Agent tree.** This is proof-only. No product, test, generated, pin, lock,
dependency, environment, Git ref, daemon, or shared-install change was made
by this worker.

The exact evidence is recorded from temporary `report.md`; that temporary
root report is removed after this copy so the product worktree remains free of
report artifacts.

## Source and custody

Start and end identity were identical:

```text
Agent HEAD:  d682c5977e0d5a7627ca04852980a2d65ca899d4
Agent tree: 7d86b443453d9498569a7eee0c53410a5bbdc6a3
Base:        d682c5977e0d5a7627ca04852980a2d65ca899d4
Base tree:   7d86b443453d9498569a7eee0c53410a5bbdc6a3
Runtime HEAD: 9ce4242bc01f100bab9efc51032a73985cefb2b2
Runtime tree: 92ab1f5f739ffdfedf7b25fbd2a7b46ae42c5d1a
```

The exact two fixture blobs equal both independent author `3ef951f3a` and
review/cleanup `8f0d10001`:

```text
tests/core/execution/test_custody_broker.py
  blob 41745ad6e4fed962b0a21885b680d65c1a50e2d6
  sha256 b743e1edc49574dacd6a750d07fa6f9201519693309512b3b8b6184307a74610
tests/core/rendering/test_installed_registry_security.py
  blob 1d251cc50d67d41d6ffbc2767d759283d9ffc585
  sha256 fbe2476030da04776fe5c53a0bf0c999f0b438643b05b9af6ba32f2430de88d1
```

`git diff --quiet 58316fd6e0ce8a1fb3b2b3826ec71906d29080de..HEAD -- astrid`
passed: all product bytes are exact to 583. The fixture diff contains only
the already reviewed custody-wrapper Runtime source-root restoration and the
supported schema-path propagation in the two projection environments. The
original custody assertions and refusal/guard assertions are unchanged.

Production source SHA-256 values, each equal to the 583 baseline:

```text
83b7a8124e3f42f6ceffa966e22be8c5695a5434066be08c554b60fd69e57e94  astrid/core/execution/custody_broker.py
fc020cc2f6256642203fc4d36a9bb661265fa9a9589d386a46963528d11791d3  astrid/core/execution/generic_host.py
bce716c4c544f3247f189100c6fc74ab1decb2e7f9191196e92386959d5861b  astrid/core/execution/process_group.py
84a495de2139c74b22c001094a3bb4d9252803f11715d7803054ecc2f9cc617e  astrid/core/rendering/remotion_runtime.py
```

The actual imported origins were captured with the supported environment:

```text
python:          /home/user/work/venv-agent/bin/python
Agent custody:   /home/user/work/wt/agt-F-D22-custody-integrated-1542/astrid/core/execution/custody_broker.py
Agent remotion:  /home/user/work/wt/agt-F-D22-custody-integrated-1542/astrid/core/rendering/remotion_runtime.py
Runtime platform: /home/user/work/runtime/runtime_protocol/platform.py
schema path:     /home/user/work/venv-agent/lib/python3.13/site-packages
```

## Exact bounded run

Exactly three original nodes were selected: the engine custody node (the
command counterpart was already qualified by the author and was not repeated)
and the two original projection checks in the supported environment.

Central targeted service request:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-F-D22-custody-integrated-1542 targeted --files "tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[engine] tests/core/rendering/test_installed_registry_security.py::test_installed_native_readiness_context_must_match_projected_context tests/core/rendering/test_installed_registry_security.py::test_installed_actual_worker_environment_matches_launch_projection[command]"
```

The service captured this exact supported environment and command:

```text
env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime:/home/user/work/agent-runtime-projection-0856/site-packages" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/bin:/bin ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-composition14-255b6856 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-composition14-255b6856/node_modules /home/user/work/venv-agent/bin/python -m pytest -q tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[engine] tests/core/rendering/test_installed_registry_security.py::test_installed_native_readiness_context_must_match_projected_context tests/core/rendering/test_installed_registry_security.py::test_installed_actual_worker_environment_matches_launch_projection[command]
```

The imported Runtime origin was `/home/user/work/runtime/runtime_protocol/platform.py`,
Runtime was `9ce4242bc01f100bab9efc51032a73985cefb2b2`, and the schema path was
`/home/user/work/venv-agent/lib/python3.13/site-packages`.

Result: **3 passed in 10.96s**, service wall time **13s**, exit 0. Service
result: `agt-F-D22-custody-integrated-1542-targeted-1023154311-7230`.

## Static evidence

```text
git diff --check 58316fd6e0ce8a1fb3b2b3826ec71906d29080de..HEAD PASS
/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json PASS
/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check PASS
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m compileall -q tests/core/execution/test_custody_broker.py tests/core/rendering/test_installed_registry_security.py PASS
```

Reused unchanged independent review evidence: Ruff zero new findings;
private mypy current 1912 versus baseline 1912; reviewed cleanup left no
tracked report or generated artifact.

## Limits

Only the three-node proof above is credited. The clean-environment projection
pair, static full run, browser/live journey, daemon, native14, full D22 census,
and seven historical managed/CPU process nodes were not repeated. Those seven
remain **UNCONFIRMED**. The separate current installed `9`-pass result on its
different pair remains retained and is not credited here. No broader D22 PASS
is claimed.
