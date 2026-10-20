# App2 native parity environment

Prepared 2026-10-20 for the App2 duplicate-capture prerequisite (PLAN Gates 5/6).
This is a private Agent test environment only; it does not claim Runtime durability,
browser coverage, or writer retirement.

## Reproducible inputs

- Interpreter: `/home/user/work/venv-app2-native/bin/python` (Python 3.12.3)
- Environment is private and must be treated as read-only by downstream workers.
- Duplicate source: Agent `68a51203310eb7c1bad343e50a42cf75c46c5321`
  (extracted with `git archive` to
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-duplicate`).
- Parent-media source: Agent `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`
  (extracted with `git archive` to
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary`).
- Both source trees were checked against the Agent root `AGENTS.md`. No source
  checkout or shared integration worktree was changed.

Installed into the private venv only:

```
pytest==9.0.2
jsonschema==4.26.0
PyYAML==6.0.3
```

`pytest` and `jsonschema` are declared by the Agent test/runtime requirements.
`PyYAML>=6.0` was the only additional import required by the repository
`tests/conftest.py` (`astrid.core.pack.canonical`). Its normal dependencies were
installed by pip. No production editable install or optional/heavy dependency was
used; `httpx` was not needed by either targeted recipe.

## Evidence

Commands were run with no pytest config and no cache provider, using only the
extracted Agent source on `PYTHONPATH`:

```
PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-duplicate \
/home/user/work/venv-app2-native/bin/python -m pytest -q -c /dev/null -p no:cacheprovider \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-duplicate/tests/editing_conformance/test_recipe_occurrence_duplicate.py
```

Result: **63 passed in 4.07s**.

```
PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary \
/home/user/work/venv-app2-native/bin/python -m pytest -q -c /dev/null -p no:cacheprovider \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary/tests/editing_conformance/test_recipe_m2_parent_media.py
```

Result: **85 passed in 22.91s**.

These are targeted Agent recipe tests only. No full suite, localhost service,
browser, Runtime, or live-socket test was run.

## App2 handoff

Use the venv interpreter directly and keep the environment read-only. Re-extract
or refresh source privately when a different Agent SHA is required; do not install
the Agent package into this venv. The passing recipes establish native duplicate
and parent-media recipe parity at the stated frozen inputs, not end-to-end App2
capture or Gate 5/6 completion.
