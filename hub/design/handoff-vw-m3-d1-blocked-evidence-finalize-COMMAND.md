# D09 blocked-evidence command record

This is a record of the prior worker's stopped preflight, not an instruction
to replay it.

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d1-public-positive-real-pinned-node
/home/user/work/venv-agent/bin/python -B "$W/run-integration-clean.py" --preflight \
  | tee "$W/preflight-local.log"
```

Recorded outcome: **exit 1**, refusal at the peer-graph guard
(`unexpected peer graph entries: 21565`). The real Node guard had already
passed. No `request-test`, central test, browser, full suite, install, or
network command belongs to this finalization.
