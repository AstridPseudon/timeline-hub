# F D141 final unit-notes installation review validation

Status: **FAIL_CUSTODY_LIMIT**.

- Read-only verifier: PASS for candidate/target equality, exact backup hashes, regular `0644` non-symlink checks, prefix conservation, AST inspection, and controlled function-only render; actual outside count `568`.
- Caller: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build` SHA-256 `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca`; one `render_readme` and one `main` definition found by AST; only `render_readme` invoked.
- Outside recomputation: PASS for 568 genuine paths and current equality against each retained map; genuine independent pre/post comparison: **UNOBSERVABLE** because the installer pre-mutation map was not durably retained.
- Review sampler: `3` durable samples at a five-second interval, minimum available bytes `5708038144`, four-gigabyte stop not reached, PID `9`, wait return code `0`, process reaped `True`.

Installer disk-monitor PID/exit/wait/reap facts: **UNOBSERVABLE** from retained installer artifacts; the separate review sampler lifecycle is recorded independently.

No product tests, type checks, lint, full suite, delivery-build main/CLI, build, rehearsal, clone, export, ZIP, source repair, or installation was run by this review.
