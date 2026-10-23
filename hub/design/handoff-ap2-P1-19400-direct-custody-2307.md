# Direct custody report — P1 run 19400

Verdict: **P1 remains NO-GO.**

- Fixed App `HEAD 5b6aae277…`, tree `7144f377…`; worktree clean.
- Protected case hashes PASS: first `4b04ad7e…ea8b7f`, second `2f750118…00a2f7`.
- Diagnostic artifact: **168246 bytes**, SHA256 `9aa108b2aa421cbf3fd0ac62555bb59d34e2619b5294e688c069d9e213ac6a3e`.
- Safe JSON parse, exact allowlist/schema, bounds, credential/unsafe-URL checks: **PASS**.
- Production serializer round-trip: **PASS**.
- Mounted production projection: **28/28 PASS**.
- Production path remains mounted App → durable outbox → Runtime commit route; no source or wire-shape changes.

Run attribution: actual qualified run was **169s, 1 PASS / 1 FAIL, exit 1**. The second trim POST, accepted Agent move, and Runtime `409` were reached. The primary assertion expected:

`config/clips/id:<rightId>/app/astrid`

but actual conflict path was:

`config/clips/id:<rightId>/at`

This is a primary assertion mismatch, not a diagnostic-serialization failure. Rollback/message/history assertions were unreached; eventual recovery is **UNKNOWN**. `CommandError` absent defaults do not establish absent operands. Historical 24510 `source-parent-mismatch` and 2218 reconstructed cause remain distinct and were not relabelled.

Commands/results:

- `git rev-parse HEAD HEAD^{tree}` — PASS
- `git diff --check` — PASS
- `git status --short` — clean
- `wc -c`/`sha256sum` on the diagnostic — PASS
- Read-only `node --experimental-strip-types --input-type=module -` schema/security/serializer audit — PASS
- No tests, browser, service, reproduction, or full suite run.

No repository files changed. Completion marker and commit message were recorded.