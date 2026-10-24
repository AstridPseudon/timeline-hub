# D40 installed prerequisite review — FAIL / NOT READY

The prep report’s six-argument request is incorrect. `request-child-venv` accepts:

```text
NAME AGENT_SHA BASE_SUITE REMOTION_GRAPH \
--source-carrier AGENT_CHECKOUT RUNTIME_CHECKOUT RUNTIME_SHA
```

The exact supported form is:

```bash
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-child-venv \
  venv-agent-child-d40-original-252cf-f320 \
  252cf33d02184abcba4664634802291cfc791ca3 \
  venv-agent-child-d22-8c3b926e \
  agent-remotion-v3-819acf-1110 \
  --source-carrier \
  /home/user/work/wt/agt-pin-252cf33d \
  /home/user/work/wt/rt-pin-f3208b26 \
  f3208b26b53c4d7053e5464eaa7c5e15b1505812
```

This was not run. The Agent source-carrier checkout does not exist because the prep worker was recycled. The required normal checkout is:

```bash
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-checkout \
  agent 252cf33d02184abcba4664634802291cfc791ca3 \
  "D40 installed exact Agent source carrier"
```

`venv-agent-child-d22-8c3b926e` is the current plain-layout base selector, and `agent-remotion-v3-819acf-1110` is the existing Remotion selector. The apparent original-node selector, `d09-current-v3-1113`, is stale and points at the recycled `f1012-installed/venv` layout; it must not be reused.

## Evidence

- Exact Agent commit: `252cf33d02184abcba4664634802291cfc791ca3`.
- Exact Runtime commit: `f3208b26b53c4d7053e5464eaa7c5e15b1505812`.
- Runtime checkout `/home/user/work/wt/rt-pin-f3208b26` is clean.
- Agent commit’s four canonical client file hashes exactly match Runtime f320’s client hashes.
- Current `/home/user/work/agent` and `/home/user/work/runtime` are clean but at unrelated revisions.
- `/home/user/work/wt/agt-F-D40-installed-prep-0354` is absent.
- Free disk: `10,685,194,240` bytes, approximately `9.95 GiB`. The store reserves 8 GiB; observed child sizes are roughly 0.65–0.9 GiB, so only about 1–2 GiB of build headroom remains. This is borderline and should be checked again immediately before provisioning.
- Required profile is Remotion archive `819acf6b…`, lock `f4fc0a32…`, Node `v20.19.4`, with origins recorded in the installed child. No ambient `PYTHONPATH`, editable install, digest-only trust, or relabeled stale environment is acceptable.

## Decisive blocker

The original test exercises an external Python `orchestrator` through:

```text
host.admit("orchestrator", ...)
host.invoke_capability(capability_kind="orchestrator", ...)
```

Current D40 custody handling only selects externally captured executor/action definitions. `invoke_capability` requires the definition to be in `self.capabilities`, while orchestrators admitted through the existing path are not registered there. The worker also passes captured source bytes to executor execution, not to the orchestrator runner.

The actual approved Runtime boundary is `TrustedLocalHostLaunchVerifier`; the prep report’s `RuntimeHostLaunchVerifier` name is not an existing class. Therefore the original orchestrator invocation cannot currently run through the approved existing launch boundary. A setup-only fixture seam is insufficient; changing the consumer path would be required. I made no product changes.

## Required future acceptance

Preserve the original fixture bytes, predicates, `host.admit`, `host.invoke_capability`, and assertions. Add only a Git-backed temporary fixture checkout, private Runtime owner grant, `OwnerSourceCapture`, retained preparation/profile binding, and launch through `TrustedLocalHostLaunchVerifier`.

After the consumer-path blocker is resolved and the exact child exists, the acceptance selector is:

```bash
/home/user/work/venv-agent-child-d40-original-252cf-f320/bin/python -P -m pytest -q \
  -o addopts= -p no:cacheprovider \
  tests/stage1/test_zero_shim_execution_pack_deletion.py::test_generic_host_runs_external_python_orchestrator_from_admitted_pack
```

No tests, provisioning, launch, or rejected six-argument request were run. PLAN §3 and `design/commit-v2.md` were reviewed; no schema, client, pin, Git, or test changes were made.