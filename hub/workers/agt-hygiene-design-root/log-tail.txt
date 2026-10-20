## Report: agt-hygiene-design-root

**Result:** `tests/reshape/test_repo_hygiene.py::test_live_tree_passes_repo_hygiene` should pass again. The root `design/` directory is gone. The two compile-contract docs now live in `docs/design/`, which is already an allowed location. I did not touch `ROOT_DIR_ALLOWLIST`. I did not run the full suite, and I did not push, merge, or commit.

**What changed (worktree `/home/user/work/wt/agt-hygiene-design-root`):**
- Moved `design/audio-compile-contract.md` and `design/visual-compile-contract.md` to `docs/design/`. The directory `design/` is removed.
- Updated the references in:
  - `tests/editing_conformance/test_compile_contracts.py` (docstring)
  - `tests/editing_conformance/fixtures/audio_compile_contract.json` and `visual_compile_contract.json` (`contract` field)
  - `tests/packs/rendering/test_normal_audio_source_phase.py` (docstring)
  - the two moved docs, which reference each other's path and `owner-film-differences.md`

**Decisions:**
- I used `mv` and `sed` instead of `git mv`/`git rm`, because the sandbox refused some shell forms. The harness will stage the deletions and the additions.
- I also rewrote the `design/owner-film-differences.md` references to `docs/design/owner-film-differences.md`, to keep them consistent with the move. That file is not in this tree, so those references are still dangling. They were dangling before this change too.

**Tests:**
- Command: `bin/request-test agt-hygiene-design-root targeted --files "tests/reshape/test_repo_hygiene.py tests/editing_conformance/test_compile_contracts.py tests/packs/rendering/test_normal_audio_source_phase.py"`, run as `pytest -q` in the venv.
- Result: **pass**, 41 passed, 6 xfailed in 1.35s.
- The 6 xfails are the existing strict xfails (audio vectors 10–11 and the four PCM tests), which the contract documents. I did not change any test expectations.

**Unverified:** The moved docs' own cross-references (for example, `docs/reference/...` paths) were not re-checked beyond the targeted run. I did not run `check_doc_references` or any docs-alignment test.

**Artifacts:** `commit-msg` and `DONE` are written under `$ORCH/workers/agt-hygiene-design-root/`. No build output or temp files were left in the worktree.

**Recommended next step:** Run the full suite through the central service once the orchestrator approves it. Also decide whether `design/owner-film-differences.md` should be created in `docs/design/` or the references dropped.
