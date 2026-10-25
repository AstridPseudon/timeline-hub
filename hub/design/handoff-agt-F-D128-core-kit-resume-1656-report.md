## D128 report — blocked

- Verified installed maker: SHA-256 `0857a5e0…e57b6d39`, mode `0755`; independent review/install receipts passed.
- Verified frozen four-repo tuple, custody, profile, protected hashes, and free space.
- Submitted exactly one normal child request: `venv-agent-child-custody-a4e016`.
- Terminal refusal: `maker provision report differs from authenticated installed inventory`.
- No child key, manifest, preflight, suite edit, service ID, or full-body submission. Existing layout remains `UNVERIFIED / EXACTMISSING`.

Validation:

- JSON evidence parsing: PASS
- `git diff --check`: PASS
- Published maker receipt controls (`bash -n`, 29 unittest controls, Ruff): PASS
- Worktree: clean

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D128-core-kit-resume-1656/evidence/`

Recommended next step: Runtime owner resolves the normal maker report mismatch; do not retry or bypass this refusal.