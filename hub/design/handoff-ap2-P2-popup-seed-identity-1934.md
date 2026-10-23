# Handoff: ap2-P2-popup-seed-identity-1934

Source-qualified PASS. On App base `2107e1870e51c650d59315f4cc1ab6af338f198c` / tree `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`, the only worktree change is four lines in `tests/e2e/local/three-products.p2-popup.spec.ts`: the setup `doc.patch` now declares the authenticated old registry asset for both physical internal-revision owners, `seed.occurrenceId` and `f2-occurrence-copy`.

The Farm run `app-ap2-P2-exact8-1023192238-31814` captured the refusal before popup gestures: 422 `capture_mismatch` / `doc.patch must declare every created identity`. Pinned Agent `079580ca46af77e0292d49dc34386b25c8391f99`, `_doc_patch.py` blob `e780e7abf3baf7aca1315fbc8a54c3a9e13feef2`, explicitly generates one asset identity per authenticated owner and requires an exact `created` list. This correction follows that rule from `oldMedia.asset` returned by the real import/selection flow.

Evidence: Agent doc-patch conformance **102 passed**; Root/App/Node TypeScript **passed**; scoped ESLint **passed**; Playwright three-products `--list` **2 tests**; `git diff --check` **passed**. Gesture test tail hash stayed `2eda7eb8fe2fa77ed69195f471ecf5d6d46736bed012cbd78035c5487e5e35cb`. No live Farm/browser rerun is claimed; independent review and an authorized pinned Farm rerun remain next steps. Full report: worker `report.md`.
