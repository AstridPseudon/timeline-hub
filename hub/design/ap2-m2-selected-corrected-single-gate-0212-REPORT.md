# AP2 M2 selected corrected DEV single-gate report

## Result

The one authorized central selected DEV run was submitted only after the exact
independent readiness review approved commit `a0a73dae3303bf5174267fcb53f3fe8ae3cbc426`,
tree `2fc6328ed0ea1ecba55269be6f976354406035f`. It failed at the first real
readiness assertion. No retry, repair, second run, or local browser/socket run
was performed.

Central result:

- Test ID: `ap2-m2-selected-corrected-single-gate-0212-ap2-m2-selected-real-p1-history-fixture-fix-1021021417-20336`
- Suite: `ap2-m2-selected-real-p1-history-fixture-fix`
- Frozen tuple: Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime
  `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, public13 locked graph,
  all75/all77 Composition pair
- App tree: `2fc6328ed0ea1ecba55269be6f976354406035f2`
- Outcome: exit 1, 1 test failed, 98 seconds

## First failure and preserved evidence

The first assertion was the unchanged existing helper boundary:

```text
expect(page.getByRole('combobox', { name: 'Select project' }))
  .toContainText('Direct Journey 5ffc32')
```

It timed out after 5 seconds because the `Select project` combobox was not
present. The hosted page navigation itself returned HTTP 200. The preserved
Playwright network trace contains no Runtime-door `/v1` request before this
assertion, so there is no selected P1 request/response, commit response,
refusal, lost acknowledgement, retry, restart, undo, or zero-legacy traffic
evidence to classify. This is a central App readiness/boot-surface failure,
not evidence against the selected writer or Runtime contract.

Preserved trace:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/`

The central result log and snapshot remain under the corresponding test-result
directory in `scratchpad/orch/tests/`.

## Scope and callers

The approved correction changed only
`tests/e2e/local/three-products.selected-param-dev.spec.ts`; no production
code, helper, or live caller was changed by this worker. The existing selected
driver and all original P1/P2/source-removal/refusal/draft/lost-ACK/restart/
exact-retry/undo/zeroLegacy assertions remain in the source, but were not
reached by this failed run.

The selected-writer merge `db8` is not qualified by this result, and bounded
ledger closure is not warranted. The selected writer remains open pending a
separately authorized readiness repair and review.

## Exact test command

```text
request-test ap2-m2-selected-corrected-single-gate-0212 ap2-m2-selected-real-p1-history-fixture-fix --no-cache
wait-test ap2-m2-selected-corrected-single-gate-0212-ap2-m2-selected-real-p1-history-fixture-fix-1021021417-20336
```

No full suite, install, or local browser/socket test was run.

## Recommended next step

Diagnose the existing App boot/readiness failure that leaves the project
combobox absent in the exact frozen graph. Any correction must be reviewed
independently before another central run; do not infer selected-writer or
ledger status from this attempt.
