# F D18 supported-invocation correction

## Scope and decision

This worker applied the D18-authorized harness correction to the existing
orchestration row only. The change removed the unsupported
`PYTHONNOUSERSITE=1` binding from
`agt-F-installed-return-1012-installed-env-one-installer-d09` in
`ORCH/tests/suites.conf`. No Agent, Runtime, test, fixture, client, pin,
guard, installed package, manifest, daemon, launcher, or shared worktree was
changed.

The decision follows D18 and the supplied escalation: the prior
`RemotionValidationError` was a harness invocation defect, not an Agent or
autoclassifier safety refusal. Runtime's `_UNSUPPORTED_PYTHON_STARTUP` guard
was preserved byte-for-byte.

## Source and durable custody preflight

- Agent source remained `7abfb8d69f625d0aada79346d5806f5f9525ed8c`, tree
  `9618a0928a361eca8f172e0bf56a1ae5d0e472fa`.
- The reviewed Agent parent is `ef851b22c506245441b9a630c093b3460e39cbdc`,
  tree `b11eee891208d11e23c55950f8954ddd3377d5a8`.
- The actual fixture blob at the reviewed `7ab` tree remains
  `dfe8ed9a4d0fc8870b76079889b1cb9c9b3bd9d4`, matching the independent 956
  review. Its current SHA-256 is
  `6098692c7edcbf8d918c436f8c5303f787a005f08d264618e73c5c72a8374efa`.
- Durable source custody remains the independently qualified Agent `ef851`
  extract and Runtime `1365e4b17b31c4a7093d5943674637067fd2bab4` extract;
  both were previously verified exact and symlink-free. The current Agent
  tree and fixture identities are unchanged, so the independent 1021/1038
  custody checks were reused as authorized.
- Durable install root: `/home/user/work/venv-agent-child-f1012-installed`.
  Profile remains the private source/runtime site-packages root and private
  venv. The 164-pin digest remains
  `478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`.
- Wheel hashes remain:
  - Agent `fcccab4dc881faa4eead1f971fc655dc96ebfac9efac199015794d7b644007e3`
  - Runtime `aac07960e997c8881a594d6d9a3e18eccfef6828dc15cab9fc0f3fd25f941c49`
  - Runtime client `f0cb9f222c5d2697eb8c1d912cccfce30fa058530a1471b8441b54b4546497a4`
- All 182 recorded RECORD files still match the durable pre-exit manifest;
  the direct check found 0 missing and 0 mismatched files. The independent
  review records 26,679 RECORD rows unchanged.
- Guard and relevant test hashes were unchanged:
  - `astrid/core/rendering/remotion_runtime.py`:
    `84a495de2139c74b22c001094a3bb4d9252803f11715d7803054ecc2f9cc617e`
  - `tests/integrations/test_d09_managed_scene_only.py`:
    `6098692c7edcbf8d918c436f8c5303f787a005f08d264618e73c5c72a8374efa`
  - `tests/test_installer_service_repair_integration.py`:
    `d4ed5f4efc884b5d347f72b19e35a02be822c426638a0cc4deb78c09a577fb8a`

## Orchestration row proof

The named row remained line 5 and retained its two original test nodes. The
only row change was removal of `PYTHONNOUSERSITE=1`.

- Outside-named-row SHA-256 before and after:
  `df3d20c8204ff4b9b41bb381014119132b50d7dbd2fc4a47ae4ba9df7db751a8`.
- New named-row SHA-256:
  `0225b7d034f56ed84c6a35d90905ddf15ca2cac86db552292fa3bba7b467e936`.
- New row contains no `PYTHONNOUSERSITE` and exactly two test paths.
- `bash -n` of the exact row command: PASS, exit 0.
- Exact two-positive collection using the corrected environment: PASS,
  `2 tests collected in 1.58s`.

The product contract/assertion surface was not rewritten. In particular the
guard, isolated CLI/Runtime caller, managed-scene retained-result assertions,
full v2 request/reply fields, source/origin checks, security checks, and
defaults remain the reviewed bytes.

## One central activation

Requested exactly once with:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-F-D18-supported-invocation-1045 agt-F-installed-return-1012-installed-env-one-installer-d09) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Actual service test ID:

`agt-F-D18-supported-invocation-1045-agt-F-installed-return-1012-installed-env-one-installer-d09-1023104628-20337`

Result: **FAIL, exit 1; 1 passed, 1 error in 27.91s**.

- Installer node `...[False-0]`: PASS.
- D09 node: ERROR during autouse fixture setup, before the D09 test body.
- The prior unsupported-startup refusal is gone. No Agent-tool or
  autoclassifier denial occurred.
- No second request, retry, assertion rewrite, guard change, native/browser/
  HTTP/full run, or duplicate journey was performed.

## Causal trace and classification

The retained central log is:

`ORCH/tests/agt-F-D18-supported-invocation-1045-agt-F-installed-return-1012-installed-env-one-installer-d09-1023104628-20337/log.txt`

The retained probe stderr is:

`/tmp/astrid-probe-logs/registry_discovery-kg4cixk9.stderr.log`

The Runtime receipt was:

```text
phase=registry_discovery
original_child_pid=29110
original_wait_exit_code=1
retained_set_final_census_complete=true
custody_admitted=true
failed_checks=[original_wait_exit_code]
```

The stderr traceback reaches `astrid/core/rendering/_effect_registry.py` and
fails at `_public_registry_ids()` with:

```text
ValueError: cannot verify missing rendering components: no Node executable is available for Composition's public registry API
```

The source-backed immediate cause is a second harness-environment deficiency:
the service command's isolated `PATH` is only the installed venv plus
`/usr/bin:/bin`, while D09's unchanged fixture pins the required Node
executable to `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`.
`_public_registry_ids()` accepts `ASTRID_NODE_EXECUTABLE` or `shutil.which("node")`;
the owned registry child had neither available, so its positive registry
probe exited 1. This is a harness invocation/environment classification, not
evidence against the Agent/autoclassifier and not a reason to weaken the
Runtime guard.

The one authorized central activation is exhausted, and the meaningful D09
body did not run. I therefore did not make a second service-row correction or
blind retry. A future separately authorized activation would need to provide
the documented pinned Node in the isolated service environment (for example,
the toolchain path in `PATH` or the existing explicit Node selector) while
preserving the same guard, source custody, and assertions.

## Blockers and next step

Blocked only on D09 end-to-end qualification: the installer proof is passing,
but managed-scene retained-result behavior, production isolated CLI/Runtime
execution, and live child-origin assertions remain unverified because setup
stopped at the registry probe. The next step is a new authorization for the
supported pinned-Node invocation; no current test or product change is
recommended.
