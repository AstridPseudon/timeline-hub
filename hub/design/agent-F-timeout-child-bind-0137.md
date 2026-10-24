## Report

Added [tools/run-render-timeout-0137.sh](/home/user/work/wt/agt-F-timeout-child-bind-0137/tools/run-render-timeout-0137.sh).

- Receipt-gated lookup binds `venv-agent-child-render-current-0134` to bench entry `child-d12c6f…`.
- Verified current child validator SHA `361f759e…9686`; stale c886 is `90644c…b785`.
- Preserved original test/body hashes and 45-second timeout.
- Profile, Node 20, Runtime, imports, forbidden environment, and trivial support preflight all passed.
- Original test was not run; manager service owns it.

Commands:

- `bash -n tools/run-render-timeout-0137.sh` — PASS
- `git diff --check` — PASS
- `EXPECTED_SOURCE_TREE=fcd3135b3dc8e93009b86b7e4b75053a4e5b9476 tools/run-render-timeout-0137.sh preflight` — PASS, 0 failures

Exact suite row:

```text
test "$(git rev-parse HEAD^{tree})" = 3b9634548932220d34519a61140525705aa6fef1 && test "$(sha256sum tools/run-render-timeout-0137.sh | awk '{print $1}')" = 2ac1b958f4373fa860998155e50c8501c87191b813df599a1711ee1c139431bd && env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 EXPECTED_SOURCE_TREE=3b9634548932220d34519a61140525705aa6fef1 bash tools/run-render-timeout-0137.sh run
```

Commit message written; `DONE` created.