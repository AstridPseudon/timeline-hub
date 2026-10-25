Implemented P2 D105a scoped placement oracle.

Changed:

- [three-products.p2-elements-assets.spec.ts](/home/user/work/wt/app-P2-D105a-scoped-oracle-resume-0614/tests/e2e/local/three-products.p2-elements-assets.spec.ts)
- [p2-elements-assets-receipt.test.mjs](/home/user/work/wt/app-P2-D105a-scoped-oracle-resume-0614/tests/e2e/local/support/p2-elements-assets-receipt.test.mjs)

Proof added for projected identity, five byte-identical mutation refusals, and inverse residue detection. No product/DOM changes.

Tests:

- Node 20 support tests: 139/139 passed.
- Projection + `ShotTimelinePreview.integration` Vitest: 37/37 passed.
- Three locked TypeScript projects: passed.
- Scoped ESLint `--max-warnings 0`: passed.
- `git diff --check`: passed.
- Playwright `--list`: exactly 1 placement test; exit 1 is the repository skip-guard’s expected list-only behavior.

Protected six SHA-256 values remained unchanged. No browser, service, full suite, merge, or original placement run was performed.

Pending: independent protected Luna review, ledger integration by the manager, and later normal merge. `DONE` and commit message are prepared.

Appendix:

> Actual31499 proved a bounded oracle identity mismatch: the immutable occurrence projection mounts the canonical child as `<occurrence-id>:<raw-clip-id>`, while the old reload predicate selected the raw ID alone. D105a preserves upstream product behavior and qualifies the scoped oracle with exact projected count-one/raw-count-zero reload checks, strict wrong-occurrence, sibling, raw-fallback, duplicate, and same-bytes refusals, plus an inverse check that fails while the projected clip remains and passes only after that exact scoped identity disappears. No product behavior or Runtime wait was changed.