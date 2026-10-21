# normal014 source/setup custody review

## Verdict

**APPROVE within the requested source/setup scope.** The final95 base-Python
setup selects the exact frozen Agent and Runtime sources, and the helper refuses
arbitrary source/repository overrides. Synthetic ancestry/tree/pin logic and
the child-exit capture remain outside this review; the synthetic logic was
already approved by review0202.

## Frozen facts and helper hashes

- Agent final95: commit `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.
- Runtime/producer final95: commit
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- Stale Runtime commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a` has a
  different tree (`7ab412cc4bcbe517efcfa806e092336390312e18`).
- `design/normal014-source-common.sh`:
  `c76c48fa5f73b72ada6ba8fa857f229778e2ed6948568e77000bf4c1a8490270`.
- `design/normal014-app-central.sh` (reported for provenance only; its exit
  capture is not re-reviewed here):
  `8f70ed7adafa42d90b3053f5972bd763a653ae690c1b2dfda352e3704615686e`.
- `design/normal014-parent-media-central.sh`:
  `1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd`.

The source helper now sets `APP_BASE_RUNTIME_SHA` to final95
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, not stale `2c4ac180...`.
`prepare_sources` checks out the exact Agent, Runtime, and producer commits and
trees, verifies the producer ancestry, and verifies the artifact/schema bytes.

## Focused probes

All probes were read-only, used temporary private checkouts, and performed no
browser, localhost/socket, full-suite, or package-install work.

- `sh -n .../design/normal014-source-common.sh` — PASS.
- With `NORMAL014_PROFILE=final95 NORMAL014_USE_BASE_PYTHON=1` and
  `NORMAL014_PYTHON_BASE=/home/user/work/venv-app2-native/bin/python`, the
  helper prepared the exact sources and selected that exact base interpreter.
  `verify_python_imports_and_collection` passed, including the required
  `test_native_parent_clip_swap_route_replaces_parent_media` collection. The
  artifact probe reported 76 verified artifacts and schema digest
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- A direct module-path probe passed: Agent modules
  `astrid.core.gateway`, `astrid.sdk.timeline.capture`, and
  `astrid_runtime_client` resolved below the prepared Agent checkout; Runtime
  `runtime_protocol.service` resolved below the prepared Runtime checkout.
- With caller `PYTHONPATH`, `ASTRID_CHECKOUT`, and
  `ASTRID_RUNTIME_CHECKOUT` set to foreign paths, the same import/collection
  guard still passed and printed `CALLER_SOURCE_ENV_OVERRIDE=IGNORED`.
- `NORMAL014_APP_SOURCE=arbitrary` was refused with status 2.
- `AGENT_REPO=$PWD` followed by `prepare_sources` was refused with status 128
  (`reference is not a tree` for the frozen Agent SHA).
- Passing the App worktree as the Agent import root under `sh -eu` was refused
  with status 1 (`ModuleNotFoundError: No module named 'astrid'`). Passing it
  as the Runtime import root was likewise refused with status 1
  (`ModuleNotFoundError: No module named 'runtime_protocol'`).

These probes establish both sides of the source/setup contract: the base
interpreter is only the execution environment, while the helper supplies the
exact frozen source roots and refuses roots that do not contain the required
imports. No smallest correction is required.

## 3198 evidence boundary

The planted-negative result `...1021021120-3198` remains valid and was not
rerun. Its retained central textual log records `status=fail`, `exit=1`, one
real Playwright failure, and `normal014 Playwright child exit: 1`. The trace and
error-context files named by that log were removed by cleanup; this report does
not claim they were retained.

## Not run / next steps

No code edits, browser/socket run, full suite, install, or broad retest was
performed. The next step is to carry this source/setup approval alongside the
already-approved exit-capture and synthetic-source reviews; no repeated browser
negative is needed.
