# F-D22 profile-fixtures-1454 handoff

Status: **qualified with a test-support correction; six failures preserved and classified**.

Base Agent: `58316fd6e0ce8a1fb3b2b3826ec71906d29080de`.

Profile: Runtime `3b926efab2eed122d374540baee297d4cdcec62a`, Node `v20.19.4`,
Composition `0.0.14`, archive `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

## Correction

Updated only existing profile-related test support:

1. backend fixture package assertion 0.0.13 → 0.0.14;
2. layer-tail duration module old chunk `SE4TPVLW` → current archive chunk
   `A6LVBEHN`;
3. typecheck mapping parser ignores fixed Composition imports and validates
   the current public registry when no hashed host imports exist;
4. AM plate host fixture uses the locked 0.0.14 archive SHA
   `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234` and
   80-file body.

Product source, contract, lock, archive, generated files, pins, dependencies,
and environment were untouched.

## Exact qualification

Command prefix:

```text
env PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/bin:/bin /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider
```

It was followed by the 40 explicit inventory nodes: 10 backend, 12
layer-tail, 3 typecheck-mapping, 13 AM-plate, and the 2 compile vectors.

Result: **34 passed, 6 failed, 1:50.75**.

Preserved failures and owners:

- backend raw-manifest node: sanitized child cannot import `runtime_protocol`;
  D18 invocation/child-environment owner;
- three `public12_outer_geometry_gap_does_not_erase_original_positive` nodes:
  current 0.0.14 source returns `GAP` for evaluated crop/entrance geometry;
  Composition/profile owner;
- fade-in and fade-out compile vectors: projection has no
  `audio.render_source`; trusted-host prepared-envelope owner.

The original SSR/painted-backing positives and negative controls pass under
the current profile. Assertions were not weakened, skipped, or xfailed.

## Checks

`git diff --check`, changed-test `compileall`, and the repository Ruff baseline
passed. Ruff baseline stayed exactly `2149`. Mypy baseline could not execute
in the shared venv because `types-PyYAML` is absent and one NumPy stub requires
Python 3.12+; expected baseline is `1912`. No dependencies were installed.

Changed test body hashes are recorded in `report.md`; lock/archive hashes are
unchanged and equal to the profile values.
