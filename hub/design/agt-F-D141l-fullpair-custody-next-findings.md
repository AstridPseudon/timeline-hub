# Findings

Verdict: `PASS_EVIDENCE` for custody association only; `qualification=NONE`, `REG credit=NONE`.

1. Cut `agent-agent-core-full-1026100428-24814` was requested at `2026-10-26T10:04:28Z`, dispatched at `2026-10-26T10:04:27.972946+00:00`, and ended native `fail/exit 1`. Pristine `agent-agent-core-full-1026103030-25513` was requested at `2026-10-26T10:30:30Z` and followed serially to native `fail/exit 1`. IDs come from retained service metadata.
2. The existing native binding inspector returned `artifact_checks=PASS` for both; request, returned ID/result directory, snapshot, summary, status/exit, raw/log, JUnit, command hashes, row readback, source tuple and custody seal all associate by plain artifacts. No mismatch occurred, so no withdrawal was needed.
3. Both command terminals report `state=FAIL`, `body_started=1`, runner exit 1, monitor/source/cleanup/evidence exits 0, and equal source-before/source-after bytes. KEEP and after-custody records remain.
4. Native and command traces cover admission, before/during/after phases and remain above the 4 GB stop. The one controller witness is `6479253504 >= 4714564096`; native admission floor is 4700000000.
5. The controller outer trace is retained but not qualified: its stat arithmetic emitted literal `available_bytes=UNREADABLE`. It is not used to infer a native sampler failure; real native traces and each manager trace remain distinct.
6. Cut declares `9561/201 failure/196 error/0 skipped` in `1525.081s`: 9388 concrete testcase IDs plus 173 aggregate unnamed subtests. Pristine declares `3255/20 failure/15 error/0 skipped` in `391.013s`: 3082 concrete IDs plus 173 aggregate unnamed subtests. No aggregate difference is called a loss.

The C0 commit-v2 contract is not exercised: this is the six-field test-service request. No new protocol, lease, guard, kit, interface, or product change was made.
