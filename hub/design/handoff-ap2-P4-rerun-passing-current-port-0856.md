# P4 rerun current integration port

PASS for the requested test-only source port.

Current base is `2e12b49ba61bc68a982a1cdc9d2d012036c9b720` /
tree `6f7649a4e0b8f1d936dc94a5fa0bb7c5fb3db276`, the newer reviewed
successor of `e837e18c5156e762eca05e6d9bb15779cf847b60` / tree
`405aca5e68dfc70fa0678b42207ab72908cce68f`. The only imported path is
`tests/editing_conformance/test_p4_note_rerun_v2_runtime.py`, byte-identical
to donor commit `f0847d8a304c731b215b69a4c023c4a65a902931` blob
`192efbfa14607f0edfb362d47d5238645c64e984`, SHA-256
`02ffa65700ff1c4d2e4a017fbaef6f646d100de5af61bc85e9003866eb927f36`.
The candidate final tree is
`39d050ea28b3f6c85915957a57470a8e1cad28d1`; the harness has not committed
it.

The target was absent at the current base, so no current file was overwritten.
Outside tracked files/blobs are unchanged; status reports only the target path.
The existing P4 service row was read-only and its row hash remained
`fafc5fa04275856881cb8188f782f00b73caf9492640a34369799738bd0af948`.

Checks passed: exact named collection (1), scoped Ruff, private-cache Mypy
(target plus ten-note neighbor), private-cache compilation, vendor-lock check,
diff check, exact Runtime object identity/origin guards for
`a5d4258312c979024865ee704da2d632ca5b2730` / tree
`f74b016ea837f8148db4a602c972073a226ed177`, and clean current Runtime
worktree inspection.

No live HTTP/body/socket/browser/service/full/build/request was run. The
named `/home/user/work/wt/rt-pin-a5d42583` checkout is absent locally, so
the exact Runtime pin was verified from the clean Runtime repository and a
private archive for origins; the existing service row was not executed or
mutated. Actual original-node behavior and manager/owner review remain
pending. Full v2 request/reply and production-caller behavior are preserved
by the exact reviewed test import but are not newly behaviorally claimed here.

