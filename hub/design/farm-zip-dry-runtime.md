# F-zip-dry rehearsal: runtime (tf-zip-runtime)

**Status: BLOCKED at step 3.** Steps 1, 2 and the step-4 file-level overlap check pass. Step 3 (fresh clone checked out at BASE, then apply) was refused by the sandbox permission check on `git checkout --detach`. Per the brief, I stopped and did not route around it. Steps 3–5 are not run.

## Step 1: record integration, base, ancestry: PASS
- Integration `tl/integration` = `cfa0af0d476e6954df041c08d7ef378fd6782932`, tree `3675f446c82c455ef5635ae725409eb6076a4f83`.
- Hub ref `hub/timeline/runtime/tl/integration` = same SHA, so the two agree.
- BASE `a98fbc2f9544a8be14281e32afde8aafa098f5f7`, tree `16c923ce3d96ffd67d242b4ad9a3e4893ff48a38`.
- `git merge-base --is-ancestor a98fbc2f9 cfa0af0d4` → ancestor: yes.

## Step 2: squashed patch base..integration: PASS
- Command: `git diff --binary a98fbc2f9 tl/integration`, with the patch written to the session scratchpad, `zip/zip.patch`.
- Size: 4,632,068 bytes (about 4.6 MB).
- Files: 245 (154 added, 91 modified; 72,073 insertions, 2,913 deletions).
- Test vs product: 173 paths are under `tests/`, 72 are product (`--name-only` list in `zip/files.txt`).

## Step 3: fresh clone at BASE, `git apply --check` and apply: NOT RUN (refused)
- Fresh clone: a repo was initialised in `orch/workers/tf-zip-runtime/zipfresh` and fetched `refs/heads/main` from `https://github.com/banodoco/banodoco-workspace-runtime`. The fetched tip was `f23d1e43f6b206d4a3b3f9058c47a1562eb6bfc6`.
- `git checkout --detach a98fbc2f9` was denied by the permission check (exact refusal: "Permission to use Bash with command ... checkout -q --detach a98fbc2f9... has been denied").
- Consequence: no applied tree exists, so the "applied tree == integration tree" equality is unverified.

## Step 4: apply to the live upstream tip: PARTIAL (file-level only)
- Live `git ls-remote https://github.com/banodoco/banodoco-workspace-runtime refs/heads/main` = `f23d1e43f6b206d4a3b3f9058c47a1562eb6bfc6`. It equals the fetched tip.
- **Drift is larger than the brief lists.** The brief names only `6162e0e33` (tests only, deferred). Upstream base..tip has 3 commits:
  - `b70c323` skip registry: `tests/lanes.py`, `tests/test_skip_registry.py`, `tests/test_skip_guard.py`. Tests only.
  - `6162e0e` skip guard test: `tests/test_skip_guard.py`. Tests only.
  - `f23d1e4` remove dead pictureTracks handling: `runtime_protocol/visual_seam.py` (**product code**), `docs/visual-seam-policy.md`, `tests/test_visual_seam_admission.py`, `tests/test_canonical_render_admission.py`.
- **Overlap with the integration patch (file level, 5 files; the rest of upstream drift does not overlap):**
  - `runtime_protocol/visual_seam.py`: integration +/- 23 lines, and `f23d1e4` changes the same file. **Likely conflict; this is the one product-code overlap.**
  - `tests/lanes.py`: integration 172 lines changed; `b70c323` also changes it. Likely conflict.
  - `tests/test_skip_guard.py`: integration +32; `b70c323` and `6162e0e` both change it. Likely conflict.
  - `tests/test_skip_registry.py`: upstream only in the base..tip diff, so it is not an integration overlap. (Listed above as drift.)
  - `tests/test_visual_seam_admission.py` and `tests/test_canonical_render_admission.py`: integration 154 and 143 lines; `f23d1e4` also changes them. Likely conflicts.
- **Not verified:** the actual 3-way apply and hunk-level conflicts. These need the step-3 checkout.
- Decision for the orchestrator: the upstream rule says defer, but `f23d1e4` touches product code (`visual_seam.py`), so it may not be test-only drift. It needs an orchestrator call, or a U-task at the freeze.

## Step 5: fast checks on the applied tree: NOT RUN
- Reason 1: no applied tree (step 3 refused).
- Reason 2: runtime declares no lint or typecheck config (no ruff/mypy/flake8 in `pyproject.toml`, `setup.py` or `.github/workflows/ci.yml`). CI runs `python -m pytest -q -n 2`.
- Reason 3: there is no `venv-runtime` under `/home/user/work/`. The only Python venvs present are agent venvs, and using them returned an approval prompt. Running `ruff` (`--select E9,F`) against the worktree also returned an approval prompt. No install was attempted.
- The worktree `tl/tf-zip-runtime` is clean at `cfa0af0d4`, the same SHA as integration, so any check there is on the integration tree, not the applied fresh tree.

## Commands run (exact)
- `git -C /home/user/work/runtime diff --binary a98fbc2f9 tl/integration > zip/zip.patch`, then `wc -c`, `grep -c '^diff --git'`, and `git diff --name-status | cut -c1 | sort | uniq -c`. Result: 245 files, 154 A, 91 M.
- `git ls-remote https://github.com/banodoco/banodoco-workspace-runtime refs/heads/main` → `f23d1e43f6b206d4a3b3f9058c47a1562eb6bfc6`.
- `git -C .../zipfresh fetch -q <upstream> refs/heads/main` → fetched; `merge-base --is-ancestor a98fbc2f9 f23d1e4` → yes.
- `git -C .../zipfresh checkout -q --detach a98fbc2f9` → **denied** (permission check). Not retried.
- `git -C .../zipfresh diff --name-only a98fbc2f9 f23d1e4` and `log --name-status` → 7 files, listed above.

## Smallest cause of the block
A permission denial of `git checkout --detach` in the scratch clone. Unblock by approving that checkout (or running it for me). Step 5 also needs a runtime venv (`venv-runtime`), which the dispatcher should provision, or an approval for `ruff` and the Python imports.

## Recommended next steps
1. Orchestrator: decide whether `f23d1e4` and `b70c323` are in scope now (they are not in the brief's drift list), given the `visual_seam.py` overlap.
2. Re-run the rehearsal with checkout approved, then apply `--3way` to `f23d1e4` and record the conflicts.
3. Provision `venv-runtime` (or confirm ruff/mypy access) for step 5. Otherwise state "no lint config; collect-only only".
