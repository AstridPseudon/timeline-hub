Implemented the bounded literal parent-media trim migration through shared capture, `TimelineSession`, and its durable outbox. Legacy families remain supported.

- Targeted pytest: **395 passed, 92 subtests passed**.
- Central `identity-pin94114269-integration --files tests/editing_conformance/test_cli_trim_runtime.py`: **5 passed**, covering reload, exact retry, dependent intent, rebase, conflict retention, and undo.
- No full suite, schema/pin changes, or private candidate.

[Report with exact commands, failures, and remaining writer paths](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-cli-ordinary-native/notes/report.md)

Commit message and `DONE` written. Occurrence trim and other ordinary families remain unqualified.