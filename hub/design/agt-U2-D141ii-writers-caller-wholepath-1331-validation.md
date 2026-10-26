# Validation

## Read-only checks

No pytest execution was requested or run. No source/test repair was made.

The initial worker-root trace was:

```text
/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331
/dev/vda  252G  35G  4.7G  89%  /home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331
## tl/agt-U2-D141ii-writers-caller-wholepath-1331
```

The current tree remains clean at `3638da72332dee5ffccacb704c9ac3c794b7c959` before evidence/marker creation; evidence is outside the worktree.

## F7 exact reproduction

Command:

```text
/home/user/work/venv-agent/bin/python --version
/home/user/work/venv-agent/bin/mypy --version
/home/user/work/venv-agent/bin/mypy --follow-imports=silent --ignore-missing-imports astrid/packs/timeline/cli_native.py
```

Result:

```text
Python 3.13.16
mypy 1.17.0 (compiled: yes)
/home/user/work/venv-agent/lib/python3.13/site-packages/numpy/__init__.pyi:737: error:
Type statement is only supported in Python 3.12 and greater  [syntax]
    type _Falsy = L[False, 0] | bool_[L[False]]
                                               ^
Found 1 error in 1 file (errors prevented further checking)
exit=2
```

This fails before `astrid/packs/timeline/cli_native.py` is checked: the repository's configured mypy target is Python 3.11, while the shared interpreter is Python 3.13.16 and the installed NumPy stub uses Python 3.12 `type` syntax. It is `FAIL_ENVIRONMENT`, not a source-level failure.

Diagnostic only (not a replacement for the mandated command):

```text
/home/user/work/venv-agent/bin/mypy --follow-imports=silent --ignore-missing-imports --python-version 3.12 astrid/packs/timeline/cli_native.py
Success: no issues found in 1 source file
exit=0
```

No shared dependency, repository configuration, or environment setting was changed.

## Source/review evidence checked

- Read `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md` first.
- Read both immutable review packets and their `findings.md`, `review.json`, `per-id.json`, `validation.md`, and `handoff.md`.
- Read current CLI handler, `cli_native`, `Timeline`, `TimelineSession`, `RemoteTimelines`, `WorkspaceClient`, generated client, Runtime HTTP/service/port/store/provider, current actor tests, original base actor test, genuine CAS selector, and generated-client conflict control.
- Did not run a full suite, browser/live journey, or pytest.
