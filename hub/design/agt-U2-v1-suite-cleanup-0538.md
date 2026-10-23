# U2-v1-suite-cleanup-0538 — PASS

This was a bounded operational cleanup, not a product change. Per the settled
PLAN/BOARD-HEADER direction, only the external allow-list file was edited:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`

The two exact retired graph rows removed were pre-edit lines 73 and 74:

```text
agent remotion-0010-nodes ... ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0010 ...
agent remotion-0012-nodes ... ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0012 ...
```

The complete command rows were the standard `env -i ... /home/user/work/venv-agent/bin/python -m pytest -q -n 2` rows. No other suite row was selected by suite name substring or by unrelated `0012` text. In particular, the active related rows and Composition14/native-v2 rows were preserved.

## Reproducible evidence

The verification reconstructed the pre-edit bytes by inserting the two recorded
rows at their original positions, then checked:

- before SHA-256: `4f6aaf8a1e8ef12205722f20129c0efbaffdd499c45613588b7598a0fb01a4c8`
- after SHA-256: `f3a50f5c4cae32b37831c520e5c5920c361c40419a119bd649b3241cb01dfb3d`
- before bytes: `106065`
- after bytes: `104635`
- removed-line count: `2`
- outside-line byte equality: `PASS`

The non-executing parser used the same three-field shape consumed by
`bin/test-run` (`repo`, `suite`, `COMMAND` via `split(maxsplit=2)`). It found
`127` nonblank rows and `127` unique repo/suite keys; the two deleted suite
keys were absent. Parser check: `PASS`.

`git status --short --branch` in the assigned Agent worktree reported no
working-tree changes. No tests were run because this task is external config
cleanup and explicitly forbids old tests/full/browser/heavy execution.
