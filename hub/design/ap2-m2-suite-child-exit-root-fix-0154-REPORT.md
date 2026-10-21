# normal014 Playwright child-exit repair — CORRECTED / SUPERSEDED

> Correction notice: this report is corrected by the [0226 exit-hardening
> correction](ap2-m2-exit-hardening-report-correction-0226-REPORT.md).
> The 0154 wrapper change remains a hardening and observability change; it is
> not a proven repair of the historical 4657 loss. Do not read this report as
> declaring the historical root-cause requirement complete.

## Corrected result

The 0154 change made the App2-owned normal014 wrapper invoke Playwright and
capture its status immediately, before the structured verdict check and EXIT
cleanup. That is the smallest defensible hardening: it makes a future failure
boundary visible and preserves the captured child status for final reporting.

The exact historical diagnosis is narrower. The old conditional handoff was
reproduced with an injected child exit of 7, and the value propagated through
the old wrapper and central runner: `child 7 -> wrapper 7 -> central 7`, with a
failed status. Therefore the available evidence does not show that the old
`if flock ...; then ... else ... fi` handoff caused the original 4657 loss,
and it does not establish that 0154 repaired an identified historical
overwrite. The first loss in historical 4657 remains unknown because the
per-run child/wrapper/central RC trace evidence was not retained; its retained
runner log was empty, and the disposable run root containing the trace and
error-context files was deleted. The original 4657 result remains withdrawn.

The separate final95 source guard correction in
`normal014-source-common.sh` changed the stale Runtime SHA
`2c4ac180c2220bdad966bc01e95ad230e99ce26a` to the final95 lock's
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`. This was required so the
negative test reaches the planted spec rather than being refused by source
binding. This is source/setup evidence, not exit-cause evidence; it is covered
by the [approved source/setup review
0218](ap2-m2-normal014-source-setup-custody-review-0218-REPORT.md). The
synthetic ancestry/source custody checks are separately covered by the
[approved synthetic custody review
0202](ap2-m2-parent-synthetic-snapshot-custody-review-0202-REPORT.md).

## Preserved planted-failure evidence

Private spec:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-suite-child-exit-root-fix-0154/normal014-negative.spec.ts`

It throws from the Playwright test body. The wrapper copies it only into the
disposable overlay as `tests/e2e/local/three-products.spec.ts`; no checked-in
App source, real bootstrap case, or passed neighbor was modified or run. In
private mode the command also names that exact file, so the central run had
exactly one test:

```text
Running 1 test using 1 worker
normal014 planted failure reached Playwright test body
1 failed
normal014 Playwright child exit: 1
```

Central result:

`ap2-m2-bootstrap-current95-create-observer-cause-0115-normal014-integration-e2e-gate5-negative-single-1021021120-3198`

`status=fail`, `exit=1`; the result summary reports `1 failed`. The retained
textual evidence therefore preserves the actual sequence: Playwright test body
reached, child `1`, wrapper `1`, and central `status=fail`, `exit=1`. The log
also shows the required summary guard refusing the absent real-case summary,
as expected defense in depth.

The retained textual log remains available. The trace and `error-context.md`
files named by that log were deleted during cleanup and are unavailable; they
must not be claimed as retained artifacts. This planted negative proves
propagation for that current failure, not the historical first-loss location
in 4657. It was not rerun for this correction.

## Separate scopes and status

The [0218 historical causal diagnosis](ap2-m2-original-child-exit-causal-diagnosis-0218-REPORT.md)
records the exact old-path `7 -> 7 -> 7` reproduction and the missing
historical RC evidence. The [0226 correction](ap2-m2-exit-hardening-report-correction-0226-REPORT.md)
already records that 0154 must not be described as the proven historical root
fix; this original report is updated to carry that same correction at the
source of the old claim.

The owner-pending [0224 evidence-limit escalation](../escalations/app2-20261021T0224-historical-exit-evidence-limit.md)
remains open. No historical root requirement is declared complete.

This correction changes no code, helper, suite, caller, result, or historical
artifact, and adds no new proof. No browser, socket, full-suite, install, or
negative rerun was performed.

## Exact commands and checks

The exact registered normal command remains:

```sh
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=bootstrap \
  bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-app-central.sh run "$PWD"
```

The narrow registered negative command was run through the central service:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-bootstrap-current95-create-observer-cause-0115 \
  normal014-integration-e2e-gate5-negative-single)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
  ap2-m2-bootstrap-current95-create-observer-cause-0115-normal014-integration-e2e-gate5-negative-single-1021021120-3198 100
```

The central log passed the final95 locked graph/source/artifact checks and
hosted build before the one browser test. Shell syntax also passed:

```sh
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-app-central.sh \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh
```

No full suite, real bootstrap case, passed neighbor, local server/browser
run, `bin/test-run` change, product-code change, dependency install, or shared
dependency mutation was performed.

## Changed artifact hashes

```text
8f70ed7adafa42d90b3053f5972bd763a653ae690c1b2dfda352e3704615686e  design/normal014-app-central.sh
c76c48fa5f73b72ada6ba8fa857f229778e2ed6948568e77000bf4c1a8490270  design/normal014-source-common.sh
2c2c9be1d0fd3bc5ad6e85fda5bc19f7be88d9c7748363274acdce0668ad24bb  tests/suites.conf
10db990835b172c58a0d3a7a43ee8c00dead5b00cb6cc198ef8984edd9221b51  normal014-negative.spec.ts
```

The assigned App worktree is clean; orchestration files above are the only
changed artifacts. The historical 4657 false-green result was not edited or
relabeled. Any future historical-cause work remains subject to the owner-pending
evidence-limit escalation.
