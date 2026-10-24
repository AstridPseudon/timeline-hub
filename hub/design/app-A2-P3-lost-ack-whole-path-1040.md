# Report: app-A2-P3-lost-ack-whole-path-1040

## Outcome

Hypothesis “B was submitted early” is **FAIL / unsupported**.

The App outbox cannot dispatch dependent B while A remains pending:

- `commitOutbox.ts:464-484` returns the existing pending request.
- `commitOutbox.ts:500-516` assigns B’s `readyBase` only after A is accepted.
- `localSaveSession.ts:269-320` persists B with `basis: { after: A }`.

The observed `attempts: 2` can therefore be an automatic exact retry of A, not B.

## Source path

Relevant production blobs are identical between base `82cb5c0005df7abe0fcb8673f7be192a6c9e9183` and HOME `d6ed8cbda122d810d5836ebfce3c56c10e76e9b4`:

- `commitOutbox.ts` — `8f6c157b...`
- `localSaveSession.ts` — `c8eb5074...`
- `timelineLocalSaveHandoff.ts` — `bf167a51...`
- `useTimelinePersistence.ts` — `b289d039...`

The real path is:

`timelineLocalSaveHandoff.ts:565-577` → `localSaveSession.ts:165-208` → `dataProvider.ts:746-767` → `client.ts:687-694` → `generated.ts:202-204` → Runtime `/v1/.../commit`.

Runtime commit handling at pinned `37eb6c7b...` looks up `(timeline scope, idempotency key)` and replays the stored result (`timeline_commit_store.py:189-200, 1205-1218`). A retry with the same key/body is expected to return the durable result without a second history entry.

## Why Gate5 reports two attempts

`three-products.spec.ts:795-807` increments `attempts` before awaiting `route.fetch()` and before adding the request to `posts`.

After `loseAck()`:

- `useTimelinePersistence.ts:551-589` schedules transport retry after 500 ms.
- `useTimelinePersistence.ts:892-903` explicitly treats this as recoverable.
- `localSaveSession.ts:165-208` retransmits the retained pending request.

Therefore the second counted POST may be A’s automatic exact retry. The retained Gate5 result does not include the second request’s body or key, so it cannot prove B was sent.

The test assertion at `three-products.spec.ts:1365` counts all POST attempts, while later assertions at `1661-1676` explicitly expect A’s exact retry to be POST number two and B to be POST number three.

## P1 comparison

Retained P1 passed:

```text
npm run test:e2e:three-products
playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.p1-chain.spec.ts
2 passed (56.3s)
```

P1 captures request body/key identities (`three-products.p1-chain.spec.ts:393-415`) and verifies the exact retry (`1493-1501`). Its route timing controls the retry before releasing the dependent request, so it does not use an undifferentiated attempt-count assertion.

## Deterministic reproduction for Sol1040

Repeat the retained Gate5 sequence, but capture each commit POST’s raw body and `Idempotency-Key` immediately at interception, before awaiting `route.fetch()`:

1. Submit A and hold its acknowledgement.
2. Perform the Agent C edit.
3. Abort A’s held response.
4. Wait until A’s durable outbox state is `pending.outcome.kind === "retry"`.
5. Start B’s drag.
6. Classify POST #2:
   - Same body and key as A: automatic exact retry; not B.
   - Different body or key: investigate as a real outbox violation.
7. Confirm B only becomes POST #3 after A’s accepted response; B should have a fresh key and base the A head.

This requires no private-trace extraction beyond the request identity fields.

## Evidence

Retained Gate5 command:

```text
playwright test --config playwright.three-products.config.ts \
  --grep 'M2 real gate 5 ...'
```

Result: **FAIL**, expected attempts `1`, received `2`, at `three-products.spec.ts:1365`.

No local tests were run; this was a source-only investigation as requested. No production or test files were changed. Worktree remains clean.