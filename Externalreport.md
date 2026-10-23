# F unconfirmed13 independent review — FAIL for qualification

Date: 2026-10-23 UTC  
Reviewed tree: `tl/integration` / Agent `2e21af300abbefc8afbad217189fa4715cf82616`  
Authoritative bounded evidence: `agent-F-unconfirmed-env-0900.md`  

## Verdict

The bounded lane is **FAIL**: the central service result is **13 collected,
9 passed, 4 failed, exit 1, 23.44s**. This is an independent review of the
existing evidence, not a product or test change and not a full-suite
qualification.

Central evidence command (read from the service result; not rerun by this
reviewer) was:

```text
env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$PWD:/home/user/work/runtime:/home/user/work/agent-runtime-projection-0856/site-packages" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/root/.cargo/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin \
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

Service artifacts: `.../orch/tests/agt-F-unconfirmed-env-0900-targeted-1023090053-24359/{summary,log.txt,snap}`.

The author report's prose says “seven hostnodes” pass. The exact result has
nine PASS identities; this report records the exact count and identities
without rewriting the author report:

- `tests/test_generic_host.py::test_idle_remotion_empty_polls_and_canonical_renewal_skip_only_native_walk`
- `tests/test_generic_host.py::test_idle_remotion_claimed_task_full_preflight_failure_settles_exact_lease[unavailable]`
- `tests/test_generic_host.py::test_idle_remotion_claimed_task_full_preflight_failure_settles_exact_lease[exception]`
- `tests/test_generic_host.py::test_idle_remotion_runtime_transport_failure_blocks_claims_until_successful_renewal`
- `tests/test_generic_host.py::test_idle_remotion_parallel_slots_copy_observation_and_honor_parent_fence`
- `tests/test_generic_host.py::test_structure_pack_members_survive_harvest_cleanup_and_reopen`
- `tests/test_generic_host.py::test_idle_remotion_parallel_real_claim_loop_renews_without_full_walk`
- `tests/test_generic_host.py::test_idle_remotion_parent_fence_during_idle_check_prevents_claim_rpc`
- `tests/test_generic_host.py::test_idle_remotion_parent_fence_during_selected_full_check_fails_lease`

## Exact inventory audit

The sole full run was `agent-full-1023072419-4249`, snapshot
`fcc33e0eb964dd48d422673e8f692f195c88748c`, Agent commit
`d24da4af0f1ca83880b4b9ef57559e28ebe52a2a`: **240 failed, 16,388 passed,
140 errors, 40 skipped, 5 xfailed, exit 1, 4,269.86s**.
Its recorded command was
`env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -n 3`.

The bounded command has 11 selectors. Expanding its two two-parameter tests
produces exactly 13 unique nodes. A read-only comparison against the full
report's 24-node unconfirmed inventory found:

- all 13 are present exactly once;
- no bounded node is omitted or duplicated;
- the other 11 unconfirmed full-run nodes are not silently credited or
  reclassified here.

No credit is taken for a newer Agent head: the bounded result is snapshot
`6f7649a4e0b8f1d936dc94a5fa0bb7c5fb3db276`, while the full result is the
separate `fcc33e...` snapshot. No upstream-431 baseline was run, so there is
no upstream/pre-existing credit. D14 contributes zero nodes and zero credit;
the two deferred anchor-undo positives were not exercised by this lane.

## Four exact failures and causes

1. **D13 installer preflight — environment/resource blocked.** The exact
   profile, regular bindings file, source/agent/wheel digests, native Node and
   Remotion lock digests, browser path/digest, and ffmpeg/ffprobe paths/digests
   are absent. The test requires the real non-symlink tuple; no admission is
   earned by an ordinary renderer environment. Owner: farm/installer fixture.

2. **Legacy assembler admission — current source-backed failure.** The test's
   intentionally minimal `SimpleNamespace` capability record has no `adapter`.
   `_renderer_selection` dereferences `record.adapter.remotion` at
   `astrid/core/execution/generic_host.py:1639`, from the admission call at
   line 8897, before `_assert_fixed_request_scope` at line 8902 can produce
   the required `immutable original target` refusal. The proposal remains
   untouched in the observed failure. Owner: Agent generic-host/admission.
   Upstream status is untested.

3. **Installer repair `[False-0]`.**

4. **Installer repair `[True-1]`.**

   Both parameterizations fail at the initial isolated launch
   `version.python -I -m astrid_runtime` (`astrid/installer/backend.py:77`),
   before registration, service start, repair, or PID assertions. The exact
   diagnostic probe
   `/home/user/work/venv-agent/bin/python -I -c 'import astrid_runtime'`
   returned `ModuleNotFoundError: No module named 'astrid_runtime'`.
   `-I` ignores `PYTHONPATH`; this is an installer environment blocker, not a
   repair-behavior result. Owner: farm/installer provisioning.

The nine PASS nodes pass under the durable 0856 projection with Node
`v20.19.4`, Composition `0.0.14`, and `runtime_protocol` resolving from the
Runtime checkout. They establish environment-sensitive bounded PASS only;
they do not prove the cause of the original full-run behavior and do not
grant full or upstream credit.

## Production caller and v2 static trace

Static source inspection is **PASS**, with no live acceptance claim:

- `Timeline.open` uses `AstridClient.open_from_launcher` and
  `TimelineSession.open` (`astrid/sdk/timeline/commit_session.py:260-277`).
- The production flush builds the exact request body and sends it through
  `client.timelines.commit` (`astrid/sdk/timeline/sync.py:514-547`), then
  `WorkspaceClient.commit_timeline` delegates to the generated client
  (`astrid/sdk/workspace_client.py:485-498`; generated POST at
  `generators/python_client_template.py:940-965`).
- The render production caller is the backend-neutral `RenderService`: the
  canonical render action constructs the service (`astrid/packs/rendering/actions/render/run.py:87-96`),
  and service resolution/invocation selects the registered actual backend
  rather than importing a concrete backend from the caller.

The unchanged full-v2 request surface contains `api_version`, scope IDs,
the exact `base_revision_id`/`base_publication_id` pair, `commands`, `label`,
complete per-step fields (`id`, `label`, `intent`, `tags`,
`command_ordinals`, `patch`, optional `reads`), `merge`, request `reads`,
idempotency `key` (header), `dry_run`, `source`, `rationale`, and `group_id`.
The response contract retains `{data, receipt}`; `accepted`, `merged`, and
historical `rebased`; head/document/records plus dependencies/effects/steps;
history and `undo_steps`; preview with required `would_status`; conflict
`reason` and head; and invalid `code`, `path`, `hint`, and suggested
`command`. The Runtime wire spelling for the historical status is `rebased`.

## Limits and next owners

No product, test, fixture, environment, source, pin, schema, contract, or
shared-dependency files were changed. No full rerun, browser, heavy journey,
P1/P4 HTTP, native14, crash24, or D14 run was performed. The only new
diagnostic was the one isolated installer import probe above.

Next owners are: farm/installer for the exact D13 tuple and isolated
`astrid_runtime`; Agent generic-host for minimal-record admission while
preserving the refusal and artifact assertions; and farm durability review
for the nine environment-sensitive PASS nodes. Do not claim full, newer-head,
upstream, or D14 credit from this review.
