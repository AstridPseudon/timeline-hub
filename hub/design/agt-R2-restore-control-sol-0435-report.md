Repaired only [the regression file](/home/user/work/wt/agt-R2-restore-control-sol-0435/tests/sdk/test_timeline_restore_effect_order_runtime.py).

- Reused the existing authenticated P4 MemorySocket/generated-client fixture.
- Corrected restore and publication-undo calls.
- Made the opaque scene schema-valid and specified complete ordered source/inverse expectations independently.
- Preserved history, head-pair, dry-run/no-write and retry checks; added restart checks.
- Left historical ID5 and all three capture/order/ABA controls unchanged.

Static validation passed: AST/in-memory compile, schema predicates, baseline/candidate Ruff and mypy, and `git diff --check`. [Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-restore-control-sol-0435/evidence/checks.txt).

No tests, collection, helpers, fixtures or services were executed. Configured mypy does not check untyped function bodies by default.

Next: one fresh protected review, then actual MAIN old-RED/new-GREEN proof alongside original ID5 and the strict controls. [Call trace and handoff details](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-restore-control-sol-0435/evidence/static-callgraph.md). Product `72a` remains unchanged and HELD.

Prepared the F-D86/R2 commit message and created `DONE`.