# Gate6 KEEP-pin command record — 0923

Packet root:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-pinned0d43-preflight-and-one-actual-0923/packet`

The required registered commands, not submitted because the complete path
prerequisite list failed, are exactly:

```sh
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-pinned0d43-preflight-and-one-actual-0923/packet/run.sh --preflight
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-pinned0d43-preflight-and-one-actual-0923/packet/run.sh
```

They are bare absolute Bash commands: no outer flock, `env`, or `bash -c`.
`run.sh` alone owns fd9. No `request-test` call was made. The local
preflight invocation was run from ORCH cwd and failed closed before central
submission because the exact source lacked `node_modules/tsx`.
