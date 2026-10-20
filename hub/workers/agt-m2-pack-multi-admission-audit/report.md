## Result

Found a real multi-admission preservation gap.

- Current `b2b51c4a`: rejects B-only re-admission because the whole-pack closure changed, while preserving A’s old document/snapshot bytes.
- Untouched M1: admits but duplicates A’s `(id, kind, revision)`; resolving old A then fails. The one-element metadata-only case has the same duplicate-identity bug.
- A candidate retaining A’s old snapshot and adding B’s new full-pack snapshot resolved losslessly with unique identities.

Tests:

```text
/home/user/work/venv-agent/bin/python -m pytest -q \
  tests/core/test_project_packs.py \
  tests/core/test_project_pack_snapshots.py \
  tests/core/test_project_pack_inputs.py
83 passed in 24.27s
```

No full suite, install, network, Runtime pair, browser, merge, or product changes were performed. Worktree remains clean.

Reports and messages:

- [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-pack-multi-admission-audit/notes/report.md)
- [runtime-coordination.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-coordination.md)
- [commit-msg](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-pack-multi-admission-audit/commit-msg)
- [commit-msg.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-pack-multi-admission-audit/commit-msg.txt)