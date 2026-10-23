# F-unconfirmed-env bounded diagnosis

Date: 2026-10-23 UTC  
Scope: the 13 host/installer/publication-chain failures retained from sole full4249.

## Result

The bounded rerun used the durable 0856 environment and the existing test service. It ran 13 collected nodes (the two parameterized nodes in the claimed-task test and the two installer parameters are included in that count): **9 passed, 4 failed, exit 1, 23.44s**.

Command/result identity:

```text
env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$PWD:/home/user/work/runtime:/home/user/work/agent-runtime-projection-0856/site-packages" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:... \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-composition14-255b6856 \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages \
  ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-composition14-255b6856/node_modules \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_legacy_assembler_admission_refuses_before_execution_and_keeps_artifacts \
  tests/test_generic_host.py::test_idle_remotion_empty_polls_and_canonical_renewal_skip_only_native_walk \
  tests/test_generic_host.py::test_idle_remotion_claimed_task_full_preflight_failure_settles_exact_lease \
  tests/test_generic_host.py::test_idle_remotion_runtime_transport_failure_blocks_claims_until_successful_renewal \
  tests/test_generic_host.py::test_idle_remotion_parallel_slots_copy_observation_and_honor_parent_fence \
  tests/test_generic_host.py::test_structure_pack_members_survive_harvest_cleanup_and_reopen \
  tests/test_installer_service_repair_integration.py::test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids \
  tests/test_generic_host.py::test_idle_remotion_parallel_real_claim_loop_renews_without_full_walk \
  tests/test_generic_host.py::test_idle_remotion_parent_fence_during_idle_check_prevents_claim_rpc \
  tests/test_generic_host.py::test_idle_remotion_parent_fence_during_selected_full_check_fails_lease
```

The central result was `agt-F-unconfirmed-env-0900-targeted-1023090053-24359`; its snapshot was Agent tree `6f7649a4e0b8f1d936dc94a5fa0bb7c5fb3db276`. The sole full4249 snapshot was `fcc33e0eb964dd48d422673e8f692f195c88748c`, Agent commit `d24da4af0f1ca83880b4b9ef57559e28ebe52a2a`, and ended `240 failed, 16388 passed, 40 skipped, 5 xfailed, 140 errors`, exit 1, after 4269.86s. This bounded result is not full-suite qualification and gives no credit to later fixes outside the tested snapshot.

## Exact causal map

| Exact node(s) | Evidence-backed classification | Cause and next owner |
| --- | --- | --- |
| `test_d13_installed_native_preflight` | Environment/resource blocked | The full4249 trace lacked the D13 contract inputs. The durable rerun still reports missing `ASTRID_D13_SOURCE_PROFILE`, `ASTRID_D13_EXPECTED_BINDINGS`, the binding fields, native/browser/tool digests, and the browser/ffmpeg/ffprobe paths. The existing test requires a regular non-symlink bindings file with the exact Agent/source keys; no fake admission is valid. Owner: farm/installer fixture provisioning. |
| `test_legacy_assembler_admission_refuses_before_execution_and_keeps_artifacts` | Current source-backed failure; upstream status untested | `generic_host.py:8897` calls `_renderer_selection`; `generic_host.py:1639` unconditionally reads `record.adapter.remotion`. The test intentionally supplies a minimal `SimpleNamespace` record without `adapter`, so admission settles with `"'types.SimpleNamespace' object has no attribute 'adapter'"` before `_assert_fixed_request_scope` can produce the required `immutable original target` refusal. Owner: Agent generic-host/admission owner; preserve fenced failure and untouched proposal while making the admission helper handle the supported minimal record shape. |
| `test_idle_remotion_empty_polls_and_canonical_renewal_skip_only_native_walk` | Environment-sensitive; passes in bounded durable rerun | Full4249 observed zero claim RPCs (`claim_calls == 0`); the same node passed with durable projection, Node 20.19.4 and Composition 0.0.14. No current source defect is proven and no upstream claim is made. Owner: farm durability review, then rerun if the post-exit review changes the environment. |
| `test_idle_remotion_claimed_task_full_preflight_failure_settles_exact_lease[unavailable]` | Environment-sensitive; passes in bounded durable rerun | Full4249 did not raise the expected fenced HostError; durable rerun passed. The expected path is the selected-task full preflight before materialization. No source regression is proven. Owner: farm environment review. |
| `test_idle_remotion_claimed_task_full_preflight_failure_settles_exact_lease[exception]` | Environment-sensitive; passes in bounded durable rerun | Same evidence as the `unavailable` parameter: the durable rerun raises/settles as required; full4249 did not. Owner: farm environment review. |
| `test_idle_remotion_runtime_transport_failure_blocks_claims_until_successful_renewal` | Environment-sensitive; passes in bounded durable rerun | Full4249 resumed with zero claim calls after successful renewal; durable rerun passed the offline/renewal fence sequence. Owner: farm durability review. |
| `test_idle_remotion_parallel_slots_copy_observation_and_honor_parent_fence` | Environment-sensitive; passes in bounded durable rerun | Full4249 observed zero claims for the two slots; durable rerun passed both slot claims and the parent fence. Owner: farm durability review. |
| `test_structure_pack_members_survive_harvest_cleanup_and_reopen` | Environment/resource blocked in full; passes with durable projection | Full4249 child traceback was `ModuleNotFoundError: runtime_protocol` from `astrid/core/foundation/atomic_io.py` in the external command. The durable rerun passed. Owner: environment provisioning; no source repair inferred. |
| `test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[False-0]` | Environment/resource blocked before repair assertions | Both parameters fail at the initial isolated `Backend.runtime` call (`backend.py:77` → `Backend.run`), before registration/start/repair. `-I -m astrid_runtime` cannot find `astrid_runtime` in `venv-agent`; an independent exact probe returns `No module named astrid_runtime`, and `-I` ignores `PYTHONPATH`. Owner: installer environment/provisioning; supply the actual isolated Runtime package in `version.python` or the existing packaged executable. |
| `test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[True-1]` | Same environment/resource blocker | Same initial `astrid_runtime` import failure; the `fail_log_open` branch is never reached. Owner: installer environment/provisioning. |
| `test_idle_remotion_parallel_real_claim_loop_renews_without_full_walk` | Environment-sensitive; passes in bounded durable rerun | Full4249 timed out in the claim loop; the durable exact node passed in the bounded run and completed cleanup. No current source or upstream causality is proven. Owner: farm durability review. |
| `test_idle_remotion_parent_fence_during_idle_check_prevents_claim_rpc` | Environment-sensitive; passes in bounded durable rerun | Full4249 did not raise the parent-fence error; durable exact node passed with zero claim RPCs. Owner: farm durability review. |
| `test_idle_remotion_parent_fence_during_selected_full_check_fails_lease` | Environment-sensitive; passes in bounded durable rerun | Full4249 did not raise or settle the expected fenced lease; durable exact node passed. Owner: farm durability review. |

The seven idle/host nodes above are not relabeled upstream or deferred by assumption: they have a same-source, durable-environment PASS, but the rerun does not isolate which full4249 environment difference caused the original behavior. The 0856 environment report records the relevant changes as the durable `site-packages` projection, Node `v20.19.4`, and the normal Composition `0.0.14` graph. Independent post-exit startup review is still pending.

## Import and security evidence

The durable projection is `/home/user/work/agent-runtime-projection-0856/site-packages`; its `runtime_protocol` link resolves to `/home/user/work/runtime/runtime_protocol`. The old `/tmp/w-5829dd921/site-packages` path is absent. An exact clean-environment origin probe reported:

```text
astrid /home/user/work/wt/agt-F-unconfirmed-env-0900/astrid/__init__.py
runtime_protocol /home/user/work/runtime/runtime_protocol/__init__.py
astrid_runtime_client /home/user/work/wt/agt-F-unconfirmed-env-0900/astrid_runtime_client/__init__.py
banodoco_timeline_schema /home/user/work/venv-agent/lib/python3.13/site-packages/banodoco_timeline_schema/__init__.py
node v20.19.4
```

The qualified Composition lock digest is `b7c4ab2e3c3f466d9d1c0c8d7472a40101d37b6288d52b930067dc663a17feb0`. The 0856 report also records positive-origin, missing-source negative-refusal, Node 22 negative-guard, and normal renderer-graph checks. No source, test, fixture, pin, shared dependency, launcher, process, or security-guard changes were made here.

## Smallest next repair group

1. Farm/installer provisioning: provide the exact D13 profile/bindings/native tuple and an isolated `astrid_runtime` installation usable by the test's `version.python -I` command. Rerun only D13 and the two installer parameters first.
2. Agent generic-host owner: repair the minimal admission-record incompatibility at `_renderer_selection` while retaining the immutable-publication refusal and artifact-preservation assertions. Rerun the one legacy node.
3. Farm owner: complete the independent post-exit startup/durability review, then repeat the seven host/idle nodes only if that review changes the environment. Do not request a full run from this report.

## Limits

No source/test/fixture/environment/pin/shared-dependency change was made by this worker. No browser, render, heavy journey, P1/P4 HTTP, native14, crash24, or full suite was run. The exact D13 environment is not present, so D13 remains unadmitted rather than fabricated. This report makes no full-qualification claim and makes no authentic-upstream-431 claim; no upstream baseline was executed.
