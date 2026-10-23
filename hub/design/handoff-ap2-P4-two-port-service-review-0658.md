# P4 two-port service review handoff

## Disposition

**PASS** for bounded source qualification and the terminal operations-row
review. This handoff does not claim live HTTP/body execution.

## Source qualification

- Resolved current integration base: `9df06d16de5270c449dea938175123942ad00a8b`, tree `39193b28f71e832d85ff01d6eec893ebdff8f1ea`.
- Candidate: `a809764ae56f9fc13845464138c9ad4cd56e2575`, tree `15b155b7872b24e640b82fb93382970eb6e837c4`.
- Exact ten-note blob: `cdb186d001fe8bd7476c2a059ee65e9a312dbec5`, matching reviewed ref `tl/ap2-P4-ten-current-review-0621`.
- Exact conflict-rerun blob: `cbd332db227ecb9c6254e8ced0af72c3de91821e`, matching reviewed ref `tl/ap2-P4-http-conflict-rerun-review-0647`.
- `cmp` passed for both donor files. Candidate code changes against the resolved
  base are only the two requested test paths; product/helper/fixture/schema/
  generated/pin ancestry is not part of this source qualification.
- Normal client source remains Runtime 34eac004; d106 edit-command schema remains
  exact. The target files retain the existing `test_native_batch_ingress.runtime`
  production caller and full-v2/closure/undo/redo/conflict/rerun/history/restart
  assertions.

Source checks:

```text
2 tests collected with pytest --collect-only (unknown timeout option warning)
Ruff: All checks passed
Mypy: Success, no issues found in 2 source files
git diff --check: passed
```

## Ops row

The ops worker is terminal: `DONE`, exit `0`. Receipt:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/queue/done/checkout-runtime-1cf5562f8d2eddb6ee26cbec5155f94098e057b8`

Verified checkout:

```text
HEAD  1cf5562f8d2eddb6ee26cbec5155f94098e057b8
tree  f74b016ea837f8148db4a602c972073a226ed177
status clean
```

The absolute suites configuration contains exactly one `p4-v2-http-nodes` row.
Recorded ops evidence is config `89540 -> 90710` bytes, target row `209 -> 1379`
bytes, and unchanged outside-row `89331` bytes with SHA-256
`d9591c5ece20def0e0c77dbb1f61169dcd221413c55bfa100c634c79397fa5e3`.
The after-row SHA-256 is
`2ff0bb94d75defeee99267b073369406f3069726728704ea135453b4234f7cc0`.
The exact Runtime SHA/tree/clean checks, Runtime/Agent import-origin checks, and
the original `venv-app2-native` pytest entrypoint/args/selector are retained;
there is no new launcher/suite/pin/client change.

## Limits / next step

No HTTP, body, socket, service, browser, full-suite, or build command was run.
Manager may now run the original ten-note node once and then the distinct rerun
node once, subject to the retained Runtime independent/integrated PASS. Those
live executions remain unverified by this review.
