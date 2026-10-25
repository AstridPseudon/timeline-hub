# F-D87 coverage audit — PASS_SOURCE

Verified the exact handback against Agent HEAD `0d142f79518ba4ec20eb195657ccc7eb6e903fc3`.

- Exact mapping: 24 retained native-batch selectors + 1 separate checkout case; all replacement functions exist with assertions.
- Current capability gaps: 0.
- Six other checkout/frontend cases remain live.
- b9f remains unmerged; no native envelope, alias, or new format.
- Production old-route grep: no `commands-file`, `apply --native`, `publish_bundle`, or `three_way`.
- Evidence and exact SHA256s: [d87-coverage-review.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D87-coverage-review-0033/evidence/d87-coverage-review.md).
- Exact author artifacts consumed from hub: `handoff-agt-D87-0007-appendix.md`, `handoff-agt-D87-0007-source-acceptance.md`, and `handoff-agt-D87-retained-source-manifest.json`.

Checks:

- In-memory AST membership/assertion scan and compile: PASS.
- Scoped mypy: PASS, 7 files.
- Scoped Ruff: exit 1, 11 pre-existing `F811` diagnostics only.
- `git diff --check`: PASS; worktree clean.
- Pytest, collection, helpers, services, builds, browser/full suites: not run by instruction.

ZIP migration text returned exactly to the Runtime docs owner:

```text
### Timeline write-route migration

The delivery retires the native `edit commands-file`/native-batch ingress and
the other separate native/publish writers (`edit --native`, `apply --native`,
`undo --publication`, `publish`, `publish_bundle`, and the old three-way
writer). A document edit now uses `timelines commit --file ... --message ...
--idempotency-key ...`; the Runtime `commitTimeline` door owns accepted,
merged, conflict, and invalid replies, durable exact-key retry, and the
receipt/history. A single move or trim uses the current native `timelines edit
...` route. Cut-sheet edits use the current `timelines apply <sheet> ...` /
`NativeSheet` route, which emits registered commands through that same Runtime
door and preserves the draft on refusal. No native packet envelope,
commands-file alias, detached document overwrite, or resurrected G5 interface
is included.
```

`commit-msg` and `DONE` were created.