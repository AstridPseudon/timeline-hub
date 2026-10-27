# H3 validation

- `bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/test-run` — **PASS**, exit 0.
- Read-only source check: Runtime suite command is the exact `runtime full` row in `tests/suites.conf`; the current runner and retained 14:13 pre-request backup both contain the Runtime `tl/one-head` Agent selector and command rewrite. The backup also passes `bash -n`.
- Read-only ref check: Agent `refs/heads/tl/one-head` and `/home/user/work/wt-int/agent-88a9dfe98563` both resolve to `88a9dfe9856344ade53d88d7dd4ec9883bd7a38c`.
- Read-only source check at Runtime `d3969a86e62f5f8761533499e7d2e3f97195932b`: bootstrap path prepends the selected root and clears foreign-root `astrid.*` modules; provider seam imports `astrid.sdk.timeline.commit` and invokes `create_runtime_commit_service`.
- Original request: `H-tests-runtime-final-full-1027154307-24227`, requested `2026-10-27T15:43:07Z`; Runtime tree `61568665d2c58da55d2082065dc8b1d4142b8632`; retained outcome **7,385 passed, 75 failed, 25 errors, 26 skipped, 13 xfailed**, status `fail`.
- Historical source limitation: retained runner errors at lines 470 and 477; summary was recovered from the test log and has no effective command; no per-process module-origin capture was found. The 88a9 provider identity is explicitly labeled source-backed inference.
- No full or targeted suite, test-service request, test body, socket, registry, install, kit, or product/source mutation was performed. Original proof was not retried or retargeted.
