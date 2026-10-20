Implemented the ordinary native-sheet subset: trim/source windows, explicit clears, scalar parameter edits, and occurrence fragments through existing capturers and Session batches.

Validation: **500 targeted tests passed locally; 12 central integration tests passed**, covering reload, undo/redo, exact retry after restart, disjoint rebase, and conflicts retaining the draft. Exact commands and results are in the [report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-sheet-native-ordinary/notes/report.md).

AG03/WC7 remains open. The [design](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-sheet-native-ordinary.md) names remaining legacy callers, unsupported grammar, and the stale first-apply CLI gap. No full suite ran; typechecking and global baseline checks remain non-green as documented.

`commit-msg` and `DONE` are written. Recommend reviewing this bounded port, then completing the remaining caller migrations before deletion.