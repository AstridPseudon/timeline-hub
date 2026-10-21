# Selected DEV one-case report

## Result

The one permitted central request was submitted with the frozen SOURCE worker
`ap2-m2-selected-existing-mount-precondition-source-0311` and completed as a
failure. It did not qualify the selected journey.

- Source argument: `ap2-m2-selected-existing-mount-precondition-source-0311`
- Approved source commit/tree: `b9a5ecd91d0235a9958af258e2cd5b1504687332` /
  `ec5791f3c0d05d3a6934d72a77f03da5a49ea94f`
- Exact command:
  `request-test ap2-m2-selected-existing-mount-precondition-source-0311 ap2-m2-selected-real-p1-history-fixture-fix --no-cache`
- Result ID: `ap2-m2-selected-existing-mount-precondition-source-0311-ap2-m2-selected-real-p1-history-fixture-fix-1021032129-25606`
- Result: `fail`, exit 1, 183 seconds
- Collection: exactly 1 test in 1 file; the hosted build passed.
- No retry or second request was made.

Pre-submission checks passed: the worktree was clean, `git diff --check`
passed, the frozen source contained one matching selected test declaration,
the central selected queue/process inventory was empty, and 17 GiB was free.
No local browser, socket, full suite, install, or second test request was run.

## Exact failure and reached scope

Startup itself passed: the existing `#root > *` mount precondition completed
within its 20-second budget. The selected fixture setup also completed: the
page displayed the `Selected PARAM` timeline and `selected-param-clip`, so the
initial draft/P1 setup did not fail before the test body.

The first failing assertion was the timeline-provider locator at
`tests/e2e/local/three-products.selected-param-dev.spec.ts:55`:

```text
getByTestId('video-editor-provider')
Expected data-timeline-id: 4a16a443-05a2-48b1-bdd6-4a0e211151cb
Timeout: 90000ms
Error: element(s) not found
```

The retained DOM showed the loaded editor, `Selected PARAM`, the selected
timeline clip, and the right panel, but no `video-editor-provider` test ID.
Therefore the run stopped before the first UI amount edit and before any
browser commit packet assertion.

| Scope | Actual result |
| --- | --- |
| Startup/mount precondition | Passed; existing `#root` observer and 20s budget were used. |
| Initial draft fixture | Reached/passed as setup; no pack ID was used for the initial draft path. |
| Initial native P1 fixture history | Reached/passed as setup; the fixture's exact native operation assertion is `clip.set-element` then `clip.set-params`. |
| First UI P1 edit, P1 schema/data/body | Not reached; provider locator failed first. |
| P2 admission and authored-source removal | Not reached. |
| Retained P1 after P2 | Not reached. |
| Refusal and dirty-draft preservation | Not reached. |
| Lost acknowledgement | Not reached. |
| Restart/reload recovery | Not reached; no `page.reload()` in the journey executed. |
| Exact retry body and idempotency key | Not reached. |
| Undo/inverse | Not reached. |
| Zero legacy traffic | Not asserted; no claim made. |

## Retained evidence

The central service retained the first failure evidence before cleanup:

- Result log and summary: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-selected-existing-mount-precondition-source-0311-ap2-m2-selected-real-p1-history-fixture-fix-1021032129-25606/log.txt`
- Driver stderr, Playwright error context, and trace ZIP:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/`
- No pending-module artifact was produced; this was a post-mount provider-selector failure, not a startup/module failure.

## Live callers and guards

- `tests/suites.conf:23` invokes the durable driver
  `workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh`.
- The driver collects the exact title with Playwright `--list` before the
  hosted build and then runs that same grep; collection reported one test.
- The sole selected test is
  `tests/e2e/local/three-products.selected-param-dev.spec.ts:33`.
- Its live setup caller is the worker-scoped `seedSelectedParamDev` fixture at
  line 10; its timeline-open caller is `openSeededTimeline` at line 54.
- No other selected central test was queued/running, and no selected driver or
  browser process was live before submission.

No product or test source changes were made in this worker. Ledger closure is
not warranted because the full P1/P2/recovery body did not pass.
