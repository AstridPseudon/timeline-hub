# D141ee inverse38 protected findings

## PASS

- All 38 recorded approved IDs were executed as exact selectors: 38 PASS, 0 FAIL, 0 ERROR, 0 SKIP.
- `astrid/core/timeline/inverses.py` is byte-identical to the recorded pristine blob; the only diff is that approved additive file.
- Every protected input and assertion remains in the exact restored test blob. The authenticated SDK undo route and Runtime writer surfaces are unchanged.
- No external production caller was found. The approved public-use surface is direct import of `InverseRequest`, `plan_inverse`, and `plan_inverses`; no writer or analogue credit is claimed.

## Finite findings / limitations

- Ruff fails with `BLE001` at restored line 770. Running Ruff against the pristine blob produces the same diagnostic, so this is pre-existing upstream debt; the review did not edit or suppress it.
- Erased-payload cases preserve non-invertibility and the erased reason, but the pristine planner returns caller-supplied before/after projections. The exact tests do not prove redaction; no stronger guarantee was approved or inferred.
- No broader or unassigned tests were run, so they receive no credit and are not part of this PASS.

No author repair was made.
