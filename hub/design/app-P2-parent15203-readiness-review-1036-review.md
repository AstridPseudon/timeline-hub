# P2/A2 parent15203 independent readiness review

Verdict: SOURCE PASS. Approval remains HELD_PENDING_OWNER_ANSWER per the scope escalation; this is not original-browser GO.

The exact Sol1028 proposal materializes as one line in `tests/e2e/local/three-products.p2-tour.spec.ts`:

```ts
await expect(page.getByTestId('runtime-not-connected')).toHaveCount(0);
```

It is applied in the shared helper used by all three callers (lines 746, 778, and 798). The original connected/project/track/geometry/input/request/reply/history/reload/undo predicates are unchanged. The assertion rejects the retained-before-down state even when connected and visible checks pass, and accepts only after the connection panel is gone.

Source proof: `support/app.ts:256-257` uses the same panel-removal convention. `RuntimeConnectionProvider.tsx:478-489` keeps the connected app under `inert` while the overlay exists and clears it only when `exit.left()` clears the overlay. `RuntimeConnectionPanel.tsx:47-77` calls `exit.left()` only after settle and leave timing. Gate behavior is identical to frozen comparison commit `3881e9440688f774878e18806da2dc5c993a9b00`.

The bounded retained finding is actual inert at mouse-down, clearing by move completion, with unchanged clip and no selection. Exact callbacks/capture, save scheduling, outbox state, and Runtime cause remain unknown; zero commit POSTs do not establish any of them.

Tests: fallback focused jsdom Vitest passed 2 files/154 tests; both app/node `tsc --noEmit` checks, targeted ESLint, and `git diff --check` passed. The requested `--configLoader=runner` Vitest command failed before test load because the existing config references `__dirname`; no browser/backend/service/full suite was run.
