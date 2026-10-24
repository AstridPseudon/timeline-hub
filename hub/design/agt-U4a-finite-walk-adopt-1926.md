## U4a report — PASS (provenance scope)

Updated only `runtime.lock.json` to Runtime `e89eb8c7dfa8…`.

Verified:

- Runtime clean, tree `19972951e704…`.
- Finite-walk source blob matches qualified `f51e2965…`: `fc3691c964…`.
- Canonical/schema/config hashes unchanged (`canonical15`, `schema867f`, `config4d74`).
- All tracked consumer hashes unchanged except the lock provenance line.

Commands passed:

- `refresh_runtime_client.py --producer /home/user/work/runtime`
- `vendor_lock.py check runtime.lock.json --producer /home/user/work/runtime`
- `artifact_manifest.py --check`
- `git diff --check`

No tests/full/browser suites run per task constraints. Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U4a-finite-walk-adopt-1926/evidence/`

Commit message and `DONE` marker written.