## FAIL — independent R2/F review

Finding: incomplete fork provenance is accepted.

`inverse.py:433-443` guards only present `commit.materialization` bindings. If the internal-root binding is missing while the shot binding remains, a later equal-value clear on the fork is accepted, and inverse of the original publication also succeeds. This violates the required complete-owner/root/revision provenance and same-value history scan.

Probe result: `inverse UNEXPECTED_ACCEPT False`.

Validation on author branch `d7db17a60`:

- Fork regression + original exact test: **6 passed**
- Scalar provider lane: **20 passed**
- Immediate R2 negatives: **16 passed**
- Config/history/ABA/compiler/transcript controls: **8 passed**
- Ruff, mypy, vendor lock, artifact manifest, and diff checks: **all passed**
- Diff contains only `inverse.py` and the new regression file.

No code or tests were changed. Recommended next step: fail closed on missing/ambiguous materialization bindings and add the missing-binding/equal-clear regression.