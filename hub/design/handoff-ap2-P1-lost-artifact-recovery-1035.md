# Handoff: P1 28486 lost-artifact recovery

Service run `ap2-P1-P3-ops-identity-return-1015-ap2-P1-chain-h6-1023101921-28486` cannot yield an exact refusal reason from retained artifacts.

The only durable evidence is `.../tests/ap2-P1-P3-ops-identity-return-1015-ap2-P1-chain-h6-1023101921-28486/log.txt`: the second P1 case timed out at `three-products.p1-chain.spec.ts:519`, with `traffic.posts` expected 2 and received 1 (`log.txt:160-177`). The expected 409 assertion at lines 520-521 was never reached. The named `error-context.md` and `trace.zip` are absent. The result directory has only status/manifests/log/summary; the temporary snapshot and harness directory were removed.

Source confirms why recovery is impossible: `scratchpad/orch/bin/test-run:37-44` creates and then removes the snapshot; `:43` retains only stdout/stderr in `log.txt`; `:46-47` retains only summary/tail. Playwright output defaults under the snapshot, and the local harness keeps runtime/audit output in memory before deleting its temp directory at teardown.

Do not classify this as a Runtime 409 or guessed legitimate local refusal. Source shows only a possible pre-dispatch capture/scheduling boundary: persistence awaits local capture before POST, while poll adoption uses a deferred recheck and clean-session ownership can be retired/rebuilt. The actual branch, basis, outbox state, and poll ordering were not retained.

Recommended next work:

- Add a minimal JSON `console.log` failure capture around the P1 line-519 wait, including full traffic, readonly outbox records, request/basis/head data, page/request errors, and poll/recovery state. `log.txt` is already durable.
- Preserve `test-results/three-products/**` before snapshot removal if trace/error-context is required; attachments alone are currently deleted.
- Extend the existing mounted `useTimelineSave` unit test with a controlled poll-adoption/owner-retirement boundary around split ACK, Agent move, and Source In `0 -> 3`. Assert durable intent/request identity and distinguish capture refusal from a later Runtime conflict without changing the original E2E body or expectation.

The first hold-oracle mismatch remains Luna1035-owned; no action was taken here. No tests were run per the slice restrictions; the prior 86-test bounded run was not repeated. Full evidence is in [the worker report](../workers/ap2-P1-lost-artifact-recovery-1035/report.md).
