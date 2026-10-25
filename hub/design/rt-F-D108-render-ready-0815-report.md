## D108 render rehearsal report

Prepared a fail-closed rehearsal checker and receipt:

- Source manifest SHA verified: `37e559e6…a4504`
- All four durable patch hashes and applied trees verified.
- Exact D13/D77 selectors and route preserved.
- Tool hashes match; installed profile, seven-key bindings JSON, schema/site input, and Remotion `node_modules` are missing.
- Disk: 6,020,866,048 bytes free — D89 5.2 GB floor passes; old 8.5 GB floor fails.
- Result: `NOTRUN`; no service registered, renderer started, installer invoked, or ZIP published.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D108-render-ready-0815/evidence/`

Checks:

- Candidate compile: PASS
- Ruff: PASS
- `bash -n scripts/check-before-push`: PASS
- `git diff --check`: PASS
- `python -m pytest ... tests/test_release_native_smoke.py`: `1 passed`
- Poisoned manifest/wrapper controls: correctly refused with exit 2
- Full/browser/live render suites: not run

Worktree remained clean. Commit message and `DONE` marker written. Smallest blocker is the authentic D13 installed source profile plus its existing seven-key bindings carrier.