# D125 independent Proof verdict

Overall: **NO-GO**. Qualified **partialGO** for 5 verified tails.

- Preflight `...0913-15235`: PASS, exit 0.
- Sole terminal `...0943-3250`: FAIL, exit 1 after 554s.
- Original results: 5 PASS, 2 FAIL, 1 NOTRUN.
- Exact tuple, four clean checkout receipts, persistent plan, source hashes, service versions, and JUnit hashes verified.
- PASS tails: ADD, parent move, both transition clears, automatic child placement.
- FAIL: SWAP (`p2-popup.spec.ts:495`, `history_unavailable`); element edit (`p2-elements-assets.spec.ts:1052`).
- NOTRUN: registerAsset (`p2-elements-assets.spec.ts:1133`).
- SWAP lower private attribution: UNKNOWN. Pending element HTTP and backend cost: UNKNOWN/not inferred.
- No source changes or test reruns; typecheck/lint/targeted tests N/A for read-only review.

Artifacts written:

- `evidence/verdict.json`
- `evidence/verdict.md`
- `evidence/facts.json`
- `commit-msg`
- `DONE`

The final report is this message; no `report.md` or design publication was written directly.