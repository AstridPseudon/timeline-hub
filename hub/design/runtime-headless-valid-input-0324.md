**Blocked by an additional required declaration.** Only `tests/test_timeline_headless_overwrite_refused.py` changed.

- Added the standard authored visual track and clip reference to the positive copy, with exact reconstruction checks.
- Added a strict trackless negative using genuine verified media. It passed, including retry and complete SQL/CAS/head/history no-write checks.
- Preserved all 67 original assertions, historical requests, constants and C0 request metadata.

The single authorized family run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/test_timeline_headless_overwrite_refused.py
```

**12 passed, 1 failed.** The positive fails at Agent `_doc_patch.py:480`: adding `parent/track:picture` requires declaring that created identity. The unchanged request declares only asset and clip. Stopped without further body changes or reruns, per instruction.

Other checks:

- Ruff, parent/final: `ruff check --no-cache --output-format json --stdin-filename <worktree>/tests/test_timeline_headless_overwrite_refused.py -` — same two existing B010 findings; **zero new**.
- Pyright, parent/final: `PYTHONDONTWRITEBYTECODE=1 /root/.local/bin/pyright --project /tmp/w-a3cd913107/checks-{parent,final}/pyrightconfig.json --pythonpath /home/user/work/venv-runtime/bin/python --outputjson` — one file each, **zero diagnostics**.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python /tmp/w-a3cd913107/static_checks.py` — AST/assertion map, original constants, compilation and diagnostic comparison passed.
- `git diff --check` — passed.

Runtime base: `b67f88d4`. Agent remained clean at reviewed `622b30a8`, tree `49c96e08`; imported source origins/blobs matched before and after. **No source advancement.**

Next: manager decision authorizing the track’s created declaration and corresponding record expectation. Accepted-path downstream assertions remain present but unqualified. Wrote `commit-msg` and `BLOCKED`; no full suite or Git writes.