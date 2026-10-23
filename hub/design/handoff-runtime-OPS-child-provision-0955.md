# Runtime handoff — OPS-child-provision bounded process-group correction

Result: the independent 1005 finding is corrected in a fresh candidate. Live
`make-child-venv` remains unchanged pending the next independent install
review.

Candidate: worker `rt-OPS-child-return-1006`

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-child-return-1006/evidence/candidate/make-child-venv
SHA-256 01bfbf9a17db0ae54e059a4badac5e1b13a8f6f52ae4b7e61c699f14b277f67f
mode 755
```

Failed predecessor retained:

```text
SHA-256 526e16145c3b014fb613618c27fe6d1a007857d769f31bfe5169ce423c71b52a
```

Live capture, rechecked:

```text
path /home/user/timeline-hub/hub/kit/bin/make-child-venv
SHA-256 ea4a1f53722ddd9f943b217021b6b4ed4828f34d10de76bae7ddc71fa470d6bc
mode 755, owner root:root
```

Exact diff from 526e16: remove `--foreground` from the existing overall and
stage GNU `timeout` calls; explanatory comments only otherwise. Default GNU
`timeout` process groups cover descendants and inherited dispatcher FIFO
stdout while retaining the existing finite overall/stage budgets and
`--kill-after` grace. Dispatcher/request/queue shapes and all product files
are unchanged.

Evidence report and scripts are in the candidate worker's `evidence/`:

- `report.md`
- `test_stubs.sh`
- `test_descendant.sh`

Checks passed: all three `bash -n` checks; retained offline success,
timeout, Runtime-failure, missing-import, immutable, and recovery stubs; and
the new real-GNU-timeout descendant/FIFO probe. The descendant probe returned
in 2 seconds, left no final environment or live descendant, and then ran a
following fake queue job successfully. ShellCheck was unavailable. No real
install, network, daemon, dispatcher, D09, full suite, or heavy graph was run.

Ready publication instruction after independent review only:

```text
install -m 755 <worker-evidence>/candidate/make-child-venv \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-child-venv
```

Agent0958 remains owner of the original installer/D09 and real private
Agent+Runtime environment. Original failure `20851` remains retained.
