# D118a parent track labels2 evidence

- The authorized file remained byte-for-byte unchanged at SHA-256 `1e3517c511a1e6f1090d9d15bf212553762de83cfae40ad330ac77749a0edb91`.
- Exact own2 run used clean Runtime checkout `/home/user/work/wt/rt-pin-42aad0e9`, commit `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`, with the genuine `real_runtime` fixture and production caller.
- Both exact nodes errored during the shared `m1.film` fixture baseline commit, before either parent-label test body ran. The boundary is `astrid/sdk/timeline/validation.py:650`, with `candidate.timing: legacy word anchor is missing`.
- The causal setup is in the shared `tests/editing_conformance/test_commit_runtime_m1.py::film` fixture, which is outside this task's allowed file. No target-local setup/caller gap was available to repair without copying or changing shared fixture behavior; no speculative metadata, guard, skip, xfail, or product change was made.
- Static checks: Ruff pass; mypy `--follow-imports=skip` pass; `PYTHONPYCACHEPREFIX=/tmp/w-039bb19e06/app-D118a-parent-label2-1206-pycache python -m py_compile ...` pass; `git diff --check` pass.
- The target file is absent at frozen `08e6b905` (`git cat-file -e` returned the expected missing-path error), and its authored assertion/call counts remain 30/89.
