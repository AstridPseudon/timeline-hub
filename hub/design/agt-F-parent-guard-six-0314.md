## Result

All six cases share one Agent-side R1 defect:

| Selector | Input distinction | Projected guard |
|---|---|---|
| image-anchor | image birth; anchor-after; consumes `anchor` | `scope`, `ref=parent`, `path=[]` → public `dependency_changed` |
| image-fallback | image birth; fallback-at `22.25`; consumes none | same |
| image-lane-end | image birth; lane-end; consumes lane members | same |
| video-anchor | video birth with `from=0,to=2.5,speed=1`; anchor-after | same |
| video-fallback | same video fields; fallback-at `22.25` | same |
| video-lane-end | same video fields; lane-end | same |

The source trace is:

- [`_registry()`](/home/user/work/wt/agt-F-parent-guard-six-0314/astrid/sdk/timeline/native_occurrence_media_commands.py:110) reads `parent/collection:asset`.
- [`canonical_site()`](/home/user/work/wt/agt-F-parent-guard-six-0314/astrid/sdk/timeline/_commit_patch.py:100) falls back to the whole `parent` root.
- [`finish()`](/home/user/work/wt/agt-F-parent-guard-six-0314/astrid/sdk/timeline/_commit_patch.py:523) records that as a root scope dependency.
- [`rebase_patch()`](/home/user/work/wt/agt-F-parent-guard-six-0314/astrid/sdk/timeline/_commit_patch.py:921) therefore conflicts with the unrelated `parent/clip:anchor.params.later` write.

The smallest faithful correction scope is Agent R1’s `_commit_patch.py` asset-collection guard projection. Runtime, fixtures, command semantics, reservations, no-write behavior, retry, inverse, ABA, and assertions remain out of scope. This shares the file/merge queue with the earlier R1 atomic-scope repair, but is a distinct seam.

The captured failure stops before Runtime preview/accept. The exact narrow replacement encoding for the asset-map guard is not proven by the captured XML and should be decided by the R1 owner; no code change was made.

## Validation

- In-memory compile of four relevant Python files: PASS.
- Scoped Ruff on `_commit_patch.py`: PASS.
- Scoped mypy on `_commit_patch.py`: PASS.
- `git diff --check`: PASS.
- Worktree: clean.
- No pytest, fixture execution, service, reproduction, or full suite run, per SOURCE-ONLY constraints.

Commit message and `DONE` marker were written.