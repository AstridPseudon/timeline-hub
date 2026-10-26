# D141l same-ID pristine receipt completion

Result: PASS for the existing `timeline.d89d.measured-floor.v1` data attachment.
The original request remains queued and no body was dispatched.

Exact unchanged read-only validator command:

```text
python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/d141-validate-receipt.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-d822d2f5-full-1026063854-17524/recorded-measured-floor.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch app-pin-d822d2f5-full-1026063854-17524 app full /home/user/work/wt/app-pin-d822d2f5 d822d2f5d2bd05187b4ff5b6071c3e13945d4747 2af40a015057779ceb4e4b37cad62e1469aa7e36 'npm test -- --maxWorkers=3'
```

Observed stdout: `4793895424`  
Observed exit: `0`  
Validator SHA-256: `2987adbcd888400a41afbbd60e22ea2e4afe6c4580b084a4d63dcced6943a7f6`

The receipt binds the genuine pristine source HEAD
`d822d2f5d2bd05187b4ff5b6071c3e13945d4747`, tree
`2af40a015057779ceb4e4b37cad62e1469aa7e36`, normal registered command,
and existing normalized DATA witnesses. The arithmetic is:

```text
growth = 5433016320 - 4839120896 = 593895424
floor = max(4600000000, 4000000000 + 593895424 + 200000000)
      = 4793895424
```

The normalized witness files are derived DATA projections, not original stdout;
their provenance and hashes are unchanged. No new witness, observation, request,
body, queue edit, direct run, admission claim, or floor bypass was made.

At `2026-10-26T06:53:53.474Z`, current free space was `4699176960` bytes, so
the actual service remains queued pending independently meeting the measured
floor. The service's existing queue `why` record was preserved.
