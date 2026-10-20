Implemented scalar M2 fixture diet.

- Factored shared input and independent expected patches across four scalar JSON fixtures.
- Preserved all 5 cases, command/guard goldens, full expanded-document equality, and portable parity.
- Reduced fixture bytes: 53,710 → 24,783 (53.9%).
- No product/schema/public fixture paths changed.

Tests:

```text
pytest ...test_recipe_scalar_commands.py ...test_fixture_loader.py
75 passed
ruff: passed
pyright: 0 errors
git diff --check: passed
```

Reports written:

- [design report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-test-fixture-diet-current.md)
- [worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-test-fixture-diet-current/notes/report.md)

Commit message and `DONE` marker created.