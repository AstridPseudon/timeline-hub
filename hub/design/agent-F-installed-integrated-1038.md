# F-installed integrated proof — fixture and durable environment

## Verdict

**Integrated component: PASS.** The actual reviewed Agent tree has the
default-preserving fixture seam, and the durable installed environment remains
present and unchanged after this worker's test process exited.

**D09 behavior: NOT DONE / remains STOPPED.** I did not rerun D09. The prior
authorized activation stopped before the D09 body on the existing Runtime
safety refusal of `PYTHONNOUSERSITE=1`; this report does not convert that
STOPPED result into a D09 pass.

## Source and fixture identity

- Current worktree commit: `7abfb8d69f625d0aada79346d5806f5f9525ed8c`.
- Current tree: `9618a0928a361eca8f172e0bf56a1ae5d0e472fa`.
- Reviewed source commit: `9564261cf0e1b62f0ea45f01f5bc75a7a3ecad61`, same
  tree `9618a092…`.
- The actual fixture-seam blob
  `tests/integrations/test_d09_managed_scene_only.py` is
  `dfe8ed9a4d0fc8870b76079889b1cb9c9b3bd9d4` in both trees.
- The only diff from Agent `ef851b22c506245441b9a630c093b3460e39cbdc` is
  the reviewed 8-line insertion/2-line deletion in that fixture. The normal
  defaults remain `/home/user/work/runtime` and
  `/home/user/work/venv-agent/lib/python3.13/site-packages` when optional
  bindings are absent; supplied bindings are preserved. `git diff --check`
  passes.
- Durable extracted source identity is exact and symlink-free:
  Agent `ef851…`: 3,400 tracked files, 0 missing, 0 mismatched;
  Runtime `1365e4b17b31c4a7093d5943674637067fd2bab4`: 467 tracked files,
  0 missing, 0 mismatched.

## Durable installed environment

Root `/home/user/work/venv-agent-child-f1012-installed` still exists after
the worker test process. The profile points both checkout fields at the
private site-packages directory and the environment field at the private
`venv`. The standard virtualenv `venv/lib64 -> lib` link is the only durable
root symlink; both extracted source trees are symlink-free.

Read-only custody checks passed:

- Agent wheel SHA-256:
  `fcccab4dc881faa4eead1f971fc655dc96ebfac9efac199015794d7b644007e3`.
- Runtime wheel SHA-256:
  `aac07960e997c8881a594d6d9a3e18eccfef6828dc15cab9fc0f3fd25f941c49`.
- Runtime client wheel SHA-256:
  `f0cb9f222c5d2697eb8c1d912cccfce30fa058530a1471b8441b54b4546497a4`.
- The reviewed 164-pin inventory digest remains
  `478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`.
- All 182 recorded RECORD-file SHA-256 values match the durable pre-exit
  manifest; the corresponding 26,679 RECORD rows are unchanged.
- A separate `python -I -B` child resolves `astrid`,
  `astrid_runtime_client`, `runtime_protocol`, `astrid_runtime`,
  `banodoco_timeline_schema`, NumPy, Pillow, OpenCV, and PyYAML from the
  private site-packages root.

## Authorized targeted test

Exact selection recovered from the independent 1021 log/report (no D09):

```text
env -i HOME=<private-temp-home> LANG=C.UTF-8 LC_ALL=C.UTF-8 \
  PYTHONPATH=$PWD \
  PATH=/home/user/work/venv-agent-child-f1012-installed/venv/bin:/usr/bin:/bin \
  PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/venv-agent-child-f1012-installed/venv/lib/python3.13/site-packages \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-f1012-installed/venv/lib/python3.13/site-packages \
  /home/user/work/venv-agent-child-f1012-installed/venv/bin/python -P -m pytest -q \
  -o addopts= -p no:cacheprovider \
  tests/test_installer_service_env.py \
  tests/sdk/test_host_bootstrap_source_identity.py \
  -k 'installed_profile or service_wrapper or registration_preserves_settings or changed_or_cleared_service_settings or legacy_services_restart or foreground_service_uses_its_own_log or doctor_does_not_report_a_stale_bundle or doctor_returns_a_new_bundle_for_an_unhealthy_runtime'
```

Result: **17 passed, 69 deselected in 1.48s**.

The previously qualified Ruff `2149/2149` and type baseline `1912/1912`
were reused as instructed; no full, browser, HTTP, native, or D09 rerun was
performed.

## Blocker and next step

The integrated fixture/durable-environment component is qualified. D09's
managed-scene behavior, retained-result assertions, and live child-origin
assertion remain unverified because the existing Runtime startup safety guard
refused the prior command before the test body. A separately authorized future
activation must resolve that refusal; this worker made no command, guard,
environment, source, test, service, pin, or shared-dependency changes.
