## D40 Stage B report — FAIL / blocked pre-body

Ran the exact prescribed command once. It exited `1` before launching the installed child:

`RuntimeError: original identity changed: assertion_ast_sha256`

Direct `imported_from`: unavailable; original body was never invoked. Custody is incomplete; no JUnit, pytest, direct-observation, command, or custody-after artifacts were created.

Static checks passed:

- Runner SHA: `3cfefd6a…e5e1630`
- Child: Python 3.13.16, isolated `-I`
- Node: v20.19.4
- Relevant production files equal source 2007 and installed snapshot
- Worktree clean; no product/harness/test changes

Blocker: immutable baseline expects function AST `51b55e…bf5f` and source `e3980e…57db`, while the pinned runner computes `7a35b1…a3f9f` and `504e20…5002f` from identical source bytes. No retry or workaround was attempted.

Evidence: [runner-result.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D40-observed-original-0612/evidence/stage-b/runner-result.txt), observer SHA `3cfefd6a…e5e1630`.

The Runtime contract fallback was used because the Agent worktree lacks `design/commit-v2.md`. Next step: reconcile the immutable baseline identity scheme with the pinned runner, then rerun Stage B only as a new authorized attempt.