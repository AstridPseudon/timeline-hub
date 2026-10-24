# P2 terminal report

- Same-ID request waited to terminal: `app-P2-final-pure-integrated-1036-full-e2e-three-products-1024115551-11933`
- Command: `.../bin/wait-test app-P2-final-pure-integrated-1036-full-e2e-three-products-1024115551-11933`
- Result: `fail`, exit `1`, duration `469s`; no resubmission or source/config changes.

Evidence: [summary](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-P2-final-pure-integrated-1036-full-e2e-three-products-1024115551-11933/summary>) and [log](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-P2-final-pure-integrated-1036-full-e2e-three-products-1024115551-11933/log.txt>).

## Stage results

- Door allocation: PASS; port allocated.
- Hosted build: PASS; built in 1m48s.
- Native seed + authoritative history (D21): PASS.
- Selector collection: PASS; exactly 8 tests.
- Mounted readiness: PASS; 1 passed in 39.4s.
- Original body: 3 failed, 5 did not run.

Original body failures:

1. Element Apply, `p2-elements-assets.spec.ts:377`.
2. Popup ADD, `p2-popup.spec.ts:815`; expected track `V2`, received `plate`.
3. Parent move, `p2-tour.spec.ts:690`; receipt ID mismatch.

Not run: element registerAsset, automatic child placement, popup SWAP, transition-none single, transition-none bulk.

## Custody

Selected source: App `d6ed8cbda122d810d5836ebfce3c56c10e76e9b4`, tree `542b772e6deed676b917f857708445b7d37a5aa8`, parents `cad736828b4890a4df5fff42a22bfa4851a0ecfc` and `01ea81395a9bb8f091262a9d8275407675188fe6`.

Same-ID snapshot retained the same tree and path, and preflight passed far enough to execute the body. Its full commit SHA and parent list were not retained separately, so they remain unknown. Agent, Runtime, and Composition pins were retained in `ext`; daemon/provider identity remains unknown.

## H36 diagnostic

Retained artifact:

- [diagnostic JSON](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-P2-final-pure-integrated-1036-full-e2e-three-products-1024115551-11933/playwright-output/p2/original-body/three-products.p2-elements-4b4f7-tch-reload-and-guarded-Undo/p2-element-apply-diagnostic.json>)
- Origin: 1260 bytes, SHA-256 `08509524d5fd04f181b3fac8d0cdd211a32e2f4a107c4e78807ae4713e8533a4`
- Attachment duplicate: same bytes and SHA.

It records `apply-click`, `request-start`, and `retained` for correlation `apply-1`; request was a scoped commit with an idempotency key present, but response status remained `UNKNOWN`, response `none`, and lifecycle terminal state `pending`. This is observation-only; it does not establish a commit result, abort, or receipt. No safe projector/writer or authenticated response fields were present.

No files were copied or deleted. Commit message written to the assigned path.