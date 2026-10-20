Implemented the private proposal on base `a53703ce66de7119b6bef51376e274b8ad6296e7`.

- Added approved `project-data.write` v1 schema/module/registry/rebase support.
- Preserved existing 55/29 carrier structure and 12 v2 branches.
- New schema hash: `39211e63...317429d`
- Removing only the project-data additions reconstructs carrier hash `613123b2...9aaad3`.
- Ordinary `6ba...` compatibility floor remains passing.
- Published proposal: [ORCH design](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-private-full-carrier-project-data-source-proposal.md>)

Tests:

```text
69 passed in 225.60s
```

Command:

```bash
PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_recipe_m2_project_data.py \
  tests/sdk/test_timeline_materialization_schema_union.py \
  tests/sdk/test_timeline_current_union_schema.py
```

`git diff --check` passed. No generated files, pins, releases, or integration changes. Peer ACK remains pending.

Commit message written and `DONE` created under the assigned orchestrator worker directory.