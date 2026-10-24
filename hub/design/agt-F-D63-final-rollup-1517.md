# D63 report

Published read-only evidence:

- `d63-final-rollup-1517.json` — exact 276-row structured rollup.
- `d63-final-rollup-1517.tsv` — flat order/ID/status/category/baseline/evidence table.
- `d63-final-rollup-1517-report.md` and byte-identical design handoff.

Results: 199 NEW-OURS, 2 renamed counterparts, 75 exact counterparts. Current qualification preserved: 162 PASS / 112 OPEN / 2 DEFERRED. Only 7 of 66 fail-both rows qualify pre-existing; 59 remain cause-open.

Validation:

- `python3 -m json.tool` — PASS
- Structural/count/evidence-preservation validation — PASS
- Byte-identical handoff hash — PASS
- `git diff --check` — PASS
- No tests, original/full runs, source edits, installs, or daemon searches performed.

Remaining: 7 blocking core rows (5 inside exact276, 2 outside), order 181 remains REVIEW without home PASS, and 9 current-PASS contrasts need final-cut confirmation. `DONE` and commit message are present.