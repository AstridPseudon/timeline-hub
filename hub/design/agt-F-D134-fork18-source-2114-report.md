## D134 report

Status: **finite `UNAPPLIED`**. No assigned test files or product code were changed.

- Confirmed root-008’s exact 18 members: all `UNKNOWN`, no proven product fault.
- Traced the failure: active production fork capture appends physical `commit.effect` bindings, while ABI-1 requires the exact four native bindings.
- The genuine v2 fork comparator passes structurally but cannot substitute for ABI-1 history.
- No fabrication, assertion changes, ABI normalization, or legacy-route revival was performed.

Validation:

- Python 3.11 AST/compile: PASS
- Ruff on both assigned files: PASS
- `git diff --check`: PASS
- Scoped mypy baseline: blocked by 14 unrelated environment errors (missing YAML stubs / NumPy Python-version mismatch)
- Live tests: not run; published ab1e route reports an exact missing fixture input.

Evidence: [source-manifest.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D134-fork18-source-2114/evidence/source-manifest.json), [setup-proof.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D134-fork18-source-2114/evidence/setup-proof.md), [validation.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D134-fork18-source-2114/evidence/validation.md).

`BLOCKED` and the D134 commit message were written for the harness.