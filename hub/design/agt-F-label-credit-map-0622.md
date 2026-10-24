## Report — PASS

Exact three original scenarios receive current behavior credit.

| Original | Current | Preserved predicates |
|---|---|---|
| `dispatch...[args0-画面 🎬]` | `apply...[args0-画面 🎬]` | capture golden, `pub1` receipt/publication, final Unicode label |
| `dispatch...[args1-]` | `apply...[args1-]` | capture golden, `pub1`, final empty label |
| `dispatch...[args2-None]` | `apply...[args2-None]` | seeded existing label, clear/remove capture, `pub1`, final absence |

Evidence:

- Original test SHA: `94f395...c1`; current SHA: `29d820f...cd2c`.
- Current AST contains exactly 3 target parameters and 11 total module cases.
- Retained [CLI0404 receipt](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/viewing-F-retired-callers-cli-0404.md>) reports the whole current module: **11 passed in 1.63s**.
- Its retained command was the targeted `pytest ... tests/packs/timeline/test_cli_native.py`; not rerun here.
- The test file is byte-identical between receipt source `8657e836` and current `9cd3dbe865`/`bb50a43c91`.
- Production path is `_cmd_apply` → `commit_edit(sheet=True)` → `NativeSheet.apply` → `TimelineSession.commit_many` → durable Runtime commit body. Source constructs API version, project/timeline scope, pinned revision/publication, commands, label, steps, merge, dry-run, source, and idempotency key.

Finite limits:

- Credit is for the migrated connected sheet/apply path only; no claim that the retired CLI parser still works.
- No live HTTP, actor, browser, full-family, or body rerun was performed.
- Exact target predicates do not independently prove every reply/history field (merged canonical records, effects, undo/history actor details).
- `design/commit-v2.md` and the runtime fallback were absent; PLAN §2 was used as the contract source.
- Integrated `71 + 5 + 53` counts were not used to infer target membership.

No repository files changed. Worktree is clean; commit message and `DONE` marker were created.