# D141k validation

All checks used Python stdlib only (`hashlib`, `json`, `pathlib`, `shutil`, `xml.etree.ElementTree`, `collections`, `re`); no product imports, pytest, collection, provider, typecheck, lint, or body execution.

- PASS: XML SHA256 `7adf18d3a9cd20c2198d4cd4ccd7e0be59497e6111a73284c4977fe31b92b25d` and 9388 unique concrete IDs; 204 FAIL / 8988 PASS / 196 ERROR / 0 SKIP.
- PASS: derivative accounting `9561 = 9388 + 173` and `9161 PASS = 8988 + 173`; 173 aggregate members remain unnamed. Original `FAIL_CUSTODY_DISCREPANCY` is unchanged.
- PASS: pristine table hash `7535b9a70b0da2f36e2c9e2f0115cf70ef429d3b8152496a7f44a723033ae6a5`, 3255 records = 3082 concrete + 173 aggregate; 3250 PASS / 4 FAIL / 1 ERROR.
- PASS: ID multiset membership: matched 3018, cut-only 6370, pristine-only 64, no duplicate concrete IDs.
- PASS: 22 roots, 17 upstream-present, 5 explicitly absent project-only roots; unmatched ID is not treated as absence in a present root.
- PASS: 17 REG candidates exactly satisfy cut nonpass + same-kind pristine PASS; 4 both-bad rows are `FAILS_BOTH`; unmatched current nonpass rows remain UNKNOWN/N_A.
- PASS: 15 REG candidates flagged env-sensitive/undecidable and 4 supporting FAILS_BOTH rows flagged; fifth pristine timeout remains UNKNOWN with current cut PASS.
- PASS: disk trace has 10 samples, minimum `4699422720` bytes, and 4GB stop preserved before/after the join.
- PASS: service 24049 excluded; only corrected 26496 result used.

No final REG0/ship or Farm completion claim is issued; Farm need is conditional on the 15 flagged REG candidates.
