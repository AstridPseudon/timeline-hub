Implemented R2 in `_root_inverse.py` plus one new regression file. Accepted boundaries now normalize shared aliases before exact guard replay; recreated physical roots retain native creation semantics. No equality relaxation or revision-field stripping was added.

Validation—all exit 0:

- Both original repeated-source-copy selectors: **2 passed**.
- Fork guards, focused guards and neighboring history controls: **42 passed**.
- Source-authority, vendor and artifact controls: **35 passed**.
- Final focused regression: **8 passed**.
- Scoped Ruff, mypy and `git diff --check`: passed.

[Exact commands and durable evidence](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-sourcecopy-root-sol-1655/evidence/commands.txt>). [Protected-file hashes and loaded source identities](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-sourcecopy-root-sol-1655/evidence/identities.json>) confirm originals remain byte-identical and Runtime product source matches bc227.

The diagnosis narrowed to missing shared-root normalization plus an incompatible occurrence-local compiler baseline. Independent Luna core/security review: **PASS**.

Commit message and `DONE` written. No merge performed. Manager actual-home proof remains required before merge; no full suite was requested or run.