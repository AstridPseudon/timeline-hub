## D114 report

- Ran one isolated `p2-register-asset` original on the exact authorized tuple.
- Fresh normal checkout receipts verified: all four detached, clean, and exact SHA/tree.
- Source preflight: PASS, exit 0, 3s.
- Service: `app-pin-04beedcd-p2-d114-asset-0855-1025085739-15712`
- Terminal: FAIL, exit 1, 236s.
- Readiness: PASS 1/1.
- Original: FAIL 1/1.

First unmet predicate: `tests/e2e/local/three-products.p2-elements-assets.spec.ts:655`, called at `:1179`, during guarded native Undo response comparison. Backend outcome remains UNKNOWN.

Commands used:

- `request-test ... p2-d114-asset-0855-preflight --no-cache` → PASS.
- `request-test ... p2-d114-asset-0855 --no-cache` → submitted once.
- `wait-test <same ID>` → FAIL.
- `git diff --check` → PASS; worktree clean.

Outputs preserved:

- `submission/p2-register-asset/p2-register-asset-submit-plan.json`
- `submission-checkpoint.json/.md`
- `terminal.json/.md`
- `DONE`
- `commit-msg`

No product or test files changed. No retry, duplicate, retarget, collector, or cleanup performed.