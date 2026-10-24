## Report

- Verified Agent HOME: `1f15f274…`, tree `1ac5f2d6…`.
- Verified Runtime pin: `1d9ddba…`, tree `f56c396c…`.
- Reviewed `e149` `store.py` and regression-test blobs match HOME exactly.
- Original test source, AST, body, and 22 predicates are unchanged versus `2007cf…` and prior `0557` branch.
- No product/test changes; worktree clean. `git diff --check` passed.

Exact mandated test, run once:

```text
1 passed in 6.34s
```

JUnit: [normal-publish-home.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-normal-publish-home-0640/evidence/normal-publish-home.xml)

Production path confirmed: `Checkout.publish → _commit_document → TimelineSession.open → resolve_ids → raw open_composition → normal commit → WorkspaceClient.commit_timeline`.

No installed-profile, HTTP/auth, or full reply-variant qualification was claimed. Commit message and `DONE` marker created.