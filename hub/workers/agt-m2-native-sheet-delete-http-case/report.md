Implemented the missing Gate 1 HTTP proof in [test_native_sheet_current_runtime.py](/home/user/work/wt/agt-m2-native-sheet-delete-http-case/tests/editing_conformance/test_native_sheet_current_runtime.py:67).

- Added one real WorkspaceClient/Runtime/NativeSheet test covering stable-ref omission, persisted outbox retry, reload, opaque/order preservation, undo/redo, disjoint rebase, membership refusal, and target-change refusal.
- Tests: SDK neighbors `83 passed`; focused HTTP test `1 passed`; central `16 passed in 51.61s`.
- Design report: [agent-native-sheet-delete-http-case.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-native-sheet-delete-http-case.md)
- Commit message and `DONE` marker written.
- AG03 remains partial: detached legacy `apply_sheet` omission handling is still present.