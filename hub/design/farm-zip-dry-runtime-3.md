# F-zip-dry rehearsal 3: runtime (tf-zip3-runtime)

**Status: PARTIAL / BLOCKED. Steps 1, 2, 4 and the py_compile half of step 3 PASS. The smoke tests are REFUSED: `pip install` into the private venv returned `This command requires approval`, even though the brief says pip is allowed. No tests ran (count 0). Nothing was pushed, committed or edited in any product repo or worktree.**

Scratch: `/tmp/w-057577a360/` (my tmpdir). Nothing was written to the worktree `/home/user/work/wt/tf-zip3-runtime`, to `evidence/` or to `notes/`.

## Step 1: integration, base, hub: PASS
- Hub integration `refs/heads/timeline/runtime/tl/integration` (`git ls-remote hub`) = `9ce4242bc01f100bab9efc51032a73985cefb2b2`. Local `tl/integration` = the same SHA. This matches the predecessor, so the hub has not moved.
- Integration tree `92ab1f5f739ffdfedf7b25fbd2a7b46ae42c5d1a`.
- Base `a98fbc2f9544a8be14281e32afde8aafa098f5f7`.

## Step 2: patch and fresh clone apply: PASS
- Patch: `git -C /home/user/work/runtime diff --binary --output=/tmp/w-057577a360/zip3.patch a98fbc2f9544a8be14281e32afde8aafa098f5f7 9ce4242bc01f100bab9efc51032a73985cefb2b2`. Not re-counted this run. The predecessor measured 246 files.
- Fresh clone: `git clone -q --no-checkout https://github.com/banodoco/banodoco-workspace-runtime /tmp/w-057577a360/fresh`, then `git -C … checkout -q --detach a98fbc2f9544a8be14281e32afde8aafa098f5f7` → HEAD `a98fbc2f9544a8be14281e32afde8aafa098f5f7`.
- `git -C … apply --check` → exit 0. `git -C … apply` → exit 0, with 3 "new blank line at EOF" whitespace warnings only. `git -C … add -A`.
- `git -C … write-tree` = **`92ab1f5f739ffdfedf7b25fbd2a7b46ae42c5d1a` = integration tree. Equal.**

## Step 3: checks on the applied tree
- **py_compile (PASS):** `python3 -I -m compileall -q` over `runtime_protocol astrid_runtime generators scripts packages/python tools` in `/tmp/w-057577a360/fresh` → no error output. (Exit code not captured separately. No output under `-q` means no compile errors.)
- **Lint / typecheck:** none declared in `pyproject.toml` or CI. Not run; this is not a failure.
- **Smoke tests: NOT RUN (REFUSED).**
  - Created the venv: `python3 -m venv /tmp/w-057577a360/venv` → Python 3.13.16, ok.
  - Attempted: `/tmp/w-057577a360/venv/bin/pip install -q "pytest>=8" "pytest-timeout>=2.4" "pytest-xdist>=3" "jsonschema>=4.18" "referencing>=0.30" "PyYAML>=6" "setuptools>=70.1"`
  - Exact refusal: **`This command requires approval`**. Nothing was installed.
  - Per the brief I did not retry, did not borrow `/home/user/work/venv-*` or the `runtimes/` interpreters, and did not install anything elsewhere.
  - Planned command, once pip is allowed: `python -m pytest -q -n 2` with `PYTHONPATH` on the fresh tree. Smoke subset not yet chosen.
  - Classification: **environment** (the sandbox denied a dependency install). Not product, not harness.

## Step 4: patch against live upstream tip: PASS (apply), drift recorded
- Live upstream `git ls-remote https://github.com/banodoco/banodoco-workspace-runtime refs/heads/main` → **`aa6c5b0cb1b05e47fc3bb597f63565f1aa8f7a70`**. The predecessor saw `f23d1e43f`, then this tip.
- Drift `a98fbc2f9..aa6c5b0cb` (4 commits, `git log --name-only` on the fetched tip):
  - `b70c323` skip registry (tests only): `tests/lanes.py`, `tests/test_skip_guard.py`, `tests/test_skip_registry.py`.
  - `6162e0e` skip guard test: `tests/test_skip_guard.py`.
  - `f23d1e4` remove dead pictureTracks handling: `runtime_protocol/visual_seam.py` (product), `docs/visual-seam-policy.md`, `tests/test_visual_seam_admission.py`, `tests/test_canonical_render_admission.py`.
  - `aa6c5b0` drop Windows from CI, add no_ci to the skip registry: `.github/workflows/ci.yml`, `README.md`, `docs/runtime-portability-testing.md`, `tests/lanes.py`, `tests/test_skip_guard.py`, `tests/test_skip_registry.py`.
- Tip clone: `git clone -q --no-checkout …` → `/tmp/w-057577a360/tip`, `checkout --detach aa6c5b0cb…`.
- `git -C …/tip apply --3way --check zip3.patch` → exit 0, no conflict lines.
- `git -C …/tip apply --3way zip3.patch` → exit 0. The log says "Applied … cleanly" for every file, with "Falling back to direct application" in many. One whitespace warning only, not a conflict.
- `git -C …/tip ls-files -u` → **0 unmerged entries.**
- `git -C …/tip add -A; write-tree` = **`9a39fc7ff4597ad51b114e84b2d106cf06956030`** (merged tip + patch). This differs from the integration tree, as expected, because of the upstream drift.
- **Overlap (patch ∩ upstream drift), 5 files, all clean 3-way merges; record only:**
  - `runtime_protocol/visual_seam.py`: product. Both sides changed it (the integration side and `f23d1e4`). Clean at the hunk level, but **semantic correctness is not verified**. This is the one to review.
  - `tests/lanes.py`, `tests/test_skip_guard.py`, `tests/test_visual_seam_admission.py`, `tests/test_canonical_render_admission.py`: tests only.
  - `tests/test_skip_registry.py` is upstream-only (not in the patch).
- Compile of the merged tip tree: `python3 -I -m compileall -q` over the same package list → no error output.

## Commands and results
| Step | Command (abridged) | Result |
|---|---|---|
| 1 | `git -C /home/user/work/runtime ls-remote hub refs/heads/timeline/runtime/tl/integration` | `9ce4242bc…` |
| 1 | `git -C /home/user/work/runtime rev-parse tl/integration` | `9ce4242bc…` |
| 2 | `git -C /home/user/work/runtime diff --binary --output=zip3.patch a98fbc2f9 9ce4242bc` | written |
| 2 | `git clone -q --no-checkout …; checkout -q --detach a98fbc2f9` | HEAD `a98fbc2f9` |
| 2 | `git -C fresh apply --check zip3.patch` / `apply zip3.patch` | exit 0 / exit 0 (whitespace warnings) |
| 2 | `git -C fresh add -A; write-tree` | `92ab1f5f7` = integration tree |
| 3 | `python3 -I -m compileall -q …/fresh/{packages}` | no output (no errors) |
| 3 | `python3 -m venv /tmp/w-057577a360/venv` | ok |
| 3 | `…/venv/bin/pip install -q "pytest>=8" …` | **REFUSED: `This command requires approval`** |
| 4 | `git ls-remote https://github.com/banodoco/banodoco-workspace-runtime refs/heads/main` | `aa6c5b0cb…` |
| 4 | `git -C fresh fetch -q <upstream> refs/heads/main` | ok; 4 drift commits |
| 4 | `git clone …/tip; checkout --detach aa6c5b0cb` | ok |
| 4 | `git -C tip apply --3way --check zip3.patch` | exit 0, no conflicts |
| 4 | `git -C tip apply --3way zip3.patch; ls-files -u` | exit 0; 0 unmerged |
| 4 | `git -C tip add -A; write-tree` | `9a39fc7ff…` |
| 4 | `python3 -I -m compileall -q …/tip/{packages}` | no output (no errors) |

Shell notes: `$VAR`, `$?`, `cd`, and `ls`/`cat` of the tmpdir were refused by the command reviewer. Only the `-C` git form and literal paths worked.

## Failure classification
- Smoke tests: **environment** (`pip install` refused). Not product, not harness.

## Recommended next steps
1. Orchestrator: approve the pip install of the 7 test requirements into `/tmp/w-057577a360/venv`, or provide a runtime venv. Then run the smoke subset on `/tmp/w-057577a360/fresh` (integration) and `/tmp/w-057577a360/tip` (live tip), e.g. `python -m pytest -q -n 2 tests/<subset>` with `PYTHONPATH` pointing at the scratch tree. No full suite was run here.
2. Decide whether the `aa6c5b0` drift is in scope. It changes CI (drops Windows) and the skip registry. The brief did not list it.
3. Review the `runtime_protocol/visual_seam.py` hunk after the 3-way merge (the only product-code overlap).
4. No commit was made in this worktree: there are no product changes, so no commit message was written.
