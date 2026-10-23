# Handoff — P4 physical-boundary oracle adaptation

## Disposition

Source review of the bounded Proof change is ready. The worktree starts at
`3696239c48f9705568af30f2704855cc6a9175e5`, tree
`94f7f4ff4d60a798d9cd664638a2b182234ad82c`; the final edited target-test blob
is `cdb186d001fe8bd7476c2a059ee65e9a312dbec5`.

The mistaken initial positive required equal WORKING `shot_id` aliases. The
adapted oracle now proves the C0c-equivalent stronger physical boundary:

1. The two authenticated canonical parent occurrences remain ordered and
   resolve exactly to the one physical `chapter-shot/shot-1`.
2. That shot resolves exactly to the one physical `chapter-1/internal-1`.
3. Media pins, reference edges, timing, source offsets, tracks, speed, opaque
   fields, payload digests, and complete dependency-manifest closure remain
   unchanged.
4. The two occurrence-specific WORKING aliases are distinct but each resolves
   through `source_mapping` to that same authenticated physical tuple. No
   identity or edge is guessed or rewritten.

The initial source fixture remains physically shared. The ten-note one-commit
case and its original step undo/redo, mirrors, full authored closure,
show/history, restart, request/response, conflict/invalid, and publisher
assertions were not changed. No product/helper/schema/generated/client/pin/
lock/launcher/suite/fixture/case/production-caller change was made.

## Evidence

- Exact one-test collection: PASS, 1 collected; only the existing unknown
  `timeout` configuration warning appeared.
- Target Ruff: PASS.
- Private mypy on the target plus `commit.py`, `commit_session.py`, `emitter.py`,
  and `sync.py`: PASS, no issues in 5 files.
- `git diff --check`: PASS.
- Offline actual `bundle_from_document` physical-mapping witness from the
  authentic canonical genesis: PASS.

No HTTP, socket, Runtime service, test-body, central service, full-suite,
browser, build, live readback, or inverse evidence was run.

## Known seam and next step

Independent review confirmed the separate Agent-owned reader bug: the remote
reader requests `internal-1` under parent timeline `film`, but the authenticated
internal image is owned by `chapter-1`; the frozen Runtime lookup requires the
exact owner. This handoff intentionally does not retarget the source or rewrite
the edge. After the owner-read fix lands, import only the current callable
source and run the original body on that reviewed source; do not merge whole
branch ancestry.
