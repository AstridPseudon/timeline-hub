I couldn't do the pin because there is no Runtime checkout at `94114269d1ce23ab3224d7eca5a85138ce2b5fed`. I wrote the reason to `BLOCKED` and did not create `DONE`. Nothing in the Agent worktree has changed, and no commit message was written.

`vendor_lock.py update` refuses to run unless the producer checkout's HEAD equals the pinned `source_commit`. The checkouts I found don't match:
- `/home/user/work/runtime` is at `6023cfb`. `94114269` is an ancestor of it.
- The `rt-*` worktrees under `/home/user/work/wt` are at other SHAs.

My workaround failed. I cloned the Runtime repo into my scratchpad and tried to check out `94114269` there. The sandbox denied the checkout. That clone is still at `/tmp/claude-0/-home-user-work-wt-agt-m2-runtime-pin-current/312ea938-9703-423a-9494-2e62c845537a/scratchpad/rt`, with nothing checked out. `rm-own` refused to delete it because it sits outside my worktree.

To unblock me, please do one of these:
- Create a detached worktree at `94114269d1ce23ab3224d7eca5a85138ce2b5fed`, for example `/home/user/work/wt/rt-pin-94114269`.
- Allow `git checkout --detach 94114269d1ce23ab3224d7eca5a85138ce2b5fed` in my scratch clone above.

Once that exists I'll continue with the plan:
1. Run `vendor_lock.py update` with that checkout as the producer.
2. Derive the schema digest in `test_commit_runtime_m1.py` from the pinned contract metadata instead of a literal.
3. List the Agent edit ops that are missing from Runtime's 14-op registry, checking `agent-edit-schema-delta-for-runtime.md`.
4. List the conflicts with `tl/vw-m3-agent-consume12`.
5. Run the targeted commit-integration tests and write the commit message.
