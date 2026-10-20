Implemented WC6 native document publication.

- Added bounded pinned-base diff-to-command adapter.
- Replaced legacy `Writer.publish_parent_composition` / `publish_authoring_candidate` path with `TimelineSession` durable outbox commits.
- Added exact retry/idempotency guards and explicit holds for unsupported edits.
- Updated docs and preserved same-alias media positive as strict xfail.
- Wrote reports, commit message, and `DONE`.

Tests:

```text
148 passed, 1 deselected, 1 xfailed
Ruff: All checks passed
py_compile: passed
```

Reports: [design report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-wc6-document-script-native.md), [worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-wc6-document-script-native/notes/report.md).

Remaining gap: lossless native same-alias media replacement requires an Agent/Runtime command contract.