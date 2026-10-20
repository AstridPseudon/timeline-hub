## Report

Implemented the Agent view-write caller port:

- `WorkspaceClient.create_timeline_view` forwards explicit `idempotency_key`.
- Remote dispatch treats view creation as mutation, preserving retry keys and generating fresh keys for new requests.
- Added native SDK retry/refusal tests.
- Added [design handoff]( /home/user/work/wt/agt-m2-view-write-caller/docs/design/agent-view-write-caller.md) and [report]( /home/user/work/wt/agt-m2-view-write-caller/notes/report.md).

Tests:

- SDK targeted: 31 passed.
- CLI/public visualization: 26 passed.
- Idempotency regression: 2 passed.
- Named integration: 34 passed, 5 unrelated existing retired-shot-write failures.

Blocked: final Runtime F1/F2 union and generated-client pin are pending; live `/views` qualification remains unverified. Commit message and `DONE` marker created.