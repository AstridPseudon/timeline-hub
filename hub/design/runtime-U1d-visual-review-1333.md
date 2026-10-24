# U1d independent review: FAIL

- Reviewed `becfe6db`, actual mergebase `795379a67`, completed source `9db3ec867`, completed tests `e93805e4d`, and incoming `d4f496ec`.
- Source PASS: retains canonical clip checks, rational-FPS `_fps` handling, full-frame coverage, occurrence seams, and cue filtering.
- Test FAIL: incoming union removes:
  - `test_render_materialization_accepts_raw_rational_fps`
  - `test_render_materialization_rejects_invalid_fps`

`60a919a22` is an ancestor of `becfe` and introduced these live predicates. Incoming source line 165 uses `finite(...)`, which rejects the approved mapping/list FPS forms; completed source line 198 correctly calls `_fps(...)`.

Other renamed predicates were intentional upstream full-frame/overlay behavior changes, documented in `docs/visual-seam-policy.md`.

Checks passed:

- `python -m py_compile runtime_protocol/visual_seam.py`
- `ruff check runtime_protocol/visual_seam.py`
- Completed test blob AST/compile-equivalent and Ruff checks
- `git diff --check`

No pytest run; combined targeted testing belongs to `rt-U1d-final-1329`.

Exact blobs: source `9bb0bfb0`, docs `dca6a01c`, tests `d5fe3a20`. Commit message and `DONE` marker created.