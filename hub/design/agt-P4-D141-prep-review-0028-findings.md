# P4 D141 independent preparation review

Verdict: `FAIL`

Preparation status: `NOT_READY`. This is not a source failure caused by the missing App, GO, comparator, or registration inputs. The FAIL is caused by two independently verified preparation defects: the named central route currently resolves to a historical five-selector row, not the three-leg route described by the packet; and the packet carries unsupported 4.7 GB/5 GB body-admission variants instead of the settled 4.6 GB source floor and 4 GB stop.

## Verified source and contract

- Agent source is exactly `28e56cacb42d3da85b02e5b3543895b44f3d0f70`, tree `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`, with parents `c585cb2aa73c5298d474e614cb2144f58f27e605` and `b4eb5db76fda523407b90a9dbe820f4e20cc1f1d`.
- Runtime and Composition bindings match the preparation packet. App is genuinely absent from the final tuple; it is not substituted with the non-binding App home.
- The three primary P4 files are unchanged and hash-verified. The packet preserves the historical restart, history, undo/redo, conflict/rerun, receipt, and no-write/no-leak predicates without claiming a new D141 body.
- The generated `commitTimeline` request and reply DTOs contain the settled C0 fields: command schema/op/version/select/args, steps with patch and optional reads, merge/reads/idempotency/dry-run/source/rationale/group, canonical closure, receipt/records/bindings/dependencies/history/undo steps, conflict reason/head, invalid code/path/hint/suggested command, and preview `would_status` with a null receipt. No DTO change is indicated.

## Findings

1. `P4-D141-F001` — The current `orch/tests/suites.conf:177` row named `p4-current-becfe-http-3legs` points to the old D84 manifest and runs five selectors: the ten-note selector plus four restart/late-head parameter cases. The preparation handoff describes three primary selectors (CLI/sheet, ten-note, conflict/rerun). The three-leg command is historical evidence, not the current row. The manager must render and CAS-install the final exact owned row before requesting it.

   The supported continuation is the existing `tools/install_p4_launcher.py` CAS path followed by `request-test integration:agent p4-current-becfe-http-3legs --no-cache`. `request-test` only accepts the existing row name, optional file selection, and `--no-cache`; it cannot carry arbitrary command or environment fields. Do not add a controller and do not retarget the captured D84 receipt.

2. `P4-D141-F002` — The source-prep handoff says fresh `>=4,700,000,000` bytes and the App packet carries a 5 GB admission. The task-authoritative rule is source floor 4.6 GB, stop 4 GB, default 180. Measure the current admission at continuation; do not turn 4.7/5 GB or D89a core4.7 into a preparation hard gate.

3. `P4-D141-F003` — `D141-cut-tuple.md` still records Agent and App as pending. The exact Agent source exists in the prep packet, but the authoritative cut record is stale/incomplete. Final App commit/tree/parents, clean checkout, and receiving receipt are absent.

4. `P4-D141-F004` — Explicit MAIN GO is absent. No reservation, clock time, or preparation packet supplies it.

5. `P4-D141-F005` — No D141-specific final service row or registration receipt exists. The old row and old receipts are historical only.

6. `P4-D141-F006` — The same-cut pristine comparator and later REG closure are not recorded. They are required before the one-heavy-body P4 sequence, but neither comparator PASS nor per-ID REG closure is a prerequisite for preparing this source packet.

7. `P4-D141-F007` — AST hashes are absent from retained App evidence. They remain conditional on an explicit final cut-record requirement; no approval requirement is inferred.

## Historical boundary

The D84a service `agent-p4-current-becfe-http-3legs-1024221732-29429` passed four restart/late-head cases and timed out on ten-note at 45.314 seconds. It is not a blanket five-node pass. The D97 original service `agent-p4-d97-original-0445-1025044719-22560` is the sole accepted historical ten-note proof at 28.101 seconds with per-step inverse/undo/redo, history/receipt, restart, and no-write/no-leak. Neither old receipt is reused for D141.

No body, GO, registration, or ship credit is granted by this review.
