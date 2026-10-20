Implemented and qualified.

- Retired legacy timeline flat-version recover forwarding; it now visibly refuses with `timeline.restore` guidance and never maps version IDs to revisions.
- Added draft-preserving `TimelineSession.restore(revision_id, content_digest)`.
- Removed Agent SDK compatibility forwarding while preserving project catalog archive behavior.
- Updated CLI/docs, tests, AG-RECOVER ledger, and owner-film differences.

Tests:

- `pytest ...test_timeline_sync.py ...test_native_timeline_facades.py ...test_domain_cli_projects_timelines.py`: 187 passed, 1 skipped.
- Central `commit-integration` public HTTP lane: 12 passed.
- `git diff --check`: passed.

Remaining raw generated vendor symbol: `astrid_runtime_client/generated.py:978`; no Agent callers remain, and it is generated (“do not edit by hand”).

Commit message: `.../workers/agt-m2-recover-native-retirement/commit-msg`  
Completion marker created: `.../workers/agt-m2-recover-native-retirement/DONE`