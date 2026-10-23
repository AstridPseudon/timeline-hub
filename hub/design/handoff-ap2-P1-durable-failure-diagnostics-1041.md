# Handoff: AP2 P1 durable failure diagnostics

Implemented on App exact base `116b6514137343668fb24bff6b53f8b89d2ae2e0`.

Only `tests/e2e/local/three-products.p1-chain.spec.ts` changed. The second
case's original POST-count assertion remains unchanged semantically and is
re-thrown unchanged after a failure-only capture. The capture is stdout JSON,
bounded to existing diagnostic limits, and records the original case phase and
identities, request/reply traffic, request bases/reads, displayed/runtime head
evidence, pending/rejected outbox state, recovery message/UI state,
page/console errors, and failed requests. It does not record headers and
redacts credential-bearing values.

Static evidence:

| Check | Result |
| --- | --- |
| `git diff --check` | PASS |
| Scoped ESLint with `--max-warnings 0` | PASS |
| `timeout 180s node node_modules/typescript/bin/tsc --noEmit` | PASS |
| Playwright `--list` | PASS; exactly 2 tests |

No browser/body rerun or service run was performed in this worker. The
diagnostic is intended for the next single original service journey; it will
write to the existing durable service `log.txt` through stdout before
rethrowing the original assertion error.
