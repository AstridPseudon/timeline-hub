## Report

- Proved the production closure defect: `STORE_CONTEXT` omits `stage_stderr_path` and `retain_stage_stderr`.
- This explains the `venv-log-setup` refusal and later loss of stderr during `Store.ensure` rollback.
- Confirmed `STORE_PY`, `STORE_VERIFY`, trust, ownership, RECORD, source, reserve, registration, and verifier controls are unchanged.
- No product edits, Store/body/fixture/child execution, retries, or verifier relaxation.

Validation:

- `bash -n`: PASS
- Embedded Python compile and hash checks: PASS
- `git diff --check`: PASS
- JSON evidence validation: PASS
- Existing 44/44 suite was not rerun per task restrictions.

Evidence:

- [findings.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-D137-shell-wholepath-2058/evidence/findings.json)
- [shell-dependencies.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-D137-shell-wholepath-2058/evidence/shell-dependencies.json)
- [validation.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-D137-shell-wholepath-2058/evidence/validation.md)

Commit message and `DONE` marker created.