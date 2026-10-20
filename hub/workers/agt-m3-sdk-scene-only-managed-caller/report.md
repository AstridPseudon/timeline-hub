## Done

- Added private Scene-only managed visualization caller/result adapters.
- Reused `prepare_filmstrip` authority and managed output binding.
- Added exact capture/source/map validation and advisory `UNAVAILABLE` fallback.
- Connected results to existing `_scene_problems` formatting.
- Preserved save-core and publish/transaction purity.
- Appended the approved contract to `design/d09-scene-check-save-core-handoff.md`.
- Wrote commit message and created `DONE`.

## Tests

```text
PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/sdk/test_scene_caller_preservation.py \
  tests/sdk/test_scene_save_core.py \
  tests/sdk/test_timeline_filmstrip.py \
  tests/sdk/test_timeline_filmstrip_invocation.py
```

Result: **87 passed**.

Also passed `git diff --check` and compilation checks.

Ordinary real activation remains intentionally held until Viewing’s executor/query implementation is ready; no full suite was run.