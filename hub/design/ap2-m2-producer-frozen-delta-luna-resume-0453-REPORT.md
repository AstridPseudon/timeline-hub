# Producer frozen-delta guard repair 0453

## Result

Completed the requested test-only repair. The only tracked change is
`check_approved_delta` in
`scripts/testing/run-producer-public13-list.sh`.

The guard now:

- requires the approved wrapper-bearing `APP_SOURCE_SHA` to be an ancestor
  of the current App HEAD;
- compares the tracked delta from `APP_SOURCE_SHA` to HEAD and permits only
  no change (the approved source itself) or the exact tracked wrapper path;
- therefore rejects a wrong base and any additional tracked file, while
  admitting reviewed wrapper-only successor commits.

The existing clean-state, body/helper/config byte, graph, source, runner,
alias, Chromium, assertion, timeout, zero-test, and child-return-code checks
were left unchanged. No self-referential final hash was added to the wrapper.

## Checks run

All were local static/probe checks only:

```sh
sh -n scripts/testing/run-producer-public13-list.sh
# PASS

git diff --check
# PASS

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-frozen-delta-luna-resume-0453/guard-probes.sh
# PASS: valid approved source and wrapper-only successor; wrong base;
# extra tracked file; body/helper/config drift; final HEAD/tree/wrapper hash
```

The probe uses mocked Git/hash responses for the guard cases and an external
identity check for the final keeper cases. It is not final service proof.

No build, browser, localhost/socket, actual, or full suite was run or
authorized.

## Final keeper command template

The harness must first commit this worktree. The manager/reviewer must then
read the exact resulting values and substitute them below; they must not be
embedded in the wrapper:

```sh
cd /home/user/work/wt/<final-keeper>
FINAL_APP_HEAD=<harness-final-commit-sha>
FINAL_APP_TREE=<harness-final-tree-sha>
FINAL_WRAPPER_SHA=<post-commit-wrapper-sha256>
test "$(git rev-parse HEAD)" = "$FINAL_APP_HEAD"
test "$(git show -s --format=%T HEAD)" = "$FINAL_APP_TREE"
test "$(sha256sum -- scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = "$FINAL_WRAPPER_SHA"
sh scripts/testing/run-producer-public13-list.sh "$PWD" preflight
```

Before harness commit, this worker's HEAD is
`7fafee1f67aa7b42e3997d2c30b4ee8e1bad42c5`; its HEAD tree is
`9d5ba429c703da57203e01d13e5a5fe4cc7ee014`. Those are not the final
post-repair identities. The worktree's current wrapper hash is
`b68e675e8ec06ae8566c90b7b59ef5b81803990e3d3d82169ecb4e5bffb7bf57`;
the manager must recompute it after the harness commit.

## Scope and handoff

Changed live callers: none. No product, schema, pin, DTO, store, or harness
redesign was made. The existing ignored dependency link remains
`node_modules -> /home/user/work/app/node_modules`, and shared dependencies
were not modified.

The remaining handoff step is the external final identity check above followed
by the separately authorized service preflight. No decision in PLAN.md was
changed.
