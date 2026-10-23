# Agent F installed final review

## Verdict

Source review: **PASS**.

Durable installed-environment custody/origin review: **PASS**.

Central behavior run: **FAIL / STOPPED by the existing Runtime safety guard**.
The installer representative passed, but the D09 node failed during fixture
setup before its test body ran. The task explicitly requires stopping and
reporting an actual safety denial, so there was no retry or second service run.

This distinguishes a valid source and installed-environment qualification from
an unqualified end-to-end D09 behavior result.

## Reviewed source

- Worktree commit: `9564261cf0e1b62f0ea45f01f5bc75a7a3ecad61`, tree
  `9618a0928a361eca8f172e0bf56a1ae5d0e472fa`.
- Parent/source baseline: Agent `ef851b22c506245441b9a630c093b3460e39cbdc`,
  tree `b11eee891208d11e23c55950f8954ddd3377d5a8`.
- Runtime source archive was independently extracted from Runtime
  `1365e4b17b31c4a7093d5943674637067fd2bab4`, tree
  `6c69c3dc47822fffbaf27cd63815d2895155ffaa`.
- The durable `source/agent` extract matched all 3,400 tracked files from
  Agent `ef851`; `source/runtime` matched all 467 tracked files from Runtime
  `1365`. Both extracted source sets were symlink-free.
- The only product-tree diff is the authorized two-binding seam in
  `tests/integrations/test_d09_managed_scene_only.py`: existing defaults remain
  `/home/user/work/runtime` and
  `/home/user/work/venv-agent/lib/python3.13/site-packages` when the optional
  variables are absent; supplied values are preserved when present. No
  sanitation, GIT filtering, public13 package assertion, worker validation,
  security-profile, or other original assertion was removed or weakened.
- The Agent lock remains byte-identical to the reviewed baseline, including
  the frozen producer source `34eac0041b0891e9011966b39bcbd26053fde5bc`.
  The existing Composition artifact reference and schema/vendor material were
  not changed.

## Durable installed environment

Root: `/home/user/work/venv-agent-child-f1012-installed`.

Independent checks passed:

- Wheel SHA-256:
  - `astrid-0.1.0-py3-none-any.whl`:
    `fcccab4dc881faa4eead1f971fc655dc96ebfac9efac199015794d7b644007e3`
  - `astrid_runtime-0.1.0-py3-none-any.whl`:
    `aac07960e997c8881a594d6d9a3e18eccfef6828dc15cab9fc0f3fd25f941c49`
  - `astrid_runtime_client-0.2.14-py3-none-any.whl`:
    `f0cb9f222c5d2697eb8c1d912cccfce30fa058530a1471b8441b54b4546497a4`
- All 164 dependency identities matched the immutable inventory; inventory
  digest: `478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`.
- All 182 private RECORD files and 26,679 RECORD rows passed path/hash checks;
  the recorded RECORD-file hashes were unchanged.
- The four-field `profile/astrid.json` shape passed. Runtime checkout, source
  checkout, and runtime environment are absolute, existing, private,
  symlink-free paths under the durable root.
- Same-process installed imports resolved privately for `astrid`,
  `astrid_runtime_client`, `runtime_protocol`, `astrid_runtime`,
  `banodoco_timeline_schema`, NumPy, Pillow, OpenCV, and PyYAML. A separate
  `python -I -B` child independently resolved the required Agent/Runtime
  namespaces to the same private site-packages root.
- The outer reviewed-process guard resolved Agent and client from the current
  worktree and `runtime_protocol` from the installed site-packages root, as
  required by the normal route.
- Disk check: `15,433,682,944` bytes available on both `/home/user/work` and
  `/tmp` (above the 15 GB floor); durable root size `955,098,806` bytes.

## Source/test evidence before activation

- `bash -n` on the durable proposed command: **PASS**.
- Exact two-node `pytest --collect-only`: **PASS**, exactly 2 collected:
  `test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[False-0]`
  and `test_public_checkout_check_uses_retained_managed_scene_result`.
- Targeted installer/security lane: **17 passed, 69 deselected** for
  `tests/test_installer_service_env.py` and selected installed-profile
  `tests/sdk/test_host_bootstrap_source_identity.py` tests.
- `make PY=/home/user/work/venv-agent-child-s2/bin/python ruff`: **PASS**,
  `2149/2149`.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/agt-F-installed-final-review-1021-mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline`:
  **PASS**, `1912/1912`.
- The durable venv's bundled Ruff reports 2152 for the same source despite the
  same nominal version; the frozen qualification tool reports the required
  2149. No source or baseline was changed for this toolchain discrepancy.

## Authorized central run

Exactly one row was added to the existing orchestration
`tests/suites.conf`, using the durable proposed command and exactly the two
original nodes. The SHA-256 of all bytes outside that inserted row remained:
`df3d20c8204ff4b9b41bb381014119132b50d7dbd2fc4a47ae4ba9df7db751a8`.

Test ID:
`agt-F-installed-final-review-1021-agt-F-installed-return-1012-installed-env-one-installer-d09-1023102732-26224`

Central result: **exit 1; 1 passed, 1 error in 21.24s**.

- Installer node: **PASS**.
- D09 node: **ERROR during autouse fixture setup**, at
  `tests/integrations/test_d09_managed_scene_only.py:128`, before the D09 test
  body. The reviewed Runtime source rejects the command's
  `PYTHONNOUSERSITE=1` in `_UNSUPPORTED_PYTHON_STARTUP` from
  `astrid/core/rendering/remotion_runtime.py:209-231`, raising:
  `RemotionValidationError: runtime validation refuses unsupported
  loader/interpreter overrides`.
- This is an operational command/environment safety denial, not evidence that
  the two-line D09 seam changed behavior. It also means D09 managed-scene
  behavior, retained-result assertions, and the live child-origin assertion
  remain unverified by this run.
- No second request was submitted, no command was weakened after the denial,
  and no daemons or shared worktrees were modified.

## Recommended next step

Have the orchestrator issue a new, separately authorized activation after
removing or otherwise resolving the rejected `PYTHONNOUSERSITE=1` binding in
the proposed command. The current one-run authorization is exhausted and this
worker must not retry it. The existing named row should be treated as a failed
activation record, not as a passing D09 qualification.

