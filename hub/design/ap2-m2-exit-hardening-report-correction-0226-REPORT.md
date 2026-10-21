# App2 exit-fix0154 report correction

## Corrected conclusion

The 0154 report overstated what its wrapper change proved. Historical test
4657 remains **unknown-cause**. The exact old conditional handoff was
reproduced with an injected child exit of 7, and it preserved that value
through the wrapper and central runner: `child 7 -> wrapper 7 -> central 7`,
with a failed status. Therefore the evidence does not show that the old
`if/else` caused the original 4657 loss, and it does not establish that 0154
repaired an identified historical overwrite.

The 0154 immediate child-status capture is still a valid hardening and
observability improvement. It records the child result before verdict checks
and cleanup, making a future failure boundary visible. It must not be
described as the proven historical root fix. The historical-root requirement
is not complete; the 4657 result remains withdrawn.

## Preserved planted-failure evidence

The independent planted negative `3198` reached the real Playwright test
body and failed. Its retained textual central log records:

```text
Playwright child: 1
Wrapper: 1
Central result: status=fail, exit=1
```

This proves current failure propagation for the planted case. The trace and
`error-context.md` files named by that log were deleted during cleanup and
are unavailable. They are not retained evidence and must not be claimed as
such. The negative was not rerun for this correction.

## Separate scoped evidence

These approvals are independent of the historical exit-cause question:

- [Historical 4657 causal diagnosis](ap2-m2-original-child-exit-causal-diagnosis-0218-REPORT.md)
  records the exact old-path `7 -> 7 -> 7` reproduction and the missing
  historical child/wrapper evidence.
- [Source/setup custody review](ap2-m2-normal014-source-setup-custody-review-0218-REPORT.md)
  approves final95 source custody, Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`,
  and the `NORMAL014_USE_BASE_PYTHON=1` / base-Python import probes. That is
  a source/setup approval, not an exit-cause approval.
- [Synthetic ancestry custody review](ap2-m2-parent-synthetic-snapshot-custody-review-0202-REPORT.md)
  approves the synthetic ancestry guard and exact source/pin checks. That is
  a separate synthetic-source scope, not historical 4657 evidence.
- [Original 0154 report](ap2-m2-suite-child-exit-root-fix-0154-REPORT.md)
  is corrected by this document wherever it called the historical loss
  repaired or treated the 0154 change as an established historical root fix.

The owner-pending [0224 evidence-limit escalation](../escalations/app2-20261021T0224-historical-exit-evidence-limit.md)
remains open. No historical root requirement is declared complete.

## Live callers and changes

Live callers changed by this correction: **none**. The existing live wrapper
caller discussed by 0154 remains:

```sh
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=bootstrap \
  bash design/normal014-app-central.sh run "$PWD"
```

This correction changes no product code, helper, suite, caller, or historical
result. It is prose-only.

## Verification scope

No browser, socket, negative, full-suite, helper, suite, or historical-result
rerun was performed for this correction. The claims above are corrections to
the existing evidence record, not new test results.
