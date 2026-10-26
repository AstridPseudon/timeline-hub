# D141 integrated post-REG handoff

Runtime integrated head `95d98f038320d5d46bd679ac000ab3e15825c935` / tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1` is clean and contains the reviewed TypeScript author `4a66dee1ab34f260ea64bd58aa30cf7ac66c3ae3` plus corrected-identity upgrade author `012889c1b0bbfe5f290f757cb6d31dd7d995ccc7` on original base `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`.

The exact 15 REG selectors passed once on that integrated head: 15/15 PASS, zero failures/errors/skips/xfails. The 38 `NEW_OURS` records remain visible and are not included in the zero count. Generator, Node syntax, configured TypeScript, and diff checks also passed.

P5 applicability is path-based, not inferred from test-blob equality. The changed upgrade hunk is not reached by P5: P5 setup calls `migrate_canonical_to_current`, while `_validate_candidate` is called only from `upgrade_realm`; the TypeScript generated outputs are not P5 imports. Agent freeze2 paths `tests/conftest.py`, `tests/lanes.py`, and `astrid/packs/timeline/cli.py` are not loaded by the Runtime P5 process; Agent full and the bounded P4 CLI reproof remain separate required follow-ups from freeze2 and were not run here.

Next step: retain this producer receipt, then move normal Runtime consumer pins only through the existing supported vendor/installer tools. Do not retarget the historical P5 receipt, request a full-suite GO, or claim release/tag status from this evidence.
