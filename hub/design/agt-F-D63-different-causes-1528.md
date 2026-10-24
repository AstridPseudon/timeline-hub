## D63 report

Completed the exact four-row disposition for orders 5, 49, 50, and 51.

- All four: `MATCHED_STATUS_DIFFERENT_CAUSE_OPEN`.
- No pre-existing or exact-environment qualification.
- Current receipts remain `open`, `proof_matches=0`, `NOT_RUN_CURRENT_CORE159`.
- No current failure or regression inferred.
- Rows 5 and 51 use only their bounded D52 child-import/rendering attribution; rows 49–50 are not generalized into that scope.
- All four are non-core; no current core source repair is proven required.
- Remaining concrete fact: an authorized current exact result plus literal production-caller proof.

Evidence:

- [TSV disposition](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D63-different-causes-1528/evidence/d63-different-causes-1528.tsv)
- [JSON evidence](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D63-different-causes-1528/evidence/d63-different-causes-1528.json)

Validation:

- `python3 -m json.tool ...` — PASS
- Exact TSV row/order/receipt validation — PASS
- `git diff --check` — PASS
- Product/full tests — not run; prohibited by read-only scope.

Wrote the conventional commit message and empty `DONE` marker. No product files changed.