# Original 0154 report truth correction

## Result

Corrected the original
[0154 report](ap2-m2-suite-child-exit-root-fix-0154-REPORT.md) in place. It
is now marked **CORRECTED / SUPERSEDED** so its old conditional-handoff claim
cannot be read as a solved historical cause.

The correction uses the exact [0218 historical causal diagnosis](ap2-m2-original-child-exit-causal-diagnosis-0218-REPORT.md): an injected child
exit of 7 propagated through the old wrapper and central runner as
`child 7 -> wrapper 7 -> central 7`. The historical 4657 first loss therefore
remains unknown because its per-run RC trace evidence was not retained. The
0154 immediate capture is described only as hardening and observability.

The original report also now preserves the actual 3198 evidence: the real
Playwright body was reached, child exit was 1, wrapper exit was 1, and the
central result was `status=fail`, `exit=1`. Its retained textual log remains
available; the trace and `error-context.md` files were deleted during cleanup.

The report links the existing [0226 corrective report](ap2-m2-exit-hardening-report-correction-0226-REPORT.md), the separate approved [0218 source/setup review](ap2-m2-normal014-source-setup-custody-review-0218-REPORT.md), and the separate approved [0202 synthetic custody review](ap2-m2-parent-synthetic-snapshot-custody-review-0202-REPORT.md). The owner-pending [0224 evidence-limit escalation](../escalations/app2-20261021T0224-historical-exit-evidence-limit.md) remains open.

## Exact paragraph diff

The causal paragraphs in the original report changed as follows:

```diff
-The old loss-prone handoff was the conditional `if flock ... Playwright; then
-... else ... fi`: the child was executed as a conditional command, with
-errexit suppressed, and its status was only handed onward through that
-conditional before verdict and cleanup. The new unconditional
-invocation/capture makes the exact handoff explicit. The common trap still
-receives and returns its incoming status; it was not changed to delete failure
-evidence. The retained historical 4657 directory has no wrapper trace, so it
-cannot distinguish whether that old handoff or the central finalizer performed
-the original swallow; the fresh negative proves the repaired suite path does
-not swallow it.
+The exact historical diagnosis is narrower. The old conditional handoff was
+reproduced with an injected child exit of 7, and the value propagated through
+the old wrapper and central runner: `child 7 -> wrapper 7 -> central 7`, with a
+failed status. Therefore the available evidence does not show that the old
+`if flock ...; then ... else ... fi` handoff caused the original 4657 loss,
+and it does not establish that 0154 repaired an identified historical
+overwrite. The first loss in historical 4657 remains unknown because the
+per-run child/wrapper/central RC trace evidence was not retained; its retained
+runner log was empty, and the disposable run root containing the trace and
+error-context files was deleted. The original 4657 result remains withdrawn.
```

The planted-negative paragraph was also corrected to state the exact retained
sequence and artifact boundary:

```diff
-`status=fail`, `exit=1`; the result summary reports `1 failed`. Thus the
-planted Playwright child, wrapper, and central result all returned nonzero.
-The log also shows the required summary guard refusing the absent real-case
-summary, as expected defense in depth.
+`status=fail`, `exit=1`; the result summary reports `1 failed`. The retained
+textual evidence therefore preserves the actual sequence: Playwright test body
+reached, child `1`, wrapper `1`, and central `status=fail`, `exit=1`. The log
+also shows the required summary guard refusing the absent real-case summary,
+as expected defense in depth.
+
+The retained textual log remains available. The trace and `error-context.md`
+files named by that log were deleted during cleanup and are unavailable; they
+must not be claimed as retained artifacts. This planted negative proves
+propagation for that current failure, not the historical first-loss location
+in 4657. It was not rerun for this correction.
```

## Scope

Documentation only. No code, helper, suite, result, caller, or historical
artifact was edited, and no new proof was added. No tests, browser, socket,
full suite, install, or negative rerun was performed.
