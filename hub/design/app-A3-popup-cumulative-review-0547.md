## PASS — cumulative A3 review

Reviewed both author commits with no worktree edits:

- `03f98aafa7` — initial raw-track placement
- `fa59d33621` — mounted return and disabled-track refusal

Verified the production carrier:

`ShotTimelineMediaControls → useTimelineCommandsService → commands/media.ts → planner → A2 outbox`

Confirmed occupied V2 remains preserved, while missing, stale, wrong-kind, source, inactive, hidden, deleted, and disabled tracks refuse locally. Ordinary nearest-free/new-track planning remains unchanged.

Tests:

- Exact 8-file author selection, Node 22.22.0: **8 files, 180 passed**
- Same selection, Node 20.20.0 with existing navigator shim: **8 files, 180 passed**
- Node 20 without shim reproduced the known baseline `navigator` setup failure only.
- Serialized TypeScript checks for `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`: **passed**
- Changed-file ESLint (`--max-warnings 0`): **passed**
- `git diff --check`: **passed**
- Protected census: exact seven cumulative files; worktree clean.

No browser, backend, HTTP, service, install, or full suite run. Required commit message and `DONE` marker written. Recommended next step: merge this reviewed cumulative stack.