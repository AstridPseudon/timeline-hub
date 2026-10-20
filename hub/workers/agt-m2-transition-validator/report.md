Implemented branch-only changes in the validator and direct tests.

- Added `document_kind="canonical"` for incoming declarations. Native compiled outgoing validation remains the default.
- Canonical validation permits first clips, gaps, overlaps, oversized windows, and aliases. It rejects malformed and nonfinite durations.
- Existing behavior tests remain unchanged.

**Contract finding:** a predecessor-fit restriction would also reject ratified oversized windows. Canonical validation therefore imposes no pair-fit limit; predecessor/preroll pairing remains the compiler’s responsibility.

**Caller seam remains open:** canonical admission at `managed_timeline.py:787` shares `validate_timeline` with raw/native serialization at `banodoco_composer.py:185,271` and container validation at `banodoco_schema.py:581`. Canonical boundaries must explicitly select the layer alongside the paired conversion. Those caller edits exceed this task’s scope.

Validation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/core/timeline/test_transition_validation.py tests/test_schema_contract.py
```

105 passed; 6 subtests passed.

```bash
/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/core/timeline/validators/timeline.py tests/core/timeline/test_transition_validation.py
git diff --check
```

Both passed. No full/socket tests or render parity verification ran.

Wrote both required `commit-msg` and `commit-msg.txt` files. No commit or merge performed. Next: review paired conversion and canonical caller wiring; merge only after PLAN records M1.