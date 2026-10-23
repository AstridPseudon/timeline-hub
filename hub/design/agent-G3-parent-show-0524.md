# Agent G3 parent-native ordinary show handoff

Base: `9b658b28c3a7bc3ebda3ad5a7b5b417d78553720`.

Implemented only the bounded ordinary-show projection repair:

- `astrid/core/timeline/cuts.py`: no-placement bundles now adapt canonical `parent.clips` through the existing snapshot/span projection, use `timeline_duration_seconds` plus `clip_start_frame`/`clip_end_frame`, return no picture cuts for audio-only parents, and leave the legacy placement/shared-audio branch intact.
- `astrid/sdk/timeline_cuts.py`: the existing cut-table caller handles parent-native occurrences and preserves the canonical parent extent without creating a fake chapter/shot.
- `tests/sdk/test_timeline_show_views.py`: real `_print_cut_table` regression with parent clips `a` at 5 and `b` at 0, asserting duration 7, rows `b`, gap, `a`, and the parent clip count.

Exact targeted proof:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_cuts.py tests/sdk/test_timeline_show_views.py tests/timeline/test_cuts_views.py tests/timeline/test_mixed_mode_cut.py tests/timeline/test_multitrack_cut.py
55 passed, 2 subtests passed
```

Focused show/cuts subset: `20 passed`.

Quality/provenance:

- Changed-file Ruff for core/test files: PASS.
- `make PY=/home/user/work/venv-agent/bin/python ruff`: PASS, 2149/2149 baseline.
- Private scoped mypy: same pre-existing HEAD diagnostics (core 1, SDK 2); no new findings.
- Normal make mypy: environment-blocked by missing `types-PyYAML` and incompatible NumPy stubs; no dependency writes.
- Pinned vendor lock: PASS with `/home/user/work/wt/rt-pin-34eac004`.
- Artifact manifest: PASS.
- `git diff --check`: PASS.
- Import origins: Agent modules from this worktree; `runtime_protocol` from `/home/user/work/runtime`.

The exact requested handoff path under `/home/user/peteromallet/astrid-agent/docs/projects/timeline-r4/` was absent; authoritative copies were read from the orchestrator scratchpad design directory. No source changes were made outside this worker worktree. No full/browser/live-socket/Proof HTTP retry was run; central P4 retry remains for orchestrator/Proof after review.

