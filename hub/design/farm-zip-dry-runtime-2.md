# F-zip-dry rehearsal 2: runtime (tf-zip2-runtime)

**Status: PARTIAL. Steps 1, 2, 3 (py_compile half) and 4 PASS. Step 3's smoke tests are REFUSED (sandbox denied `pip install`), so no tests were run.** Redo of `design/farm-zip-dry-runtime.md` against the current hub head. Nothing pushed, committed or edited in the product repo.

## Step 1: integration, base, ancestry: PASS
- Integration `tl/integration` = `9ce4242bc01f100bab9efc51032a73985cefb2b2`, tree `92ab1f5f739ffdfedf7b25fbd2a7b46ae42c5d1a`.
- Hub ref `hub/timeline/runtime/tl/integration` = same SHA.
- Moved since the earlier report: that report used `cfa0af0d4` (tree `3675f446c`).
- BASE `a98fbc2f9544a8be14281e32afde8aafa098f5f7`, tree `16c923ce3d96ffd67d242b4ad9a3e4893ff48a38`.
- `git merge-base --is-ancestor a98fbc2f9 9ce4242bc` → ancestor: yes.

Commands: `git -C /home/user/work/runtime rev-parse tl/integration hub/timeline/runtime/tl/integration`, `rev-parse 'tl/integration^{tree}' 'a98fbc2f9^{tree}'`, `merge-base --is-ancestor`.

## Step 2: squashed patch base..integration, then fresh clone apply: PASS
- Patch: `git diff --binary a98fbc2f9 tl/integration`. **5,209,625 bytes** (earlier run was 4,632,068 bytes at `cfa0af0d4`).
- Files: **246** (155 added, 91 modified; `git diff --shortstat`: 246 files, 86,978 insertions, 2,913 deletions).
- Test vs product: **171** paths under `tests/` (includes 13 binary/JSON fixture files), **75** non-test paths, of which **43** are `.py` product files.
- Fresh clone: `git clone --no-checkout https://github.com/banodoco/banodoco-workspace-runtime` → `git checkout -q --detach a98fbc2f9544a8be14281e32afde8aafa098f5f7` → `git apply --check` exit 0 → `git apply` exit 0 (whitespace warnings only: 3 "new blank line at EOF" in the patch) → `git add -A` → `git write-tree` = `92ab1f5f739ffdfedf7b25fbd2a7b46ae42c5d1a`.
- **Equals the integration tree** (`92ab1f5f7`).

## Step 3: fast checks on the applied tree
- **Lint / typecheck: none declared.** `pyproject.toml`, `.github/workflows/ci.yml` and the repo root have no ruff, pyright, mypy or flake8 config. Nothing was run; this is not a failure.
- **py_compile-equivalent (PASS):** `compile_changed.py` (in scratch) reads each changed non-test `.py` path from the name-status list and calls `compile()` on it. Command: `python3 -I .../scratchpad/zip2/compile_changed.py .../scratchpad/zip2/files.txt .../scratchpad/zip2/fresh` → `product .py files compiled: 43; failed: 0`, exit 0.
- **Smoke subset of tests: REFUSED.**
  - The runtime test deps (`pytest>=8`, `pytest-timeout`, `pytest-xdist`, `jsonschema`, `referencing`, `PyYAML`, `setuptools`) are not in `/usr/bin/python3` (`No module named 'pytest'`).
  - A private venv was created in scratch (`python3 -m venv .../scratchpad/zip2/venv`, exit 0).
  - `.../zip2/venv/bin/pip install -q "pytest>=8" ...` was refused with the exact message: **`This command requires approval`** (no pip install ran).
  - I did not retry, did not borrow another package set, and did not install into a shared venv. The shared `venv-agent` has `pytest-timeout` and pytest 9.0.2 but no `pytest-xdist`, and I did not confirm `jsonschema`/`PyYAML`, so it is not a usable substitute without a documented decision.
  - **Smoke tests: not run. Count: 0.**
- Failure classification: **environment** (blocked dependency install), not product or harness.

## Step 4: patch against LIVE upstream tip: PASS (apply), with drift
- Re-fetched: `git ls-remote https://github.com/banodoco/banodoco-workspace-runtime refs/heads/main` → **`aa6c5b0cb1b05e47fc3bb597f63565f1aa8f7a70`**. This is newer than the `f23d1e43f` tip in the earlier report, and the fresh clone's `fetch` agrees.
- Upstream drift `a98fbc2f9..aa6c5b0cb` (4 commits, not 3):
  - `b70c323` skip registry: `tests/lanes.py`, `tests/test_skip_registry.py`, `tests/test_skip_guard.py`. Tests only.
  - `6162e0e` skip guard test: `tests/test_skip_guard.py`. Tests only.
  - `f23d1e4` remove dead pictureTracks handling: `runtime_protocol/visual_seam.py` (**product**), `docs/visual-seam-policy.md`, `tests/test_visual_seam_admission.py`, `tests/test_canonical_render_admission.py`.
  - `aa6c5b0` drop Windows from CI; add no_ci to the skip registry: `.github/workflows/ci.yml`, `README.md`, `docs/runtime-portability-testing.md`, `tests/lanes.py`, `tests/test_skip_guard.py`, `tests/test_skip_registry.py` (checked with `git show --name-only aa6c5b0`). **Not listed in the brief or the earlier report.**
- Tip clone: `git clone --no-checkout` then `git checkout -q --detach aa6c5b0cb1b05e47fc3bb597f63565f1aa8f7a70`.
- `git apply --3way --check` → exit 0, no conflict lines.
- `git apply --3way zip2.patch` → exit 0. `git ls-files -u` (unmerged entries) → **none**. `grep` for conflict/error in the apply log → **0 matches**.
- Merged tree (tip + patch, staged, not committed): `9a39fc7ff4597ad51b114e84b2d106cf06956030`. This is expected to differ from the integration tree because of the upstream drift.
- Overlapping files (the 3-way engine resolved all of them cleanly; record only):
  - `runtime_protocol/visual_seam.py`: integration patch and `f23d1e4` both change it. Clean 3-way merge, but hunk-level semantic correctness is **not verified**.
  - `tests/lanes.py`, `tests/test_skip_guard.py`, `tests/test_visual_seam_admission.py`, `tests/test_canonical_render_admission.py`: also touched by upstream. Clean merges.
  - `tests/test_skip_registry.py`: upstream only, not in the patch.
- Product-side compile of the merged tip tree: `compile_changed.py .../zip2/files.txt .../zip2/tip` → `product .py files compiled: 43; failed: 0`.
- Caveat: the upstream drift was not in the brief's deferred list. Per the brief I did not merge anything; the drift stays as-is and this step only observed it.

## Commands and exit codes (summary)
| Step | Command | Result |
|---|---|---|
| 1 | `git -C /home/user/work/runtime rev-parse tl/integration hub/timeline/runtime/tl/integration` | both `9ce4242bc…` |
| 1 | `git -C /home/user/work/runtime merge-base --is-ancestor a98fbc2f9 tl/integration` | exit 0 |
| 2 | `git -C /home/user/work/runtime diff --binary a98fbc2f9 tl/integration > zip2.patch` | 5,209,625 bytes, 246 files |
| 2 | `git clone --no-checkout …; git checkout -q --detach a98fbc2f9…; git apply --check; git apply; git add -A; git write-tree` | write-tree `92ab1f5f7` = integration tree |
| 3 | `python3 -I compile_changed.py … fresh` | 43 compiled, 0 failed |
| 3 | `python3 -m venv …/zip2/venv` | exit 0 |
| 3 | `…/zip2/venv/bin/pip install -q …` | **REFUSED: "This command requires approval"** |
| 4 | `git ls-remote https://github.com/banodoco/banodoco-workspace-runtime refs/heads/main` | `aa6c5b0cb…` |
| 4 | `git -C fresh fetch -q <upstream> refs/heads/main` | ok; `log a98fbc2f9..FETCH_HEAD` = 4 commits |
| 4 | `git apply --3way --check zip2.patch` (tip clone) | exit 0, no conflicts |
| 4 | `git apply --3way zip2.patch` (tip clone) | exit 0; `ls-files -u` empty |

## Environment issues
- `workers/tf-zip2-runtime/tmpdir` is a **file** (18 bytes: `/tmp/w-91689c2a14`), not a directory, so I could not use it. I left it untouched and used the session scratchpad `/tmp/w-91689c2a14/claude-0/-home-user-work-wt-tf-zip2-runtime/a132f895-c5cc-4871-b45c-756be1560034/scratchpad/zip2/` instead. Scratch files: `zip2.patch`, `files.txt`, `fresh/`, `tip/`, `compile_changed.py`, `tip-apply.log`, `venv/`.
- Shell notes: `$VAR` in commands and `cd` with git are blocked by the command reviewer; I used literal paths.

## Recommended next steps
1. Orchestrator: approve `pip install` for a runtime venv (`pytest>=8 pytest-timeout pytest-xdist jsonschema referencing PyYAML setuptools>=70.1`), or provision `/home/user/work/venv-runtime`. Then run the smoke subset on the applied fresh tree (step 3's remaining half).
2. Decide whether the upstream drift is in scope. It now includes `aa6c5b0` (CI/skip registry), which the brief did not list.
3. Hunk-level review of `runtime_protocol/visual_seam.py` after the 3-way merge (the only product-code overlap).
4. Runtime has no lint or typecheck config, so the "fast checks" are compile plus smoke tests only.
