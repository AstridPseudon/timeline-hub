## D30 report — P4 final service readiness

Prepared [tests/suites.conf.candidate](/home/user/work/wt/agt-P4-final-service-ready-1311/tests/suites.conf.candidate) for the current Agent source.

- Agent: `9b055a93ff15fce0a2e80f2647d47743b1fc4c33`, tree `ed0043b0570764fe17439830ca002db3fe358699`
- Runtime: `becfe6db88b2cc034dba3fafa6c050117cdf2b06`, tree `7edc08e3fe94edcbc8ef695c479f4de301789b89`
- Candidate SHA-256: `161d502f260dc1b49cacca1fa3f1b4f2caacce03ec606696b0e5e9f020b2557e`
- Historical receipts: single `28012`, ten-note `11615`, rerun `17739`; not reused as current pins.

Exact selectors:

1. `test_cli_sheet_v2_runtime_preserves_document_and_reads_back`
2. `test_http_ten_note_commit_per_step_inverse_and_redo`
3. `test_http_note_conflict_reruns_public_function_from_verified_peer_document`

Validation:

- `bash -n tests/suites.conf.candidate` — PASS
- Candidate serialization, selector membership, obsolete-pin scan — PASS
- Candidate diff check — PASS
- Source/module/profile preflight — PASS
- Pytest collection-only — **3 collected, exit 0**
- No test bodies, authenticated requests, full suites, installs, registry changes, or live service runs performed.

Existing environment is `/home/user/work/venv-agent`, Runtime `/home/user/work/runtime`, Node `v20.19.4`, and profile `/home/user/work/runtimes/agent-remotion-v3-819acf-1110`. Authentication is generated per local daemon by the existing fixture; no external credential source is required.

Current behavioral service result and durable XML/log for this exact tuple remain UNKNOWN until the manager queues the candidate. `DONE` and the required commit message are present.