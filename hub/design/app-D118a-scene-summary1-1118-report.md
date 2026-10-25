Implemented D118a in [test_scene_real_public_summary_rle.py](/home/user/work/wt/app-D118a-scene-summary1-1118/tests/sdk/test_scene_real_public_summary_rle.py).

- Added test-scoped removal of inherited `PYTHONNOUSERSITE`, proven to cause the `scene_answers.py:76` failure.
- Preserved all real host, span, summary, frame, and provenance assertions.
- Static checks passed: ruff, mypy, py_compile, `git diff --check`, AST conservation.
- Protected independent review: passed.
- Target renderer test was not run per static/source-only constraints.
- Evidence: `facts.json` and `facts.md`; commit message prepared.
- Completion marker created: `DONE`.