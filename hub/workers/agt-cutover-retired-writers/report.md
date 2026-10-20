Completed. All five failures began at `RemoteShots.create → create_project_shot`.

| Test area | Retired calls covered |
|---|---|
| Documented CLI mutations | create/add setup; reorder |
| Shot project scope | create/update/archive/recover |
| Editor reads/media relations | create setup; update/archive/recover |
| Candidate promotion | create/add setup; promote/replay/foreign candidate |
| Items and restart | create/add/reorder/remove/update/archive/recover |

Historical setup now uses trusted seeding. Retired writers assert the exact `retired_route` message, no receipt, and unchanged state. Catalog mutations remain positive tests with receipt, replay, and restart coverage. Five assertion mappings were added to [the deletion ledger](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/deletion-ledger.agent.md).

`_media` was removed in Runtime `2b7be58`; older `4c65c3e` provides it. This was private-fixture API skew. Replaced it with public `ingest` and migrated retired setup calls; all identity assertions remain unchanged. No repin needed.

Verification:

```bash
$ORCH/bin/request-test agt-cutover-retired-writers pin94114269-integration --files "tests/stage1/test_runtime_client_cutover.py"
$ORCH/bin/wait-test agt-cutover-retired-writers-pin94114269-integration-1020092719-30468 1
```

**46 passed**, including all four default modules: `--files` appends. Two intermediate runs had 45 passed/1 failed; both fixture defects were corrected.

```bash
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-94114269 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_commit_runtime_identity.py
```

**3 passed.** `git diff --check` passed; no new lint diagnostics. One pre-existing `F841` remains.

No blockers, skips, or xfails added. Full suite and proposal acceptance unverified. `commit-msg` and `DONE` written; ready for harness commit and integration review.