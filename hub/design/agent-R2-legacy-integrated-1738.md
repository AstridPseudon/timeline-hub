# R2/V2 integrated authenticated legacy-restore proof

## Result

**PASS** for the assigned readonly integrated proof.

The worktree was verified at:

- Agent HEAD: `079580ca46af77e0292d49dc34386b25c8391f99`
- Agent tree: `2deab1a1494fbccfce5e9235412bacb8a949c0cd`
- Integrated parent: `6531622c8f198c3efb509217e303fcad0126c47b`
- Authenticated restore parent: `d1d41c4056f509ce24af916ee20b7b683ac8f8f2`
- Runtime pin: `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`, tree
  `9b07545cac9a8bbafb16246aaa6f72050ef7cffe`
- Authentic flat archive SHA-256:
  `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`

The delta from parent `653` is exactly four files: the three reviewed
production files and the authenticated conformance test. No other current
`653` R2 storage, R1 private, runtime-lock, artifact, or unit source was
changed. `git diff --check` passed.

## Exact test commands and results

Both commands ran from the integrated Agent worktree with the same HEAD,
Runtime `d9e2a71e`, archive, and worker-owned `TMPDIR=/tmp/w-85471d3b1d`.
The focused command used durable evidence path
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-legacy-integrated-1738/evidence/focused`.

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-d9e2a71e ASTRID_AUTHENTIC_LEGACY_ARCHIVE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz ASTRID_LEGACY_RESTORE_EVIDENCE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-legacy-integrated-1738/evidence/focused TMPDIR=/tmp/w-85471d3b1d /home/user/work/venv-agent/bin/python -B -m pytest -q --tb=short -o addopts= -p no:cacheprovider -m integration --basetemp=/tmp/w-85471d3b1d/pytest-focused tests/editing_conformance/test_authenticated_legacy_restore.py
27 passed in 39.97s

env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-d9e2a71e TMPDIR=/tmp/w-85471d3b1d /home/user/work/venv-agent/bin/python -B -m pytest -q --tb=short -o addopts= -p no:cacheprovider --basetemp=/tmp/w-85471d3b1d/pytest-neighbours tests/editing_conformance/test_commit_anchor_d12.py tests/editing_conformance/test_commit_legacy_text_reference.py tests/editing_conformance/test_commit_timing_validation.py tests/editing_conformance/test_commit_v2_validation.py
80 passed in 3.34s
```

The focused 27 cases include accepted inverse, step-inverse and restore,
preview/no-write, merged disjoint movement, exact source equality, and
refusals for new/equal/modified authored writes, forged source/publication/
step, wrong digest, foreign source, ABA, source-context poisoning, changed
or removed targets, membership/order changes, owner changes, and changed
film-end flags. Refusal cases preserved the store snapshot.

Durable focused evidence contains 27 case directories and 233 files. Every
case has before and outcome records. Across all cases: one canonical source
digest (`sha256 9a11a19f18a514f380e6e3d19624d6d548561c035d1cb2bc1eed8ccb9d3605b8`),
one origin set, runtime `d9e2a71e…`, and archive SHA-256 `2915bd4a…` were
recorded. Post-run origin hashes matched the recorded pre-run hashes.

## Qualification checks

Using the author packet's dedicated typecheck environment and private cache
locations:

```text
Mypy findings: current=1912 baseline=1912
Success: no issues found in 4 source files
Ruff findings: current=2149 baseline=2149
All checks passed!
ok runtime.lock.json (matches producer manifest)
artifacts.json is current
git diff --check: exit 0
```

The exact checks were scoped Ruff/mypy, full mypy and Ruff baseline
comparisons, official producer `34eac004` vendor-lock verification, artifact
manifest verification, and `git diff --check`. Candidate blob hashes match
the reviewed packet exactly:

```text
28feda7b3831ff7ad9642e23aa6e04b19cb958242b11accab694d4b490da9542  astrid/sdk/timeline/_commit_timing_validation.py
f4272228f5c663d2f586aa5cc4f8ef2486aad4e4d38ca99e9433b6a991e53dbd  astrid/sdk/timeline/commit.py
dc3305e24bcad677c6573c5bdd8557e2a60d72dd9eedd03c307f8c8a78bf8fbc  astrid/sdk/timeline/validation.py
86e47fc83b476a4faa3f00b14c0413c6c1127cac4bfa67d7e2a9847428f9df41  tests/editing_conformance/test_authenticated_legacy_restore.py
```

Protected current-`653` hashes for `inverse.py`, `_step_undo.py`,
`_root_inverse.py`, `_commit_patch.py`, `runtime.lock.json`, and
`artifacts.json` matched exactly.

## Limits and decisions

No source changes, deletions, Git writes, environment provisioning, pin or
dependency changes, integration-worktree writes, daemon/merge-queue actions,
or product-test edits were made. No original FOUR, public redo, full suite,
P1/P4, native14, browser, socket, or other prohibited suite was run.

An initial baseline-mypy attempt with the general `venv-agent` reported the
known environment-only YAML-stub/NumPy diagnostics and stopped before project
findings. The author command packet specifies `venv-agent-typecheck-v2`;
that exact baseline environment was then used and passed 1912/1912. No
packages were installed or modified.

Recommended next step: manager-controlled continuation of the remaining
integration gates, using this PASS as the R2/V2 authenticated legacy-restore
proof only.

