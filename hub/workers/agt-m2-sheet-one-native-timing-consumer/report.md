## Completed

- Enabled connected NativeSheet `timing.for.card` edits on cut-owned rows using existing `clip.set`.
- Preserved original refs, `app.cut`, `app.for`, inverse, rebase, commit, and undo behavior.
- Confirmed nudge-seconds is already covered; nudge-frames requires unsupported word-relative semantics.
- Added design report: [agent-sheet-native-timing-consumer.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-sheet-native-timing-consumer.md)

## Tests

- Native sheet neighbors: **102 passed**
- Scalar/provider neighbors: **110 passed**
- Three legacy timing scenarios: **9 passed, 139 deselected**
- `git diff --check`: passed

No full suite or HTTP tests run.

AG03 remains partial because the no-client `apply_sheet` / `_apply_parsed` / `merge_sheet` legacy path still serves unsupported Main-positive grammar.

Commit message and `DONE` marker written.