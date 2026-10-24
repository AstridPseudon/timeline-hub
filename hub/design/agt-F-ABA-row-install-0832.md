## F-ABA-row-install-0832

Installed exactly one reviewed row into `/tmp/.../orch/tests/suites.conf`:

- Suite: `authoring-current-becfe-nodes`
- Candidate SHA-256: `f7bd322a…de31`
- Registry: 172 → 173 rows
- Pre/post SHA-256: `afd6…d9bc` → `83ff…02d27`
- Outside-byte identity: PASS
- Regular mode-600, non-symlink: PASS
- Candidate/source guards and service command preserved exactly.

Validation passed:

- `bash -n` candidate, registry, and `request-test`
- Serialization and named `*-nodes --files` enforcement checks
- `git diff --check`
- Final worktree clean

No row, original test, pytest, preflight, body, child, browser, full, or gate execution was performed. Commit message and `DONE` marker are prepared.