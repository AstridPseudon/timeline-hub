# P4 HTTP single readback handoff

Prepared in agent worktree `tl/ap2-P4-http-single-readback-0240`.

The sole product change is `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py`. It follows the reviewed P4 CLI/sheet front door through the existing Runtime fixture and normal generated transport, then checks the landed canonical closure and CLI show/history projections. It does not add a fake provider, alternate launcher, socket implementation, or acceptance shim.

Execution is intentionally deferred because this worktree has the pre-repair normal client. The compatible manager should import this test-only file onto the official G3/R2+normal adoption head and request the exact one-node targeted command recorded in `report.md`.

Source-closure seam: `initial_bundle()` omits the empty Runtime `occurrences` container. The test uses the trusted setup boundary to add that required canonical empty container, while asserting the original authored parent payload remains identical before the move. No alternate fixture or edited acceptance payload is used.
