# Validation

Review subject: `agt-F-D141l-binding-final-next` exact final-next evidence source.

The subject packet records the author and one independent run of the identical command:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -P /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/check-source.py check
```

Both recorded runs exited 0 with `control_status=PASS` and
`pair_status=READY_SOURCE_D141aa_NOT_RUN_LIVE`; each reported 10 association,
38 lifecycle, and 10 native-admission-expression cases. The unchanged launcher
controls reported positive exit 17/call 1 and Agent-SHA-only poison exit 1/call 0.

My non-mutating checks against the exact subject source also passed:

```bash
bash -n controller-continuation.sh command-cut.sh command-pristine.sh tiny-controls.sh positive-stub.sh
```

Result: exit 0.

```bash
/home/user/work/venv-agent/bin/python -P -c '<ast.parse all subject Python; json.loads all subject JSON>'
```

Result: exit 0. `controller-continuation.sh check`, `binding-source.py
dispatch-readiness`, and `binding-source.py dispatch-witness 4714564096` each
exited 0. Subject source hashes, owner-brief byte equality, product/pristine
tuples, and the 4,714,564,096-byte controller witness were read back.

No product lint/typecheck applies: this is an operational shell/Python source
review, not product code. No live CAS, row install, request-test, test-run,
wait-test, withdrawal, provider, body, collection, pytest, full suite, or
shared dependency action was run. Live native results, REG evidence, and product
qualification remain prospective and unverified.

The subject checker was not invoked a third time from this reviewer worktree
because its hard-coded `ROOT` writes private control logs under the retired
subject worker directory, outside this worker’s write scope. The recorded exact
author and independent runs are retained and were independently inspected.

Review trace: five samples at five-second cadence, all above the 4,000,000,000
byte stop; minimum 4,616,032,256 bytes. No trace gap occurred in this review.
