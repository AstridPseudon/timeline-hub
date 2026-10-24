Implemented only `tests/test_visual_seam_admission.py`.

- Preserved all incoming 41 tests / 190 AST assertions exactly.
- Restored both FPS cases from `60a919a22`:
  - `test_render_materialization_accepts_raw_rational_fps` at line 566
  - `test_render_materialization_rejects_invalid_fps` at line 576
- Final inventory: 43 tests / 192 AST assertions.
- No shared fixture dependency or production changes.

Checks:

- `python -m py_compile tests/test_visual_seam_admission.py` — passed
- `ruff check tests/test_visual_seam_admission.py` — passed
- `git diff --check` — passed
- Exact two selectors — 8 passed

No full suite run per instructions. Commit message and `DONE` marker created.