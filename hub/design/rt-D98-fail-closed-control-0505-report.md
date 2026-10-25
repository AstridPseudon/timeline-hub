## D98-control report

Implemented the private existing-route repair outside the Runtime worktree:

- Forwarded D98 activation variables in the launcher’s final clean body environment.
- Added fail-closed startup verification for observer hash, Runtime import origin/hash, binding, signature, activation witness, and process identity.
- Reused the approved observer/recursive adapter; no product, tests, schemas, pins, or dependencies changed.

Controls:

- Private/runtime compile + JSON parse: PASS
- `bash -n` launcher: PASS
- Positive `env -i` control: route/preflight/body `17/0/17`; `observer_active=1`, restored=`1`, control marker=`1`; original/stub body count `0`.
- Omitted activation poison: exit `1`, body count `0`.
- Wrong-hook poison: exit `1`, body exit `1`, body count `0`, no activation witness.
- Privacy scan: PASS; no raw payloads, credentials, URLs, or logs.
- No pytest, fixture, service, original body, retry, collector, or full suite run.

Hashes:

- Observer: `4f8c5929…4988fdc`
- Runtime auth source: `4ac2b879…cc0aeb`
- Private launcher: `c5277567…673c9d21d`

Proposed one-body command remains UNSUBMITTED for owner review. Evidence and receipt are under the worker’s private `evidence/` directory. Worktree is clean; `commit-msg` and `DONE` were created.