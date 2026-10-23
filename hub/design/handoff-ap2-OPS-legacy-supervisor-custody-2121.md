## Result

Read-only custody audit completed for the exact seven registrations in `manifest.json:5-17`; protected current 1743 remained excluded.

### Supported route

`request-test` → pending queue → `dispatcher-daemon` → `test-run` → legacy `agent …-nodes` suite rows.

- `request-test:2-15`, SHA-256 `f839c002…`
- `dispatcher-daemon:2,8-20`, SHA-256 `f18bc20b…`
- `test-run:1-36,194-221`, SHA-256 `f599c5ad…`
- Target rows: `tests/suites.conf:162-168`, SHA-256 `b53dde12…`; protected row is 169.

`test-run` is the actual launcher/supervisor. Its managed path revalidates the suite row, acquires Store locks, passes inheritable lease FDs to descendants, supervises process groups, and removes transient running markers on completion (`test-run:53-164`). However, the current `/home/user/work/bench-store` root is absent, so these legacy rows use direct-child semantics (`test-run:94-100`, `194-205`) with no registration lease.

### Retained receipt facts

- All seven have retained Runtime creation receipts: `queue/done/runtime-agent-remotion-*`, each recording completed creation, source identity, env registration, and suite registration.
- All seven have retained retirement refusal receipts: `queue/refused/retire-venv-agent-remotion-*`, each refusing because the target remained referenced.
- No live operation, retry, deletion, marker change, queue request, or process inspection was performed.
- Existing independent review reports no exact target references in pending queue, active worker/request metadata, pending provisioning, replay/debug paths, or bounded lease markers. These are absence checks only, not historical execution records.

### Custody verdict

- Universal accounting of every pre-cutover run using the seven unmanaged registrations: **UNKNOWN**.
- Source/retained receipts prove a quiescent launch boundary for those historical runs: **UNKNOWN / not established**.
- `status`, `running`, `key.running`, and final `summary/exit` markers are transient per-test-run state; completed markers are removed. They cannot account for old runs absent from retained durable receipts.
- A newly acquired Store flock/current marker cannot prove an older unleased run was absent.
- No `/proc`, `ps`, `lsof`, asserted idle boolean, or broad process scan was used.

Smallest missing owned interface: durable per-registration launch custody, or a supported Store migration/adoption transaction that atomically binds each legacy registration to supervisor lease birth and launch admission. No broad process scan is prescribed.

### Checks

- Static syntax/metadata checks: **PASS** (`bash -n`, in-memory Python compilation, manifest JSON parse).
- `git diff --check`: **PASS**.
- Worktree status: clean; no source changes.
- Typecheck/lint/tests: **NOTRUN**, correctly scoped out because this was source-report-only.
- Required commit message and `DONE` marker written.