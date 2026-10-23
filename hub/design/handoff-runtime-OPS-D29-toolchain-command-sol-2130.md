Changed only `ops-handoff/remotion-toolchain-manifest.json`: one line, restoring the lock operand’s missing final `d`. All other metadata, reviewed code, and recorded 14-case proof remain unchanged.

Validation:

- `python3 "$TMPDIR/verify-d29-command.py"` — PASS: JSON, exactly eight operands, pinned lock blob, all artifact hashes, private strict requester accepts corrected payload and rejects old 63-character digest.
- `git diff --stat` — one manifest, one insertion/one deletion.
- `git diff --check` — PASS.

Final manifest: **2,957 bytes**, SHA-256 `f49732687dea629f283e9f566ce13eb01e08c2a260822bef70ec033ed94d2146`.

Lock input: **151,418 bytes**, SHA-256 `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`.

Exact valid command:

```bash
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-runtime agent-remotion-app-p3-079-2a9-2110 079580ca46af77e0292d49dc34386b25c8391f99 f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d /home/user/work/wt/agt-pin-079580ca /home/user/work/wt/rt-pin-2a9e347f 2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d remotion-env-nodes /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin
```

Queued payload SHA-256: `0642e4d64fd68b39a8fb2f63280616c108282a95b084932b80a4688afd32ec5d`.

No blockers or decision deviations. Named source worktrees are absent here; pinned Git objects were verified. Production was never queued. Commit message and `DONE` written. Ready for package review; artifact remains **never merge Runtime**.