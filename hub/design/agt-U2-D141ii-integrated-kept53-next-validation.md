# D141ii integrated kept53 validation

Verdict: **PASS**. REG0 recommendation: **True** within this proof scope only.

## Bindings

- Agent integration and proof worktree: `ec0a9f5baef2c31bc5179087b83f044524575182`, tree `83b84c79941917fde535ee3ddba5533a776cace3`, clean before and after.
- Runtime: `95d98f038320d5d46bd679ac000ab3e15825c935`, tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`, clean before and after; `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`.
- Final writer protected review: PASS; reviewed commit `66720e11e8daa26a4e192a83d592cbe5caafc109`; F7 remains disclosed.
- Owner approval retires exactly two installer originals, dated 2026-10-26, with its verbatim quote retained in the ledger.

## Targeted proof

Selectors came directly from the reviewed `final-selectors.json` as a Python list: 38 unchanged inverse selectors plus 15 migrated writer selectors, including the force-refusal companion as one of the 15. The corrected acceptance run used the existing venv, `-q -o addopts= -n 3 --timeout=45`, private basetemp/cache, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U2-D141ii-integrated-kept53-next:/home/user/work/runtime`, and the Runtime checkout variable above.

Result from `targeted.xml`: **53 passed in 9.41s**, 0 failures, 0 errors, 0 skips. Original-purpose count and actual testcase count are both 53 and are reported separately in the JSON evidence.

The initial exploratory invocation omitted `ASTRID_RUNTIME_CHECKOUT`; it recorded 48 passed, 4 failures, and 1 error from the explicit missing-checkout guard. It is not the acceptance result and was superseded by the corrected run.

## Accounting

The per-ID ledger has all 64 records: 9 earlier qualified move PASS receipts, 38 retained upstream inverse PASS cases, 15 protected writer migration PASS cases with the exact reviewed reply-shape list, and 2 exact owner-approved installer retirements. Historical full-pair IDs 24814/25513 on candidate `ecdc242…` versus pristine `64197afa…` and all 397 cut-bad outcomes remain unchanged inputs; they were not retargeted.

Replacement installer controls remain protected by the prior 4-pass targeted evidence. Exact prior move and accounting publications are referenced by hash; no prior body was duplicated or fabricated.

## Checks and limits

- `git diff --check`: PASS before and after; no product or test mutation.
- Disk sampler: 53 fresh five-second observations, minimum 5956202496 bytes, all above the 4,000,000,000-byte stop line.
- No package installation, child, full/core/browser/render/live journey, build/ZIP, source repair, force option, authenticated undo change, hub operation, merge request, or pin.
- Existing protected-review F7 remains an environment finding; no broad lint/typecheck claim is made.
