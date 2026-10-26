# Validation

Recorded fresh source-checker command:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -P /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/check-source.py check
```

Result: exit 0; `control_status=PASS`; `pair_status=READY_SOURCE_D141aa_NOT_RUN_LIVE`; 10 association, 38 lifecycle, and 10 native-admission-expression cases; tiny positive `exit=17 calls=1`; poison `exit=1 calls=0`. Fresh control log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/private-control-logs/check-1793008726782191470.json`.

Read-only actual binding inspections (both exited 0, `artifact_checks=PASS`, `admitted=false`, `test_status=fail`, `test_exit=1`):

```bash
/home/user/work/venv-agent/bin/python -P /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/binding-source.py inspect-result /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-agent-core-full-1026100428-24814 cut /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/command-cut.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/positive.manifest /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/source-manifest.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/private-control-logs/run-cut /home/user/work/wt/agt-F-D141l-fullpair-controller-next/evidence/pair/cut
/home/user/work/venv-agent/bin/python -P /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/binding-source.py inspect-result /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-agent-core-full-1026103030-25513 pristine /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/command-pristine.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/positive.manifest /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/source-manifest.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/private-control-logs/run-pristine /home/user/work/wt/agt-F-D141l-fullpair-controller-next/evidence/pair/pristine
```

Source-before/source-after compare equal for both. Settings are 22 cut roots / 17 pristine roots with the same venv, plugin profile, sanitized env, `-n3`, cleared addopts, no cache provider and timeout 45. No live request, install, test-run, wait-test, withdrawal, provider, collection, pytest or full-suite action was performed by this reviewer.

Own sampler: three 5-second `/home/user` observations at `7534993408`, `7534993408`, `7534981120` bytes; all above the 4000000000 stop. Retained in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-fullpair-custody-next/evidence/disk-trace.txt`.
