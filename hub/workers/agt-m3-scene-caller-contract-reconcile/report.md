## Done

- Reconciled SDK Scene-only caller with the managed `filmstrip_bundle` → `scene-answers.json` contract.
- Added digest/ZIP integrity, source provenance, label, clip-map, layer, and full-frame validation.
- Missing source binding now returns advisory `UNAVAILABLE`, never `COVERED`.
- Updated fixtures; added source-binding negative and candidate-label positive.
- No save/core, executor, D09 deletion, or parity changes.

Tests:

```text
git diff --check
```

Passed.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_scene_caller_preservation.py tests/sdk/test_scene_save_core.py tests/sdk/test_timeline_filmstrip.py tests/sdk/test_timeline_filmstrip_invocation.py
```

**89 passed in 4.27s**

Ordinary live executor/Node qualification and full suites were not run. D09 remains held.

Changed files:

- [timeline_filmstrip.py](/home/user/work/wt/agt-m3-scene-caller-contract-reconcile/astrid/sdk/timeline_filmstrip.py)
- [test_scene_caller_preservation.py](/home/user/work/wt/agt-m3-scene-caller-contract-reconcile/tests/sdk/test_scene_caller_preservation.py)

Handoff, report, commit messages, and `DONE` marker published.