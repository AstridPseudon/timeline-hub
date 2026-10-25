## Report

- Read PLAN.md and all requested D107/D124 handoffs.
- Ran only the two approved selectors against Agent `20177e…` and immutable Runtime `5e9ad1…`.
- Result: **exit 1; 2 failed, 0 errors, 0 skipped**.
- Both failed identically at `test_m1_current_equivalent.py:308`: expected 5 baseline history items, received 8.
- Source boundary: failure occurred before the public SDK outbox journey.
- Safe frame: normal registered-provider Runtime/Agent history admission and baseline assertion; not a harness/timeout failure.
- XML evidence: [current-equivalents.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D107-current-two-1525/evidence/current-equivalents.xml)

Command used:

```sh
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 \
PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-5e9ad1c6" \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
--timeout=45 --tb=short --junitxml=OWN_EVIDENCE/current-equivalents.xml \
tests/editing_conformance/test_m1_current_equivalent.py::test_new_ours_current_equivalent_preserves_m1_commit_journey[disjoint-rebase-undo] \
tests/editing_conformance/test_m1_current_equivalent.py::test_new_ours_current_equivalent_preserves_m1_commit_journey[touched-basis-conflict]
```

No source, test, pin, or assertion changes were made. No unchanged retry or broader suite was run. Postflight origins and `git diff --check` passed. Further baseline-history reconciliation requires orchestrator review.