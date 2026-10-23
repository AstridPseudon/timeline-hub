# F-D22 custody/process/projection disposition

## Independent review F-D22-custody-review-1525

**PASS for the two test-harness changes only.** Compared with
`58316fd6e0ce8a1fb3b2b3826ec71906d29080de`, commit
`3ef951f3abd56a918b54b03226ec80e8b80155ab` changes only the custody and
installed-registry test files after evidence cleanup. Runtime provenance was
verified from the already imported `runtime_protocol.platform` at
`/home/user/work/runtime`, commit `9ce4242bc01f100bab9efc51032a73985cefb2b2`,
using `/home/user/work/venv-agent/bin/python`.

The engine custody counterpart passed in the targeted service (`1 passed in
1.59s`). The original two projection nodes passed with the supported schema
path (`2 passed in 9.37s`) and in a clean environment without it (`2 passed in
10.03s`). Ruff has zero new findings versus base; private mypy is exactly
`1912` versus baseline `1912`; compileall, vendor lock, artifact manifest, and
diff checks passed. Product guard bytes and original safety assertions are
unchanged. The full D22 result remains FAIL, and seven managed/CPU nodes remain
UNCONFIRMED; no full or broad cohort run was performed.

Exact commands and complete evidence are in the paired review report copied to
the absolute orchestrator design directory.

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
