# D52 read-only qualification

## Result

FAIL — confirmed deterministic stale-lock cause, not environment or test flakiness.

Integrated receipt at `2300c0a1d2f80a94403f6ac870923ed3429ebb66`:

- Receipt SHA256: `163a943aeaaf8964abf56f6fd15f53ef322eb7362f28ff9f5d2e1b3bbadd444d`
- 7 tests: 4 passed, 3 failed
- Failed selectors:
  - `tests.stage1.test_capability_parity_gate_luna::test_stage1_capability_parity_is_explicit_and_family_proven`
  - `tests.test_capability_ledger::test_shipped_ledger_reconciles_historical_capability_sets`
  - `tests.test_capability_ledger::test_reviewed_v3_pack_labels_preserve_exact_canonical_action_admission`

Independent receipt at `a521535cc5`:

- Receipt SHA256: `d624de9560d918985c7338e5cc8fcbd0a219de35afbd5807c73122ea82f151d5`
- Same seven selectors: 7 passed, 0 failed.

## Cause

The checked-in census lock is stale:

- `config/astrid-capability-census.lock.json`: SHA256 `759c360d223dd0c952484331a474c59fa2d3ab9e2368e318c4c1650d1edf88b5`
- Current generator reconstruction produces executor inventory `114`
- Retained lock contains `113`
- Missing executor entry: `music.duck`

D411 changed the authoritative generator input:

- `astrid/core/contracts/output_result_exemptions.json`
  - a521 SHA256: `08f96ead...`
  - current SHA256: `751df50a...`
  - added `music.duck` to `non_exempt`
  - increased executor totals from 111/113 to 112/114

The normal caller is:

```text
python -m astrid.core.execution.capability_ledger approve --checkout "$PWD"
```

`capability_ledger.py` calls `_census_sets()`, whose executor inventory reads `output_result_exemptions.json`. The music pack manifest and production caller were already present and unchanged:

- `astrid/packs/music/pack.yaml`: SHA256 `255c3e84...`
- `astrid/packs/music/actions/duck/api.py`: SHA256 `09578822...`
- Production path: `duck_timeline -> client.invoke_result("music.duck", kind="action", ...)`

The rendering catalog and `artifacts.json` also changed in D411, but the normal census generator does not read them; they are not causal.

## Environment/source identity

Both retained runs used the same:

```text
/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1
PYTHONPATH="$PWD:/home/user/work/runtime:/home/user/work/runtime/packages/python"
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime
Runtime commit: becfe6db88b2cc034dba3fafa6c050117cdf2b06
```

Static source hashes show `capability_ledger.py`, `generic_host.py`, the music pack, runtime files, and beta matrix were unchanged between the independent and integrated paths. Current worktree was clean; `git diff --check` passed.

## Decision / handoff

No source or test changes made. No tests or gates rerun, per task restrictions.

Sol 1213 should run the existing finite approval invocation once on the coherent current tree, then rerun the exact seven selectors. No new approval gate is indicated. `DONE` and the required commit message marker were created.