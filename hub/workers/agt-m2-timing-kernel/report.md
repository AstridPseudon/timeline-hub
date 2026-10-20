Implemented the branch-only pure compiler: immutable captured inputs, verified transcript pins, stable word bindings, rational timing, and atomic refusal. Authored data stays unchanged; derived intervals are returned separately. Added 519 product lines and 434 test lines.

Validation:

```bash
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timing_compiler.py tests/sdk/test_timing_cycles.py tests/sdk/test_timeline_checkout.py tests/sdk/test_timeline_reflow_golden.py tests/sdk/test_timeline_reflow_keep.py tests/sdk/test_media_transcript.py tests/sdk/test_intent_app_astrid.py tests/test_timeline_editing_helpers.py tests/sdk/test_timeline_cuts.py --tb=short
```

**202 passed, 17 deselected**, four Pillow deprecation warnings.

```bash
/home/user/work/venv-agent/bin/ruff check astrid/sdk/timeline/compiler.py astrid/sdk/timeline/_timing_evaluators.py tests/sdk/test_timing_compiler.py tests/sdk/test_timing_cycles.py
```

Passed.

No task blockers. Integration still needs the word/occurrence capture adapter and legacy-writer migration/parity. Unsupported maps, formulas, sequences, beats, and reflow declarations refuse explicitly. Full and integration suites remain unverified.

Both required absolute `commit-msg` files were written. Generated caches cleaned; no commits, merges, pushes, or merge requests.