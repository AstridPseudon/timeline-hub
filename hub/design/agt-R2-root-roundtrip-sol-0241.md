**Blocked; do not integrate yet.** Six original redo failures are fixed. Selected-step absence now passes structural validation but fails in the separately owned timing validator.

Changed physical-root proof recovery, nested absence/order restoration, and optional-root validation. Preserved existing expectations and guards. Added repeated-cycle and damaged-proof tests.

Results:

- Original seven failures reproduced: **11 passed, 7 failed**.
- Exact 187-test cohort: **186 passed, 1 failed**.
- Seven new focused cases: **6 passed, 1 failed**.
- Ruff: **2,145**, exact parent identities and multiplicities.
- Mypy: **1,909**, exact parent identities and multiplicities.
- Artifact manifest, changed-file Ruff, and `git diff --check`: **pass**.
- Vendor checker withheld as instructed; `34eac004` pin unchanged.

Exact commands, logs, source hashes, and patch are in [qualification evidence](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-root-roundtrip-sol-0241/evidence/qualification.json), totaling **3.04 MB**. Base: `dfe105e13e`.

Both remaining failures reach [_commit_timing_validation.py:564](/home/user/work/wt/agt-R2-root-roundtrip-sol-0241/astrid/sdk/timeline/_commit_timing_validation.py:564). Required dependency hunk:

```diff
-    for clip in projection["parent"]["clips"]:
+    for clip in projection["parent"].get("clips", []):
```

That file is outside my assigned ownership; authorization was requested and remains pending. The proposed fix is unverified.

Wrote `commit-msg` and `BLOCKED`; no `DONE`. Next: assign or authorize the dependency hunk, rerun both cohorts, then perform independent cumulative source review.