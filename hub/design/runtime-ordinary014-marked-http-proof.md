# Runtime ordinary014 marked HTTP proof

## Result

QUALIFIED. The exact completed ordinary014 current-server candidate passed the
three required positive cases: the disjoint intervening-edit rebase, the
verified generic image swap, and the public HTTP route. No Runtime product,
schema, or test file was changed by this worker.

## Immutable identities and source provenance

- Runtime HEAD: `202074110717146fc7f08af2306a8dd7f695b0b1`
- Runtime tree: `ee39286bd0eb27d4075074cc4785d6d15e33f243`
- Runtime test blob (`tests/test_timeline_clip_replacement.py`):
  `183f14dbe64466c9a8c7aec5b34850da9272f107`
- Ordinary014 artifact: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`
- Artifact manifest: `sha256:ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`
- Artifact shape: 75 paths, 55 definitions, 29 command operations.
- Frozen Agent source: commit
  `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`, tree
  `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`.
- Agent timeline commit/provider blob:
  `6dbc3c5e25b6c58d234eab25e531a42a3ebd722a`.
- Agent raw timeline schema: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

The test imported Agent from the restored private/fallback source at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source`.
The source-repair verification reported 443 extracted files with zero missing
or mismatched blobs against Agent 310. The imported module paths were:

```text
astrid.__file__ = .../agent-final-source/astrid/__init__.py
astrid.sdk.timeline.commit.__file__ = .../agent-final-source/astrid/sdk/timeline/commit.py
runtime_protocol.__file__ = .../rt-m2-ordinary014-marked-http-proof/runtime_protocol/__init__.py
```

`/home/user/work/agent` did not contain the native timeline module, so the
test fallback selected the verified frozen source; no current-Agent module was
used. The HTTP service command still reports its configured environment as
`ASTRID_CHECKOUT=/home/user/work/agent`, but the test's source-selection guard
resolved the actual native imports to the frozen fallback above.

## Evidence

Local, offline targeted positives:

```text
ASTRID_CHECKOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source PYTHONDONTWRITEBYTECODE=1 \
/home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
tests/test_timeline_clip_replacement.py::test_native_clip_swap_rebases_after_disjoint_intervening_edit \
tests/test_timeline_clip_replacement.py::test_native_generic_visual_media_accepts_verified_image_swap
```

Result: `2 passed in 2.36s`.

Socket-backed HTTP proof, submitted through the explicit marked integration
service with the required single selector:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  rt-m2-ordinary014-marked-http-proof marked-integration \
  --files "tests/test_timeline_clip_replacement.py::test_native_clip_swap_public_http_route")
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result: `1 passed in 2.92s`, exit 0. The service executed:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent \
/home/user/work/venv-agent/bin/python -m pytest -q -n 3 -m integration \
tests/test_timeline_clip_replacement.py::test_native_clip_swap_public_http_route
```

Request record:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-ordinary014-marked-http-proof-marked-integration-1020162108-7582/request`

Snapshot record:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-ordinary014-marked-http-proof-marked-integration-1020162108-7582/snap`

The snapshot key was `e182884e1a89689ac1ac0ad5e55f6a94`; its tree was
`ee39286bd0eb27d4075074cc4785d6d15e33f243`.

## Limits and decisions

- The earlier default targeted selector was not treated as evidence:
  `rt-m2-ordinary014-current-test-carry targeted --files
  tests/test_timeline_clip_replacement.py::test_native_clip_swap_public_http_route`
  exited 5 with `1 deselected`, because default addopts exclude integration.
- No full suite was requested or run.
- No schema, generated contract, product logic, or test mutation was made.
- Native-pair and App same-cohort qualification remain separate, as directed.
- No release, pin, current-tuple, or branch/ref operation was performed.
