Implemented only the two authorized test blocks.

- Ordinary equal-final-state delete replay now asserts success with unchanged stable IDs and exact state/records.
- Provider tests assert canonical document, accepted command, receipt, head, and history linkage.
- Strict inverse/publication-ABA and conflict tests remain unchanged.
- AG-OCC-ABA: resolved by the 09:42 decision; manager should update the ledger.

Tests:

`pytest -q ...` across both files plus M1/native/inverse neighbors: **269 passed, 40 deselected**.

No blockers. Commit message and `DONE` marker written.