# D128/F source and evidence review

## Verdict: FAIL

The sole service `agt-OPS-inventory-E2E-final-receive-1822-inventory-whole-maker-1025182407-27653` is not qualified. Its retained result records two fixture Git commits and two private Store initializations, then the unchanged parent maker exits `2` with no stage records. The expected parent inventory refusal was not reached. Candidate GREEN, sealed registration, verifier success, and adversarial controls remain unqualified.

## Exact first cause

This is a source1747 preparation defect, not a product failure and not a safety/classifier/permission refusal.

In source1747 `ops-child-custody/tests/e2e_inventory.py`, `prepare_venue()` creates `tiny-orch/tests/` and initializes both Stores, but never creates `tiny-orch/tests/suites.conf`. The normal Store projection contract requires that baseline: the unchanged Store helper's `Store.ensure()` calls `_verify_projection()` before its build callback, and `_verify_projection()` unconditionally reads `tests/suites.conf`. The retained venue confirms the directory exists while `suites.conf` is absent.

Therefore the first parent path is:

```text
parent maker
  -> embedded STORE_PY
  -> Store.ensure()
  -> Store._verify_projection()
  -> read(tiny-orch/tests/suites.conf)
  -> FileNotFoundError
  -> embedded exception handler / exit 2
```

That ordering explains the empty `parent_stages`: `run_stage` is inside the build callback, after the pre-build projection check. It also explains why this is not the expected parent RED inventory refusal, which would require a completed build followed by the unchanged verifier comparing the parent report against authenticated installed inventory.

## Minimum unapplied correction

In `prepare_venue()`, immediately after creating `orch / 'tests'`, create the empty projection baseline:

```python
(orch / 'tests' / 'suites.conf').write_text('')
```

This is the minimum source correction identified by the review. It is not applied here. No maker or service was rerun.

## Evidence limits

The retained `e2e-result.json` contains the parent argv and exit code, the empty stage list, and the runner's blocker, but no parent stdout or stderr. No separate retained stdout/stderr file exists under `/tmp/w-f24ccbdde1`; these are `EXACTMISSING`. The exact error text is therefore not claimed as a captured service record; it is the deterministic source-level cause from the pinned parent, helper, source1747 runner, and retained venue state.

Source state, private roots, fixture commit identities, lock identity, shell options, and helper/bootstrap routing were checked read-only. No dependency seed or Farm route was selected, and no production Store or request was touched.
