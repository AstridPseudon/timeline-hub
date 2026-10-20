Updated only the existing shared design docs:

- `edit-recipe.md`: exact gesture-time guard paths, supported mappings/refusals, follow clears, recorder authority, retained inputs and M1 acceptance checks.
- `suffix-basis.md`: real App capture requirements; dependent ABA policy remains distinct from inverse protection.
- `command-schema-handoff.md`: identity-only `id_map`, structural proof requirement and alignment with Runtime’s updated DTOs.

Schema unchanged. Runtime now omits independent `PreparedCommit.commands`; response commands derive from authoritative records.

Validation:

```bash
PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m0-a-guards/pytest-tmp /home/user/work/wt/agt-m0-command-schema/tests/m0_command_schema
```

**95 passed in 0.37s.** JSON parsing, shared-document whitespace checks and `git diff --check` passed.

No product implementation or full suites run. Real App capture and structural framework behavior remain M1 evidence requirements. No blockers.

Commit message written to the requested path. Worktree remains clean; changes are in shared docs. Next: manager review, then M1 after gate approval.