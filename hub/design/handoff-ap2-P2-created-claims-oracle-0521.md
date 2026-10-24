## P2 report

Updated only [three-products.p2-popup.spec.ts](/home/user/work/wt/ap2-P2-created-claims-oracle-0521/tests/e2e/local/three-products.p2-popup.spec.ts:464).

- ADD now requires exact ordered claims:
  - `occurrence:${sharedOccurrenceId}/asset:${authenticatedAsset}`
  - `occurrence:${sharedOccurrenceId}/clip:${reservedRawRowId}`
- SWAP remains exact with no `created` field.
- Verified fixture asset absence at lines 497–500.
- Provider source lines 844–851 and C0 creation-claim contract support this order.
- P1 and Gate5 files unchanged byte-for-byte.

Checks:

- Playwright `--list`: exit 0, 2 tests listed.
- Three TypeScript projects: exit 0.
- ESLint: exit 0.
- `git diff --check`: exit 0.
- A3 provider control under Node 22: 36/36 passed.
- Node 20 provider attempt was environment-incompatible because the test explicitly uses Node environment but accesses `navigator`; no product failure.
- No live/browser/backend run performed. D45 remains `0 PASS / 3 FAIL / 5 NOTRUN`.

Hashes:

- Target before: `722b7e9f...3f8b8e`
- Target after: `05370adc...b64a84`
- Outside-shape prefix/suffix hashes unchanged.
- P1: `50960dd2...9ebf17`
- Gate5: `0e69b561...318f14`

Commit message written and `DONE` marker created.