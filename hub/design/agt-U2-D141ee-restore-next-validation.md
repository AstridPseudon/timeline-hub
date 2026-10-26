# Validation

Environment: `PYTHONDONTWRITEBYTECODE=1`, `/home/user/work/venv-agent/bin/python`, `PYTHONPATH=WORKTREE:/home/user/work/runtime`; Runtime was read-only commit `95d98f038320d5d46bd679ac000ab3e15825c935`, tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`.

- Structural AST/input/assertion conservation: PASS, 15 writer15 + 2 schema8 nodes; inverse whole-file SHA PASS (`904063b9...a025`). See `structural-check.log`.
- Writer15 exact targeted selectors: 15 failed with visible current-route/behavior mismatches; final combined rerun stopped at collection because the exact restored authoring import is absent. Logs: `restored-targeted.xml`, `restored-targeted-final.xml`, `restored-targeted-nonauthoring-final.xml`.
- Inverse targeted command `python -m pytest -q tests/timeline/test_inverses.py`: collection ERROR, `ModuleNotFoundError: astrid.core.timeline.inverses`.
- Schema8 class(c) selectors: 2 failed. The first lacks the old staged schema package; the second cannot find `node_modules/@banodoco/timeline-schema` in the current lock.
- Ruff check on all touched tests: exit 1 only for the exact pristine inverse import block/unused `InverseRequest`; no auto-fix applied. `git diff --check`: exit 0.
- Targeted typecheck: N/A; no repository targeted typecheck workflow was identified, and no product source was changed.
- Full/browser/live-socket suites: not run, per task instructions.
