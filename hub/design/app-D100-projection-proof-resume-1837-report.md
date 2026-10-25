# D100 projection proof report

- ParentRED: **23 passed, 4 failed**. Failures were the expected pre-repair item-birth seam.
- CandidateGREEN: **24 passed, 3 failed**. First failure: `source_mapping` gained `_doc_patch_images`, violating custody preservation.
- Stopped immediately; no repair, retry, fixture receive, or App projection9/own9 run.
- Worktree remained clean; required hashes, JSON/XML evidence, and Runtime `ab1e4f61` custody verified.
- Capacity stayed above 5 GB throughout; no wait was needed.

Evidence: [facts.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D100-projection-proof-resume-1837/evidence/facts.json), [verdict.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D100-projection-proof-resume-1837/evidence/verdict.md).

Recommended next step: investigate `_doc_patch_images` mutation before rerunning the exact D100 gate.