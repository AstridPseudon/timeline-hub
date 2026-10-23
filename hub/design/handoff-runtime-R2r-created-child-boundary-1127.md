# Runtime handoff: R2r created-child authenticated native alias boundary

Status: **PASS**

Runtime owned the observed failure. Current Agent capture produced an authenticated `occurrence.create` birth followed by child commands, but Runtime evaluated the child alias/source reads against the pre-birth boundary. The previous behavior rejected the legitimate sequential capture as an occurrence alias outside its boundary.

The Runtime-only repair in `runtime_protocol/timeline_commit_auth.py` now builds a bounded intermediate closure from the current record's absent-to-present shot and parent-owned occurrence roots. It uses the exact Agent authoring identity inputs confirmed by the source witness, carries only the birth payloads, and validates subsequent reads/effects against each command's sequential input. Final accepted closure data is used only to prove the exact physical allocation and managed edge shape; it is not used to import future child payloads.

Focused coverage was added in `tests/test_timeline_commit_authentication.py` for a created child read, future-payload isolation, and foreign-alias refusal. Existing public Runtime tests remain unchanged and pass.

Durable complete native witness: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-created-child-boundary-1127/evidence/native-sequential-create-child.json`.

Validation: Runtime targeted suite **217 passed**; source/document/raw suite **22 passed**; Ruff passed; Pyright reported zero diagnostics; AST and diff checks passed. A separate direct native positive using current Agent capture and Runtime boundary handoff passed with actual source/accepted digests. The public hosted service/provider/store full-v2 journey was not run in this worker and remains a central integration-review item.
