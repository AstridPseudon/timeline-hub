Replaced the superseded proposal with **35 passing conformance cases**, using real R4 runner/rebase APIs plus bounded guard and outbox adapters. The existing wire format remains unchanged.

Validation:

```bash
PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/m0_suffix
# 35 passed in 675.05s

/home/user/work/venv-agent/bin/ruff check --no-cache --config 'include=["tests/m0_suffix/**/*.py"]' tests/m0_suffix
# All checks passed

git diff --check
# Exit 0
```

The cases retain original guards and intent, use a fresh B key after A’s ACK, allow equal-state ABA for this handoff, and separately preserve inverse-history write guards.

Updated [decision and evidence](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/suffix-basis.md>) and wrote the [commit message](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m0-suffix-conformance/commit-msg>). Temporary test data was cleaned.

No blockers. Runtime/browser restart remains unverified; persistence is modeled through JSON reload. M1 must preserve relative intent and scoped IDs, capture complete guards before dispatch, implement atomic outbox/Runtime acceptance, and promote these cases into production journeys. Full repository suites were not run.