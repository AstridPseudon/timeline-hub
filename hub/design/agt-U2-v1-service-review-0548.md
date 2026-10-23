# U2 service review — PASS

Independent audit and bounded operational cleanup completed against `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`.

The prior `agt-U2-v1-suite-cleanup-0538` report was reviewed and remains accurate for its separate 0010/0012 cleanup. This review covered the two newly deleted graph directories:

- `/home/user/work/runtimes/agent-remotion-0013`
- `/home/user/work/runtimes/agent-remotion-f4ed-0013`

Both filesystem paths were absent, and no pytest/node process referenced either path. Exact path matching found and removed 19 complete command rows: 18 rows containing the 0013 graph and 1 row containing f4ed-0013. The dedicated removed suite keys were `agent-remotion-0013-nodes` and `agent-remotion-f4ed-0013-nodes`; the other 17 rows also contained the exact deleted paths and were in scope. No substring-prefix match was used. The two `agent-remotion-composition14-255b6856` rows remain.

## Config evidence

- Reconstructed before: 105367 bytes, SHA-256 `7bb3e9c67a2cafc37045f837e4e11014aedc65a17345ac7cd76a25c90b1e50ff`.
- After: 75765 bytes, SHA-256 `9eae6c782073ed3f42d4d5a93b4f7db8932d1b1eac74272b195ee9dad608144f`.
- Removed: 19 rows, 29602 bytes.
- Parser (`split(maxsplit=2)`): before 135 nonblank / 134 unique keys; after 116 nonblank / 115 unique keys. PASS.
- Protected outside-byte equality: PASS.
- Remaining exact deleted-path references: zero for both paths.

Exact removed rows are recorded in the worker report:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U2-v1-service-review-0548/report.md`

## Production caller review

Static inspection found the production chain wired through `Timeline.commit` (`astrid/sdk/timeline/commit_session.py:138-228`) → `TimelineSession.submit`/outbox guards (`astrid/sdk/timeline/sync.py`) → generated authenticated `commit_timeline` POST (`astrid_runtime_client/generated.py:963-965`). `astrid_runtime_client/timeline_commit_types.py:74-103` retains the full v2 request, accepted/merged/rebased, preview, conflict, invalid, canonical document, records/effects/steps/dependencies/history and undo metadata shapes. Import origins are recorded in the worker report.

No Agent product files changed; assigned worktree is clean. No old/full/browser/heavy/farm/native14/crash24/live-socket/product test suite was run, as required for this external-row-only task.
