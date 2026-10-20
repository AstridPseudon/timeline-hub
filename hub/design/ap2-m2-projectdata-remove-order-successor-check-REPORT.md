# App2 project-data remove ordered-inverse source recheck

## Decision

**ACK** the exact unfrozen Agent successor for the original namespace-order HOLD.
The serialized remove -> inverse -> redo witness now restores a pruned target
namespace between its original `config.app` siblings and preserves raw values.

Qualified source tuple:

- Agent commit: `b4493c75947f8605e61852f340e56b27e24c4adb`
- Agent tree: `24c0900be7d469d1250ca9883b7714c72308ed81`
- Branch: `tl/agt-m2-projectdata-remove-ordered-inverse`
- Schema SHA-256: `0357ef34fbac2416be59dc906fa5a9d9173e322ff1d1e53b758f5c890d543906`
- Changed paths are limited to `_project_data_commands.py`, `_recording.py`,
  `_command_state.py`, `inverse.py`, and the focused project-data conformance
  test.

## Evidence

All probes used a private extracted archive of the exact commit and the existing
narrow fixture. The extracted source was removed at process exit.

- `PYTHONPATH=<extracted-source> /home/user/work/venv-app2-native/bin/python -m pytest -q tests/editing_conformance/test_recipe_m2_project_data.py --disable-warnings --maxfail=1`
  — **22 passed**, 2 warnings.
- `PYTHONPATH=<extracted-source> /home/user/work/venv-app2-native/bin/python -m pytest -q tests/editing_conformance/test_inverse_clear_batches.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py --disable-warnings --maxfail=1`
  — **157 passed**, 2 warnings.
- One-off private probe using the same fixture — **PASS**. It asserted
  `list(config.app)` and exact raw `null`/absence/opaque values through
  serialized remove, serialized guarded inverse, serialized redo, and a new
  unrelated sibling namespace added after removal. Orders were:
  `before, after` -> `before, com.example.compiler-canary, after,
  com.example.unrelated` -> `before, after, com.example.unrelated`.
- `git diff --check b449^ b449` — **PASS**.

The source keeps the sole `mode: "remove"` spelling, does not add an alias,
operation, public carrier, or store, and retains existing schema floors and
overlapping-guard refusal. No App product files were changed; no writer
retirement, activation, generation, pin, freeze, adoption, browser, socket,
central test service, or full suite was run.

## Follow-up boundary

This is source qualification only. It does not authorize source composition,
generation, pinning, activation, or App writer retirement.
