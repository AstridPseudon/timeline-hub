Created the [canonical schema](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/edit-command.schema.json) and [handoff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/command-schema-handoff.md), with inverse/restore signatures, minimal `clip.move`, projection checks, and validated examples.

Preserved R4 command field types and adopted the final recipe’s enriched recorder leaves. Runtime-owned shapes and product code remain untouched.

Validation:

- `PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/m0_command_schema` — **95 passed in 0.46s**.
- `/home/user/work/venv-agent/bin/python -m ruff check --isolated --select E4,E7,E9,F,I,BLE tests/m0_command_schema` — passed.
- `git diff --check` — passed.

No blockers. These are schema-design checks; product gates and provider behavior remain unverified.

Next: apply the handoff’s enumerated recipe corrections, retire its competing schema source, and pin the canonical artifact into Agent/Runtime. Retarget the isolated tests to the packaged schema before product-suite integration.

Commit message written to the requested path; test caches removed.