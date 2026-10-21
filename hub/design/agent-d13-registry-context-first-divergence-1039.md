# D13 registry context-first divergence

## Verdict

This is a real Agent registry source-origin/projection defect, not a fixture-only or profile-content mismatch. No product or test change was made. Native, render, HTTP, browser, install, profile rebuild, and full-suite runs were not repeated.

The retained 1034 run used Agent commit `fc8b54e97cac98576e3ff005d2c1b5d77ac09682`, tree `6f426ffc8342371799cdff578f50758a5ef2cae5`; Runtime b92 commit `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree `6abc2f117391de8e7e35c0283f575a002199894d`; and the approved 0908/f4ed installed profile. Its first product-adjacent failure was `RemotionValidationError: renderer/generator sharing contexts expect different registry contents`, before host/task admission, outbox, or render.

Retained evidence:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-d13-complete-diagnosis-one-proof-1034-d13-installed-f4ed-current-one-integration-1021103233-17006/` and `/tmp/d13-IMCTEZ/native.log`.

## Exact contexts

After `_registry_context(..., generator=False)` and project binding, the retained host context was:

```json
{
  "ASTRID_REMOTION_PROJECT_DIR": "/home/user/work/runtimes/agent-remotion-f4ed-0013",
  "ASTRID_TIMELINE_SCHEMA_PYTHONPATH": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/lib/python3.13/site-packages",
  "HOME": "/tmp/d13-IMCTEZ/home",
  "LANG": "C.UTF-8",
  "LC_ALL": "C.UTF-8",
  "PATH": "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/bin:/usr/bin:/bin",
  "TMPDIR": "/tmp/d13-IMCTEZ/tmp"
}
```

Host context SHA-256: `0b44879609bd570129e4b989b119caecd76506f82fb7a0f40580b7df3eb32077`.

The first native-worker context was the same object plus:

```json
{
  "ASTRID_PACKS_PATH": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/lib/python3.13/site-packages/astrid/packs/rendering",
  "PYTHONPATH": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/lib/python3.13/site-packages/astrid/packs/rendering"
}
```

Native context SHA-256: `db24bc769a2cc7a612b6276b36c8e49785fa74915a4104b0534db1d078b6623f`. The command-worker context was also distinct: `c1f1c18a0ae4a7527ad20ac03d8633c95bba938fdf3b2888d462e5d9b7535407`.

The first differing context field is `ASTRID_PACKS_PATH`: absent for the host, versus the selected installed rendering root for native. The next difference is `PYTHONPATH`, naming that same installed root.

## Exact registries

```text
host:
  animations = 02326f12177879eb5905f9d9b6d476b2de185928ddeeeeb2321a68ebffb47ad6
  effects = 127e5653e0c66993726f8334b9f4ac122d24cdfbaa9e70cdaa142189afcf2bbe
  transitions = c46d6bbd88712e775812867ec1cbe6de67473664775266c5a0b9317344ceb989
  registry hash = 32b312f5ea7b2a67717a79ae71b539510590e9010e2ec7f77c8bce1edbabbfc6
  registry object SHA-256 = 344651348f4abbf592e7ce83132be79acb728c3fbd09338894f7c94bf534d975

native:
  animations = 02326f12177879eb5905f9d9b6d476b2de185928ddeeeeb2321a68ebffb47ad6
  effects = acc610b80abcdaa2f90070f45da237ff162e55ed9bc14ee37e6c32b7be478eb3
  transitions = c46d6bbd88712e775812867ec1cbe6de67473664775266c5a0b9317344ceb989
  registry hash = a376c389ea7fed1c233aa874b84df0db608991ea4cc721f3dbd962968f05e4a3
  registry object SHA-256 = 678c986c998f4d493441ec547b2e695942561863efe782929c7654707174d1bc
```

The first differing registry field is `content_hashes.effects`; animations, transitions, and version match. Native discovery also includes the installed rendering root in its roots in addition to checkout roots, while host discovery does not.

## Cause and authority findings

The selected authority is the private interpreter `.../private-profile-f4edcb4b/venv/bin/python` and its noneditable site-packages tree. Relevant checkout and installed file hashes are identical, so this is not profile byte drift:

```text
remotion_runtime.py  fe36a766eba34d2052c55fdcc8b4ed8ad2b3ffa27fc5dd346c6693d9ee424f0f
discovery.py         076bd6ba127b9c49c0c4432fef806d20f7509e6ef2200e4612c38e3c816ab52f
source_setup.py      9ba00f4044e558481525e0f17e6d01fe3494f168f2207a0b30d2cf7dd6a3e27e
element/registry.py  be684e1fe871eb8f8e87de61f59837e79402126ec63884e723cb4e6c173df823
remotion/run.py      bb02817a945a5fb29fd3f1e91fb9d1defb6af9f3189f9cbe2063121e991a2cb0
```

Each hash was equal between current checkout and selected installed copy. Nevertheless both retained probes reported checkout origins:

```text
astrid_origin    = /home/user/work/wt/agt-m2-d13-registry-context-first-divergence-1039/astrid/__init__.py
runtime_origin   = /home/user/work/wt/agt-m2-d13-registry-context-first-divergence-1039/astrid/core/rendering/remotion_runtime.py
generator_origin = /home/user/work/wt/agt-m2-d13-registry-context-first-divergence-1039/scripts/gen_effect_registry.py
```

Live callers:

- `astrid/sdk/host_bootstrap.py:776` (`_host_render_environment`) removes `ASTRID_PACKS_PATH` and, for installed, removes `PYTHONPATH`.
- `astrid/sdk/host_bootstrap.py:804` (`_prepare_render_validation`) passes the host environment plus `_launch_worker_probe_environments` results to validation.
- `astrid/core/execution/generic_host.py:1715` and `:1795` (`_launch_worker_probe_environments`) add `ASTRID_PACKS_PATH=<pack_roots>` and pack-root `PYTHONPATH` to native.
- `astrid/core/rendering/remotion_runtime.py:674` (`_registry_probe`) inserts `REPO_ROOT` into `sys.path` and chooses the checkout renderer cwd; `:503` (`_registry_observation`) calls `load_checkout_script('gen_effect_registry')`; `:708` (`_settle_registries`) compares the resulting states.

The installed interpreter is selected, but registry discovery uses the provenance checkout as import/generator authority. This is the real source-origin defect. The differing explicit pack path is the first context projection defect; it exposes a second discovery corpus and changes the effects registry.

## Narrow owner fix proposal

Agent owns the fix. In the existing registry probe path, make installed-profile registry discovery import `astrid`, `remotion_runtime`, and the generator only from the selected interpreter's installed package tree. Do not insert `REPO_ROOT`, use `ASTRID_RUNTIME_CHECKOUT`, or fall back to checkout `scripts/gen_effect_registry.py`; fail closed if the installed generator is unavailable. Preserve the current source-root/origin checks and sharing guard.

Then make the existing host/native projection select one normal installed discovery context: an installed rendering root already covered by normal discovery must not be added as a second explicit root, or the same explicit root must be used for host and workers. This is a narrow change to `_launch_worker_probe_environments`/registry-context normalization, with no new authority, pin, schema, profile, or security relaxation.

After that fix, add one compact red-to-green context test asserting that host and native expected contexts and registry observations settle to the same state while retaining the existing source-origin guard. No such test is added here: the current source-origin defect makes a fixture-only correction incorrect.

## Remaining preparation prerequisites

1. Land and independently review the narrow installed-origin and canonical context fix; retain f4ed source-root and registry-sharing guards.
2. Rebuild/reselect the approved 0908 installed profile from fixed Agent source, preserving the selected installed interpreter and profile bindings.
3. Revalidate the exact Agent/Runtime/client/bindings tuple (Agent f4ed, Runtime b92, approved 95/C13 bindings) and installed origin closure.
4. Run the compact context test and relevant targeted Agent tests; central qualification may then recheck startup/preflight and registry settling.
5. Obtain separate authorization for the next actual. Host/task admission, outbox/publication, render/body decode, and undo remain unexecuted in 1034.

## Checks

```text
24 passed in 1.94s
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/.../workers/agt-m2-d13-registry-context-first-divergence-1039/pytest-tmp tests/core/rendering/test_remotion_registry_context_key.py tests/core/rendering/test_remotion_registry_git_env.py tests/core/rendering/test_registry_matrix.py
```

Read-only registry observations and SHA comparisons reproduced both objects above. No full suite, native rerun, render, launcher, HTTP/browser, install, profile rebuild, or shared dependency write was performed.
