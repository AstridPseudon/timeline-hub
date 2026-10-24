## Result

Final counts:

`PRE-EXISTING / KNOWN GAP / ENV / NEW-OURS core / NEW-OURS non-core / REGRESSION = 16 / 135 / 54 / 326 / 0 / 0`

Separate: `KNOWN-P4=1`, `PENDING-18=18`; total `550`.

Lossless status pairs:

`FAIL/FAIL=16`, `FAIL/PASS=7`, `ERROR/PASS=11`, `FAIL/MISSING=285`, `ERROR/MISSING=231`.

Produced:

- [rehearsal-rollup.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-rehearsal-rollup-2311/evidence/rehearsal-rollup.json)
- [rehearsal-rollup.tsv](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-rehearsal-rollup-2311/evidence/rehearsal-rollup.tsv)
- [dispatch-clusters.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-rehearsal-rollup-2311/evidence/dispatch-clusters.json)

The dispatch file contains 57 exact family clusters with allowed test files and acceptance suggestions. Named reservations: `ProviderABI20` → Runtime peer2310; `occurrence-media48` → Agent2311. Other ready families include native-word-binding, native-batch-ingress, wc6 completion capture, parent-media, native-sheet, parent-auto-completion, parent-media-swap, selected-schema, commit-provider custody, recipe placement/unplace, document patch, and capture/projection fixtures.

Verification:

```text
python3 .../evidence/verify_rollup.py
PASS rollup-json-tsv assertions: rows=550 categories=16/135/54/326/0/0 separate=1/18
```

No product tests, lint, or broad audit were run per the analysis-only brief. Worktree is clean. Commit message and `DONE` marker were written.