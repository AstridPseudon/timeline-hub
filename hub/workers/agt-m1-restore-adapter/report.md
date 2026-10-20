Implemented `timeline.restore` v1 through the existing commit executor/recorder, preserving exact closure pins, opaque fields, retained inputs, strict head-pair guards, and inverse/redo.

Used a semantic `timeline` root containing only a verified revision/digest pin. No schema/ABI change, renderer, alternate writer, or journal.

Validation:

- `PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py tests/editing_conformance/test_recipe_m1_commands.py` — **145 passed**.
- Central `request-test agt-m1-restore-adapter commit-integration --files 'tests/sdk/test_timeline_commit_provider_runtime.py'` — **4 passed**, including restart and exact retry.
- Changed-file Ruff and `git diff --check` — passed.

No blockers. Notes and both commit-message files written. No Git mutations performed.

Next: manager review/integration, Runtime’s seven caller adaptations, then the manager-owned postmerge full suite. Those remaining checks are unverified here.