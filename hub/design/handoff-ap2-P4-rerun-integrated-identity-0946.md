# P4 integrated conflict/function-rerun readiness handoff

SOURCE_READY: PASS. OPS_READY: PASS for the existing route, pending one manager-owned body run.

Exact integrated Agent identity:
- HEAD 543d133c85de16ab800c4df0e9ff504ca077fcbf
- tree f6cda3a2956ca702721ad3c1ba79c20932e1506a
- owner test commit de046064f1632eef96bf08289f50a6ec3fefe4a3, merged by the above head
- target blob 192efbfa14607f0edfb362d47d5238645c64e984
- target SHA-256 02ffa65700ff1c4d2e4a017fbaef6f646d100de5af61bc85e9003866eb927f36

Exact Runtime identity and cleanliness:
- checkout /home/user/work/wt/rt-pin-a5d42583
- HEAD a5d4258312c979024865ee704da2d632ca5b2730
- tree f74b016ea837f8148db4a602c972073a226ed177
- clean worktree; expected .venv/bin/python symlink convention present
- runtime module origins resolve inside this checkout; Agent generated/client/SDK origins resolve inside the exact worker
- normal vendored client remains 34eac0041b0891e9011966b39bcbd26053fde5bc; retained d106/reader168/hydration e49/R1 b8 source evidence is unchanged

Existing agent p4-v2-http-nodes row was read only and remains exact:
- row SHA-256 fafc5fa04275856881cb8188f782f00b73caf9492640a34369799738bd0af948
- whole config SHA-256 e7f44d0920291c27ef4b790b00de8b1d514a27e28ccfef839b0b45fdb3537d55

Bounded checks all passed: selector collect-only 1 collected; Ruff; private-cache Mypy target plus ten-note neighbor; private py_compile target plus ten-note neighbor; vendor-lock check; eight P4-related imports; exact origin guards; git diff --check; clean status. No live service/body run was made and no request ID exists yet.

Manager’s one allowed next request, against this worker only:
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-P4-rerun-integrated-identity-0946 p4-v2-http-nodes --files "tests/editing_conformance/test_p4_note_rerun_v2_runtime.py::test_http_note_conflict_reruns_public_function_from_verified_peer_document")
echo "$R"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"

Record R immediately. Do not rerun an older selector, use stale integration:agent, or dispatch a duplicate Agent HTTP node. No body credit is assigned before this result.
