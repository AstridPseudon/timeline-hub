# F D18 pinned-Node harness return

## Result

The authorized correction to the existing D09 service row was applied and
one central activation was run.  The pinned Node hurdle is resolved: the
installer node passed, the owned registry child completed positively, and the
D09 setup reached the next validation stage.  D09 then stopped before its
test body on a composition-package version mismatch.

Central test ID:

`agt-F-D18-node-return-1049-agt-F-installed-return-1012-installed-env-one-installer-d09-1023105154-24161`

Central result: **exit 1; 1 passed, 1 error in 62s**.

- Installer node: **PASS**.
- D09 node: **ERROR during autouse fixture setup**, before the D09 body.
- No Agent-tool or autoclassifier safety denial occurred.
- No retry, assertion edit, guard edit, package install, build, daemon, native,
  HTTP, browser, full suite, or shared-dependency write was performed.

## Authorized harness change

Only the existing named row in `ORCH/tests/suites.conf` was changed.  Its
isolated `PATH` is now:

```text
/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent-child-f1012-installed/venv/bin:/usr/bin:/bin
```

The exact pinned executable reports `v20.19.4`.  `PYTHONNOUSERSITE` remains
absent.  The row retains exactly the original two test nodes and no other row
was changed.

Outside-named-row SHA-256 remained:

`df3d20c8204ff4b9b41bb381014119132b50d7dbd2fc4a47ae4ba9df7db751a8`

The corrected named-row SHA-256 is
`0cc15ed0445399ef1997fc4dffb77a242c399732f1837f481c8df4ba27c82c3c`.

## Preflight evidence

- `bash -n` on the exact corrected row command: **PASS**.
- Exact two-node collection under the corrected isolated `PATH`:
  **PASS, 2 tests collected in 1.48s**.
- Agent source identity remained commit
  `7abfb8d69f625d0aada79346d5806f5f9525ed8c`, tree
  `9618a0928a361eca8f172e0bf56a1ae5d0e472fa`.
- Fixture blob remained `dfe8ed9a4d0fc8870b76079889b1cb9c9b3bd9d4`;
  its SHA-256 remained
  `6098692c7edcbf8d918c436f8c5303f787a005f08d264618e73c5c72a8374efa`.
- Runtime guard SHA-256 remained
  `84a495de2139c74b22c001094a3bb4d9252803f11715d7803054ecc2f9cc617e`.
- Installer test SHA-256 remained
  `d4ed5f4efc884b5d347f72b19e35a02be822c426638a0cc4deb78c09a577fb8a`.
- Durable installed root `/home/user/work/venv-agent-child-f1012-installed`
  retained the previously qualified wheel hashes, 164-pin inventory, private
  profile, and all 182 recorded RECORD files.  The current read-only checks
  passed for the profile and all 182 RECORD file hashes.
- The actual isolated installed registry probe, using the real public Remotion
  project and pinned Node, passed with registry state hash
  `32b312f5ea7b2a67717a79ae71b539510590e9010e2ec7f77c8bce1edbabbfc6`.

The preflight commands were:

```text
bash -n <<<"$(sed -n '/^agent agt-F-installed-return-1012-installed-env-one-installer-d09 /{s/^[^ ]* [^ ]* //;p;}' ORCH/tests/suites.conf)"
env -i HOME=... PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent-child-f1012-installed/venv/bin:/usr/bin:/bin ... /home/user/work/venv-agent-child-f1012-installed/venv/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider --collect-only \
  'tests/test_installer_service_repair_integration.py::test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[False-0]' \
  tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result
```

The registry preflight used the same isolated executable and environment,
with `ASTRID_HOST_EXECUTION_PROFILE=installed`,
`ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0013`,
`ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`,
and `_registry_origin.installed_argv(...)`; the child returned a positive
registry observation.

## Retained causal trace

The prior D18 result remains classified as a harness invocation defect.  Its
installer node passed, while D09 setup failed in registry discovery because
the isolated environment had neither pinned Node on `PATH` nor a selector
retained by the registry child.  The Runtime guard was byte-identical and no
Agent/autoclassifier refusal occurred.  Its log is:

`ORCH/tests/agt-F-D18-supported-invocation-1045-agt-F-installed-return-1012-installed-env-one-installer-d09-1023104628-20337/log.txt`

After the authorized `PATH` correction, the new retained log is:

`ORCH/tests/agt-F-D18-node-return-1049-agt-F-installed-return-1012-installed-env-one-installer-d09-1023105154-24161/log.txt`

The new trace records completed owned probes and completed registry settling,
then fails in `_runtime_inputs()` with:

```text
RemotionValidationError: installed Remotion package manifest has unexpected version: '0.0.13'; expected 0.0.14
```

This is not a Node or registry failure.  The exact source-backed mismatch is:

- Agent validator: `astrid/core/rendering/_remotion_package.py:10` sets
  `_COMPOSITION_PACKAGE_VERSION = "0.0.14"`, and lines 52–54 reject any other
  manifest version.
- D09 fixture: `tests/integrations/test_d09_managed_scene_only.py:32` selects
  `/home/user/work/runtimes/agent-remotion-0013`, and lines 116–117 assert the
  `banodoco-timeline-composition-0.0.13.tgz` dependency.
- Observed artifact:
  `/home/user/work/runtimes/agent-remotion-0013/node_modules/@banodoco/timeline-composition/package.json`
  declares version `0.0.13`.

The owner is the Composition package/runtime fixture alignment boundary.  The
existing public13 artifact and the installed Agent validator are from
different composition-version contracts.  This worker was not authorized to
change either package, fixture, manifest, pin, or assertion.

## Contract surface

No product contract bytes were changed.  The production caller remains the
real isolated CLI/Runtime managed-scene route.  The full v2 request/reply
surface (base pair, commands, label, full steps with patches and ordinals,
merge fields, declared reads, idempotency key, `dry_run`, source, rationale,
group ID; accepted/merged/historical-rebased replies; canonical records,
dependencies, effects, steps, history, undo steps, preview,
`would_status`, conflict reason/head, and invalid code/path/hint/command)
remains unchanged.

## Next step

Do not retry this unchanged row.  Reconcile the public Remotion artifact and
the Agent validator’s required Composition version through the responsible
Composition/runtime integration owner, then obtain a fresh explicit run
authorization if D09 qualification is still required.  Until then, D09 body
behavior, retained-result assertions, and the live child-origin assertion
remain unverified.
