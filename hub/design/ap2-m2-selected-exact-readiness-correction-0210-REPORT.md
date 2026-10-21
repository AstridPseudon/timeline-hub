# AP2 M2 selected DEV exact readiness correction

## What changed

Corrected only `tests/e2e/local/three-products.selected-param-dev.spec.ts`.
At each of the three existing readiness boundaries, the test now keeps the
existing seeded project/timeline helper and verifies the exact seeded timeline
through the existing `video-editor-provider[data-timeline-id]` selector.
It also verifies the exact seeded clip through the existing
`.clip-action[data-clip-id="${selected.clipId}"]` selector.

The initial boundary already had the exact clip and parameter-panel checks.
The post-P2/source-removal reload now explicitly checks the timeline and clip
before the existing click, parameter-panel, and `Amount = 8` assertions. The
lost-ACK reload now checks the timeline and clip, reopens the existing
parameter panel, and confirms `Amount = 8` before locating `Recover saved
edits`. The recovery click, retry, and all behavior assertions remain in their
original order.

## One-to-one mapping

| Existing boundary | Readiness retained/added | Behavior left unchanged |
| --- | --- | --- |
| Initial `page.goto` | `openSeededTimeline`; exact provider timeline id; exact selected clip; existing params surface | P1 edit, exact P1 schema pin, selection, and command assertions |
| Existing reload after P2/source removal | Same helper; exact provider timeline id; exact selected clip; existing params and `Amount = 8` surface | P2 revision/source removal, refused P1 edit, refusal body/pin assertions |
| Existing lost-ACK reload | Same helper; exact provider timeline id; exact selected clip; existing params and retained `Amount = 8` surface before recovery lookup | draft/retry state, recovery action, exact retry body and idempotency key, restart/reload, undo, and zero legacy writes |

No navigation or reload was added. No automatic recovery/retry, timeout,
DOM hook, production code, or assertion removal was introduced. The genuine
P1 `p1DocumentPin` assertions remain the authority at the first edit, refusal,
lost request, and final traffic checks. No support helper callers changed.

## Verification

Starting reviewed source:

- SHA: `45cdc3a59b79357be08e20d6ba187fedb16c8373`
- tree: `a4f47713c4227075a5f59e42d1006fa1eb831fe3`

The final working tree is intentionally uncommitted; the harness owns the
commit and final SHA/tree after worker exit. The only changed repository path
is the selected DEV spec above.

Passed:

```text
npm exec -- eslint --no-cache tests/e2e/local/three-products.selected-param-dev.spec.ts tests/e2e/local/support/app.ts
exit 0

npm exec -- playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list
exit 0; Total: 1 test in 1 file

git diff --check
passed
```

Not run, as required: browser execution, localhost/live sockets, full or
central suites, and any gate. The readiness behavior remains unverified in a
real browser until the central/authorized journey run.

## Smallest remaining limits and next step

`openSeededTimeline` still identifies the project by its existing display-name
selector and waits on the existing first track field; this correction adds the
exact timeline and clip/parameter surface in the caller without changing that
shared helper. The next step is the orchestrator's central real journey on the
exact harness-produced SHA/tree; no broader suite is warranted by this task.
