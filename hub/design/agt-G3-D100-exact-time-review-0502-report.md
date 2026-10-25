# PASS_SOURCE

Reviewed commit `404044d6aa` against parent `6cd767b6af`. Only the allowed files changed.

- Exact arithmetic is routed through `Fraction` for duration, FPS quantization, occurrence origin, local time, and strict next-occurrence checks (`capture.py:52-54, 81-91, 194-238`).
- Existing input rejection, codec handling, writes, assertions, and topology are preserved. Output conversion remains only at the existing JSON write boundary (`capture.py:241-252`).
- Production path traced: `capture_move` → `commands.execute` → registered `clip.move` operation → `capture.move`; `placement.move` delegates to the same shared move handler.
- Regression test uses `capture_move` plus registered `execute`, not private arithmetic. Old parent is source-predicted RED; candidate is source-predicted GREEN, including the over-bound refusal.

Checks:

- In-memory compile: candidate pair and parent: PASS
- Ruff candidate and parent: PASS
- Mypy candidate and parent snapshot: PASS
- `git diff --check`: PASS
- Pytest/service/full suites: not run per source-only instructions.

The requested R4 docs were absent at the supplied filesystem path; I used the available orchestrator copies of `commit-v2.md` and `BOARD-HEADER.md`. MAIN should run:

```bash
/home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_capture_move_exact_time.py
```

No functional result is claimed until that selector runs on MAIN. Pre-existing `placement.move` extent tolerance remains unchanged outside the allowed pair.