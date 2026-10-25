# D120/P2 report

- Verdict: **PARTIAL-GO** for five authentic original PASS cases; overall tuple remains **NO-GO**.
- Verified: placement, ADD, parent move, single clear, bulk clear.
- Excluded at zero credit: SWAP FAIL, element FAIL/UNKNOWN, registerAsset NOTRUN.
- Confirmed exact pinned tuple, checkout receipts, manifests, XML counts/hashes, source/import roots, versions, C0 §§1–7 predicates, complete reload/history/nativeUndo tails, and no legacy writes.
- Source hashes were unchanged before/after; assigned worktree is clean.

Commands/results:

- `jq empty notes/partial-GO.json` — PASS
- `git diff --check` — PASS
- Tests, tsc, lint, browser/backend/HTTP reruns, full suite, and second body — **not run**, per readonly brief.

Outputs:

- `notes/partial-GO.json`
- `notes/partial-GO.md`
- `commit-msg`
- `DONE`

Recommended next step: manager publishes the byte-exact verdict artifacts; retain the overall NO-GO pending the excluded cases.