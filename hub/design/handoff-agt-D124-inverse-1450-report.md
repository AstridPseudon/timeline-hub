Blocked on Runtime; no Agent product changes applied.

Added [the focused regression](/home/user/work/wt/agt-D124-inverse-alias-sol-1435/tests/sdk/test_d124_grouped_inverse_boundary.py). Runtime auth1764–1765 resolves earlier child aliases after removing their occurrence. Independent source/security review confirmed this diagnosis and found no test weakening.

Validation:

- Focused regression: **2 passed, 1 failed**. Grouped inverse retains the exact `provider occurrence alias is outside its boundary` refusal.
- Strict wrong-pair, owner, alias and ABA controls: **20 passed**.
- Scoped Ruff, Python 3.11 compilation and `git diff --check`: **PASS**.
- Runtime SHA/tree, cleanliness and module origins verified before/after.

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D124-inverse-alias-sol-1435/evidence/validation.md) and [source diagnosis](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D124-inverse-alias-sol-1435/evidence/root-cause.md) are saved alongside the manifest and receiver recipe.

OriginalTrue was not rerun: no meaningful Agent correction and observed disk below its 5 GB admission floor. Original physical pairs remain unverified.

Wrote `commit-msg` and `BLOCKED`. Next: Runtime owner corrects inverse boundary custody, then validates the retained positive regression before original/Farm qualification.