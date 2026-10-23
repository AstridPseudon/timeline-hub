# Runtime handoff: OPS-retire-process final review 1837

## FAIL — permission-denial stop rule is not met

The exact self-contained HOST command is retained verbatim in
`handoff-runtime-OPS-retire-process-return-1832.md` under its first `sh`
fence. Its extracted Python body is 8,449 bytes and hashes to:

`582405d5d6478e80560a35bb2cb523adae7b7a80e7dda4a068449ece69b2ff69`

The complete embedded command bytes are 8,470 bytes and hash to:

`31e5ccf86d13c40ed5df10f9ea1b38fe9803412455ab5a95b524a44955fe2c51`

The installed source inspected is unchanged and matches the requested
durable identities:

- handler `retire-child-venv`: `954d5d87fe2e6fcf42b34953ec0edc519a2eb97ade8f66f0f2f96f523516b791`
- request `request-retire-venv`: `21f61833a6718794ab2a06a3a96d34ca58c050ccd0151622e16866ac78758139`

The command correctly exercises the private empty-cmdline/ENOENT branch
(exit 0, `approved-empty-cmdline-exe-failure`), non-empty/ENOENT branch
(exit 2, `executable-unreadable`), hidden proc root (exit 3), and readable
non-user executable (exit 0, no failing observation). Output allowlist and
secret-sentinel checks passed. No cmdline, executable path, argument,
credential, or mountinfo payload was emitted.

### Finding

`namespace_summary.probe()` returns `(yes, denied)` for a permission-denied
`mountinfo` or PID-namespace read, but the caller continues to emit the
namespace line and scan PIDs. A private exact-command run with only the
`mountinfo` open denied produced `mountinfo_readable=denied` and then scanned
a later PID, ending with exit 4 (`pid-vanished`, `unknown-race`). This
violates the settled requirement that permission denial stop and report
without alternate probing. The command must not be exported to App2 HOST
until corrected and independently reviewed.

### Checks

- exact embedded script extraction/hash: PASS, stated hash matched;
- private fixture branches and output allowlist/secret sentinels: PASS;
- scoped Python compile of extracted script: exit 0;
- `bash -n` handler: exit 0;
- `bash -n` request: exit 0;
- `git diff --check`: exit 0;
- Runtime status clean: exit 0;
- actual HOST `/proc` or remote command: **UNRUN**;
- queue, retirement, retry, daemon, provision, install, target, guard, and
  deletion policy: untouched.

Remote App2 cause therefore remains unqualified. No original command/script
design export or remote execution is authorized on this FAIL result.
