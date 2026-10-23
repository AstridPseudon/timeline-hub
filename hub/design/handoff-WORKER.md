# A2 move-reads failover handoff

Worker `ap2-A2-move-reads-failover-0725` continued WIP `d9e0be239` in the App
worktree. The production parent move path carries the original planner basis
through `useClipDrag` and `useTimelineTrackManagement` into the existing D13
local-save handoff/outbox. The handoff declares `merge: fields`, selected clip
and consulted same-track timing fields, and the clip collection membership/order
read. A changed planner input omits the basis, preserving the existing atomic
fallback for unknown transforms.

Only three assertions were added to the already scoped handoff test. Targeted
Vitest passed 4 files / 82 tests; App TypeScript, seven-file ESLint, diff check,
normal Runtime producer lock, and exact private `819acf` graph checks passed.

This is App-side evidence only. No Runtime service/body, browser, journey, full
suite, or P1/body/whole-family qualification is claimed. Independent Luna review
is next; Undo remains on its separate branch.
