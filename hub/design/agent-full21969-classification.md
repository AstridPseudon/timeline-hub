# Agent full21969 first-failure classification

Date: 2026-10-21 UTC

## Disposition

The retained run is **red but not a valid product qualification**. Its true
first cause is the installed-child environment: the selected \`b979\` child has
no installed \`runtime_protocol\` (or \`astrid_runtime\`) package, while child
processes launched by the current Agent source intentionally sanitize the
parent \`PYTHONPATH\`. The resulting 138 failures and four errors must not be
read as 138 new Agent regressions or as the old \`full5664\` six-node baseline.

No product edit, test edit, dependency mutation, suite request, cancellation,
repeat, or source/test weakening was performed here.

## Exact retained run

Result directory:

\`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-venv-agent-child-published14-b9797941-full-1021045238-21969\`

Request: \`2026-10-21T04:52:38Z\`, target \`integration:agent\`, suite
\`venv-agent-child-published14-b9797941-full\`.

Retained source snapshot:

- Agent tree: \`0698a30b3eb42d47db84ed5ed2e21221158795c4\`.
- Agent integration commit containing that tree: \`cc37291af12ac6504eb48dd71ea39b9dfdb56d71\`.
- Runner synthetic snapshot commit: \`25f13fb3821faf48dc19ad75af24dd3c689866ad\`.
- Retained \`snap\`: \`tree=0698a30b3eb42d47db84ed5ed2e21221158795c4\`,
  \`worktree=/home/user/work/agent\`.

Installed child and compatible Runtime are separate inputs, not one source
identity:

- Child interpreter: \`/home/user/work/venv-agent-child-published14-b9797941/bin/python\`,
  Python \`3.13.16\`; installed marker \`.astrid-source-commit\` is \`b97979411\`.
- Current compatible Runtime: \`/home/user/work/runtime\`, commit
  \`b92d3e7a05eec65c142294ef4873edd059e9b31d\`, tree
  \`6abc2f117391de8e7e35c0283f575a002199894d\`.
- External runner inputs: Runtime \`b92d3e7a...\`, App
  \`bc6f9dd39c7e5154ddf075cb87b7202cf5702e65\`, Composition
  \`7bb54bbd64107e5090643ecca1e4d33164173e85\`.
- Remotion/Node inputs: \`/home/user/work/runtimes/agent-remotion-published14-091aa23e\`,
  Node executable \`/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node\`.

The exact command executed by the central runner was:

~~~text
env -i HOME=/root LANG=C.UTF-8 PYTHONPATH="$PWD:/home/user/work/runtime" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default:/root/.local/bin:/root/.cargo/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-published14-091aa23e ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-published14-b9797941/lib/python3.13/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-published14-091aa23e/node_modules ASTRID_VIBECOMFY_CHECKOUT=/home/user/work/fixtures/vibecomfy PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-child-published14-b9797941/bin/python -m pytest -q -n 3
~~~

The retained suite summary is:

~~~text
138 failed, 15840 passed, 456 skipped, 4 xfailed, 85 warnings,
4 errors, 565 subtests passed in 3351.03s (0:55:51); exit 1
~~~

Runner status is \`fail\`, exit \`1\`, and \`EXIT-MISMATCH\` is absent.
Therefore the terminal failure is interpreted explicitly as a real failing
run, not silently passed; its environment is nevertheless disqualified for
product attribution.

## True first cause

The first listed failure is:

\`tests/core/execution/test_custody_broker.py::test_isolated_wrapper_reaches_fake_peer_without_workload_startup_hook\`

Its child stderr is:

~~~text
Error in sitecustomize; set PYTHONVERBOSE for traceback:
ModuleNotFoundError: No module named 'runtime_protocol'
~~~

The same direct cause appears in 73 failure traces. The retained Remotion
probe stderr independently shows the identical import failure at
\`astrid/core/rendering/remotion_runtime.py:26\`; those probes then surface as
\`RemotionValidationError\` with \`original_wait_exit_code=1\` during
\`registry_discovery\`. This explains the three managed-scene setup errors and
the broad child-host/rendering cascades. The parent test process can import
Runtime because the runner command includes \`/home/user/work/runtime\` in
\`PYTHONPATH\`; sanitized child environments do not retain that checkout path.

This is consistent with the independent b979 hermetic diagnosis: the child
contains installed Agent/client files but no \`runtime_protocol\` or
\`astrid_runtime\`. It is an installed-profile/provisioning failure, not proof
that the current Agent tree regressed those behaviors.

There is one separate collection error:

\`tests/sdk/test_scene_real_public_summary_rle.py::test_real_public_scene_answers_reach_rle_summary\`

reports \`fixture 'native_host' not found\`. It is not explained by the direct
missing-module trace and was not independently rerun; leave it unclassified
until a coherent profile can exercise the test's plugin boundary.

## Comparison with old full5664 six-node result

None of the six exact old nodes appears in the retained run's terminal
\`FAILED\` or \`ERROR\` list:

1. \`tests/core/rendering/test_production_callers.py::test_no_production_backend_imports_outside_allowlist\`
2. \`tests/packs/test_composition_elements.py::CompositionElementTest::test_bundled_element_registries_generate_together\`
3. \`tests/packs/timeline/test_cli_commit_move.py::test_ordinary_edit_occurrence_move_keeps_legacy_owner_resolution\`
4. \`tests/test_artifact_manifest.py::test_committed_artifact_manifest_is_current\`
5. \`tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale\`
6. \`tests/timeline/test_timeline_kernel_kinds.py::DoctorV10ChecksTest::test_public_doctor_route_fails_closed_without_runtime\`

This is suite-level evidence only: no new targeted run was made, as required.
The exact old reference remains the separate \`full5664\` result: 6 failed,
14,884 passed, 452 skipped, 4 xfailed, 84 warnings, 565 subtests passed,
using Agent tree \`8626f868...\`, installed child \`c13-5c5173dc\`, and pinned
Runtime \`9d1c43c6...\`. Its six source/test classifications therefore remain
valid and are not replaced by this environment-invalid run.

## Recommendation

No owned product follow-up is justified from this run. The smallest manager
follow-up is to provision one private coherent installed profile containing
the exact selected Agent wheel plus Runtime packages (\`runtime_protocol\` and
\`astrid_runtime\`) and then perform the already-approved single qualification
run only after its hermetic import/origin checks pass. Do not repair tests or
attribute the 138 failures to current source until that profile is available.

