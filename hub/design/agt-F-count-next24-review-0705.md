## Verdict: FAIL

The candidate’s structural package is consistent, but current accounting is invalid.

- Verified five artifacts and hashes:
  - Census: `b7af85439f36b31c1603b162d331d9daea77dd2a2e44148f0ed369462fd59e8c`
  - Package: `2f74ecba4d5218e41fad670fa339059dac13fe448cb22dcfe902e716f6339481`
- Verified 267 unique `ours` records, 262 call / 5 setup.
- Exact delta: 24 nodes = 9 roots + 13 helpers + 2 schema.
- Preserved 243 other nodes, 38 prior proofs/coverage records, 94 prior mappings, and the complete contract inventory.
- Verified 118 unique CSV/JSON mapping rows, owner/family totals, report hashes, source/AST metadata, checksum, and package digest.
- Contract inventory preserves the complete v2 request/reply expectations and correctly limits proof claims; no HTTP/full/live-actor claim was inferred.

Blocking finding:

`test_restart_a_fresh_process_sees_every_edit_and_the_undo_history` remains `proven_passed` in the candidate, but Runtime’s current 0649 run failed before draft with `_FakeTimelines` missing `history`. The candidate’s seven open IDs omit this node and contain no challenged/open disposition for it. The failure must be explicitly accounted for; historical qualification is insufficient. The separate `test_two_writers_in_separate_processes_merge_different_clips_and_refuse_the_same_param` is already open and remains so.

No product edits or tests were run; only standalone stdlib verification was performed. Worktree is clean. Commit message and `DONE` marker were created. Recommended next step: reopen and reconcile the failed restart original on this same candidate before republishing counts.