## PASS — F-harness-tuple-review

Reviewed only:

- `tools/run-discovery-original-0603.py`
- `tools/run-generic-reopen-original-0605.py`

Verified exact Agent `0c2c28da…`, Runtime `becfe6db…`, candidate name, and client identity `d79568df…`. Source carriers are physical, clean, and correctly pinned. Original bodies, wrappers, custody guards, and contract/client behavior remain unchanged.

Checks passed:

- `py_compile`
- `ruff check --no-cache`
- `mypy --follow-imports=skip`
- `bash -n` wrappers
- `git diff --check`
- AST/hash/source/client identity checks
- Discovery: 9 assertions, 10 support calls, 45-second watchdog
- Generic: 12 assertions, 30-second watchdog
- Diff limited to the two authorized runner files

The shared candidate’s first attempt remains refused by the normal verifier due to unsafe/overlapping NumPy `RECORD`. No registration, READY child, preflight, original runner, process, network, cache, or install execution was performed or claimed. Runtime owns the verifier fix; no Agent guard change is recommended.

Commit message and `DONE` marker were created. Worktree remains clean.