## D127 report

- Aggregated retained safe lifecycle data in [d127-aggregate.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D127-real-profile-1535/evidence/d127-aggregate.json).
- Exact element binding: request 3, hash `69c6463f…`, 352 samples, 3 lost, pending, no wall denominator.
- Kept distinct request 2 separate: 19,603 ms wall denominator, 11,840 ms Agent-provider interval, 60.4% provider share.
- Verified all three safe stack hashes and publication index. No raw stacks, payloads, keys, auth, or private URLs used.
- Runtime owner path: `door.py → server.py:_timeline_commit → service.py:commit_timeline → timeline_commit_execution.py → provider.commit`.
- Agent owns the measured provider interval, but no exact request-3 provider frame proves a specific optimization author.
- Native 1.75 s mismatch remains unexplained; history length/cold/reopen are not evidenced.

Checks:

```text
PY_COMPILE_IN_MEMORY_PASS
EVIDENCE_JSON_PASS
PUBLICATION_INDEX_JSON_PASS
SAFE_ARTIFACT_READ_PASS
WORKTREE_DIFF_CHECK_PASS
```

No tests or request bodies were run, per brief. Runtime worktree is clean. Commit message and `DONE` marker were written.