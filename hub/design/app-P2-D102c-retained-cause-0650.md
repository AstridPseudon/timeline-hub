# P2 D102c retained-cause report

Result: ADD retained a bounded Runtime diagnostic; ELEMENT did not.

- ADD: the inverse commit request reached Runtime and ended with HTTP 503. The private stderr sink contains one `runtime.timeline_commit.error` record with safe reason `catchall:builtins.KeyError`.
- The retained exception class/location fields were digest-reduced, so no sanitized source location is available. Provider duration was 3057.395 ms; dispatch duration was 3090.333 ms.
- ADD ring retention was active: 128-event rolling capacity plus a complete final-request record. Coordinator admission/lock and provider phases were retained.

- ELEMENT: phase capture was active, but the request ended during teardown. Provider start was retained; no provider end, HTTP response, receipt, or Runtime stderr line was retained. The App lifecycle artifact records page close with terminal state `pending` and UI still applying.
- Therefore the ELEMENT cause is `UNKNOWN`; the diagnostic disappeared at the App page/harness teardown seam before Runtime produced a response or emitter line.
- No separate Agent-side diagnostic record was retained.

Source correlation:

- Runtime publishes `503 / not_ready / details.reason=runtime_unavailable` from `timeline_commit_port.py`.
- Private diagnostics are emitted by `timeline_commit_execution.py`; service catch-all handling is in `service.py`.
- App decodes the public error into `ApiError`; save handling classifies 5xx as unknown/retry and does not expose Runtime stderr.
- Harness capture writes private stdout/stderr only during teardown after the Runtime closes.

Evidence:

- Focused retained-artifact JSON/count/correlation assertions: PASS.
- Exact source-hash assertions against the recorded ADD/ELEMENT source commits: PASS.
- ADD XML/readiness/stderr/stdout hashes matched the packet.
- ELEMENT XML/readiness/stderr matched; the recorded stdout hash did not match any retained result artifact, so it remains unverified.
- No full suites or product tests were rerun.

No product files changed; worktree is clean. `DONE` and `commit-msg` were created. Per harness policy, `report.md` and shared `design/` outputs are owned by the harness and were not written directly by this worker.