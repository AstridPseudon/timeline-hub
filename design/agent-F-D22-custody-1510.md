# F-D22 custody/process/projection disposition

The full D22 run remains FAIL. Two stale harness inputs were corrected and
qualified without changing product source or safety assertions:

- custody wrapper fixture: restore the exact imported Runtime source root in
  the target `PYTHONPATH`, fixing the proven `sitecustomize` import failure
  that made `denied=False`;
- installed projection fixtures: carry the supported propagated schema path
  when present, while retaining the clean-environment absence.

The custody representative passed in the central service. Both installed
projection representatives passed with the original schema-path environment
and with a clean environment. The five CPU/process nodes remain unconfirmed:
their retained evidence has missing markers but no complete child stderr/argv
causal record. They are handed to childenv1454; no lifecycle source fix is
proven. Full details, exact commands, node IDs, and hashes are in
`report.md`.
