Implemented a minimal R2 inverse-stage patch that retains sequential physical write sites after later alias removal. Preserved the exact39229 correction and existing guards.

Validation:

- New focused regression/security tests: **19 passed**
- Existing inverse controls: **77 passed**
- Step-boundary controls: **40 passed**
- Agent strict controls: **20 passed**
- Native-provider smoke: **8 passed**
- Ruff, Pyright, compilation and diff checks: **PASS**

**Qualification remains blocked:** the unchanged genuine regression is **2 passed / 1 failed**. Grouped undo now restores the exact document; redo reaches a separate `validate_step` read-boundary refusal. I left that code unchanged because it is outside the authorized inverse-stage scope.

The broader targeted run had **318 passed, 1 failed, 10 setup errors**. The failure reproduces on the parent; setup errors lacked Agent imports.

[Handoff and findings](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-inverse-boundary-sol-1506/evidence/handoff.md) · [Exact commands](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-inverse-boundary-sol-1506/evidence/commands.txt)

Wrote `commit-msg` and `BLOCKED`. Next: independent security review and scoped ownership of the newly reached redo failure before qualification or release.