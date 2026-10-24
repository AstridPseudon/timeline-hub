Implemented only [tests/test_visual_seam_admission.py](/home/user/work/wt/rt-U1d-visual-tests-1331/tests/test_visual_seam_admission.py).

- Resolved to incoming upstream seam semantics; removed retired writer helper and superseded raw-FPS cases.
- Preserved 41 tests / 190 assertions; AST matches incoming side exactly.
- Final SHA-256: `5289802f2b2017cf4a6bc23d619dd6558187252b4d581297192d9865b7b38c41`
- Checks passed:
  - `python -m py_compile tests/test_visual_seam_admission.py`
  - `ruff check tests/test_visual_seam_admission.py`
  - `git diff --check`
- No pytest run against the incompatible base source; joined-cohort proof remains pending.
- Commit message written and `DONE` marker created.