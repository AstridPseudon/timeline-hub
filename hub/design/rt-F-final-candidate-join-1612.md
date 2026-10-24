## Report

Implemented the private joined F-final candidate:

- Added the existing inverse-sequential test to the core runner: 84 Python targets + TypeScript target.
- Preserved D68 wrapper, owner extras, overlap receipt, reviewed wrapper, and builder pins.
- Removed direct delivery-builder rows; delivery rows use the reviewed isolated caller.
- Kept only source/gate tuple placeholders pending.
- Durable evidence: `.../workers/rt-F-final-candidate-join-1612/evidence/join-validation.txt`
- Hashes:
  - installer `2262201f…`
  - delivery caller `64c83b4e…`
  - core runner `c2f319ac…`
  - rows `5d678805…`

Checks passed:

- Durable no-install installer/preimage validation.
- Python compilation.
- `ruff check --select F`.
- `mypy --no-incremental`.
- Shell syntax for all rows.
- Inverse test collect-only: 28 collected.
- Selector membership and protected-test byte equality.
- `git diff --check`.

Default Ruff retains inherited `EXE001/I001/SIM905` findings; no reformatting applied.

No live install, source Git writes, full/core/gate suite, product execution, build, ZIP, network, or tuple-dependent run performed. Actual installation remains pending the separate cut task.

Commit message written and `DONE` marker created.