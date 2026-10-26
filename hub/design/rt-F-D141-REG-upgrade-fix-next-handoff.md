# D141 Runtime upgrade REG handoff

Implemented the 13 independently proved upgrade REG repairs from
`rt-F-D141-REG-join-P5-review-0445` on base
`6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`.

Changed exactly `runtime_protocol/upgrade.py`: the staged `RealmStore`
inspector now receives the production `db_path` and `threading.RLock` before
timeline integrity inspection. This preserves fail-closed validation,
journal/rollback/integrity behavior, and schema v32. Tests, assertions,
fixtures, inputs, skips, contract files, `timeline_commit_store.py`, and P5
sources were not changed.

Acceptance is complete: the exact 13 original selectors from `reg.json` pass
(`13 passed in 4.12s`, exit 0) with
`PYTHONDONTWRITEBYTECODE=1`, authenticated Agent checkout
`/home/user/work/wt/agt-pin-28e56cac`, and private basetemp/cache. `git diff
--check` and scoped AST checks pass. Exact command, selectors, hashes, and
source-predicate custody are in the absolute evidence files.

Applicability: the fix is exercised by `upgrade_realm` and its 13 upgrade
tests. The reviewed P5 integration/crash route does not call this code, so no
new-head P5 proof is claimed; the prior P5 receipt remains the boundary.

Next step: independent review, then merge/qualify the new Runtime head and
re-prove any required downstream gate on that post-fix head. Do not move
consumer pins based on this narrow targeted result alone.
