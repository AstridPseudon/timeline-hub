# Report: FAILsource

Classified both current failures as a live R2 Agent inverse/root-baseline defect, not a fixture mismatch.

- Forward source copy and exact replay pass.
- First inverse passes and empties the destination.
- Second inverse/redo fails with `original authored guard changed`.
- Passing single-shot inverse/redo and 53 neighboring controls show the repeated shared-shot topology is the unique trigger.
- Source owner: `astrid/sdk/timeline/inverse.py` and `astrid/sdk/timeline/_root_inverse.py`. The historical root-baseline guard uses plain `State`, while canonical physical placement rows contain managed `shot_revision_id` absent from the authenticated native authored guard.
- Runtime only surfaces the Agent provider refusal; it does not appear to own this current failure. Older Runtime1557/D17 evidence was not conflated.

No tests were rerun, per instruction not to retry refused actions. Authoritative controls: 53 passed, 2 failed. Read-only checks passed: `git diff --check`, JSON validation, and clean worktree.

Evidence: [source-cause.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-sourcecopy-whole-path-1650/source-cause.json)

No product/test changes were made. Commit message written, and `DONE` created.