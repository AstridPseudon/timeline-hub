# G5 retained publish-behavior test ports

**Disposition:** bounded test-port PASS; DRAFT-only / P1 NO-GO. No integration
merge is recommended from this worker.

Only `tests/packs/timeline/test_cli_status_publish.py` changed. The separate
publish positives now use the supported detached-document `commit --file
FILE --idempotency-key KEY` route against the existing authenticated
`public_session` base/closure and an actual saved document. The tests retain
accepted receipt/idempotency, exact base revision/publication, retry without a
second history write, output/next-action messages, clean no-write, and
conservative CAS refusal with the file preserved. The four legacy parity
publish parser nodes were explicitly stale in the settled source-1515
disposition and remain untouched/deselected; no product route was resurrected.

Source hashes:

```text
de5d13bbfcc844b1313ee66696aad8b51e2682c6d6ff3c55d4f5c2d90f88f675  tests/packs/timeline/test_cli_parity.py
421da9d61c4b80a7019cc2b37754814008b7fbed039f8a6405ba43b8874ccd8a  tests/packs/timeline/test_cli_status_publish.py
```

Evidence:

- `tests/packs/timeline/test_cli_status_publish.py`: **14 passed**.
- `test_cli_parity.py -k 'not publish'`: **57 passed, 4 deselected**.
- Both files: **75 tests collected**.
- Full two-file targeted run: **71 passed, 4 failed**; all four failures are
  the named stale `publish` parser nodes, which fail because the command is
  retired. No other failure was deselected.
- Targeted Ruff: **PASS**. `py_compile`: **PASS**. `git diff --check`:
  **PASS**.
- Baselines improved without rewriting artifacts: Ruff **2148 vs 2149** and
  mypy **1911 vs 1912**.

Exact commands and full failure names are in the worker report:
`workers/agt-G5-publish-test-ports-1536/report.md`.

Limits: no full/browser/socket/daemon/native/P1/P4/integration suite was run;
no product, Runtime, schema, generated client, pin, dependency, or shared
environment changed. The four stale parity nodes remain the exact outstanding
owner-visible failures in the G5 CLI-retirement/product owner boundary
(`astrid/packs/timeline/cli.py` command registry), not green-by-deselect.
