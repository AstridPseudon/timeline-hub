# F/D141b pristine comparator controller

## Admission

- Exact authored command and row verified against the independent final review:
  command SHA-256 `db0c2f366597cba1e4a4a067366fda38049fdcb15640d82a26b4dbac41d1043e`; row SHA-256 `c3ef3edaaf5250bbe14fa94a7625a5bb17154f82d01a14d9a80f479bae474fd7`.
- Independent review `agt-F-D141b-sol-command-review-0030` is `PASS_COMMAND`, exit `0`, for exact command-author commit `0710897c87834550d1ee68b3f120405a9c81fe8f`.
- Product source is not modified. The normal Agent freeze is `28e56cacb42d3da85b02e5b3543895b44f3d0f70` / `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`; official receiving peer `0023` is `PASS_SOURCE_QUALIFICATION`, and the normal merge receipt is hash `10ada0a1bc188dc001d234970db5876d5615e7540d7d853c23f95042b47493f5`.
- The controller binds only the two command-required manager markers after these receipts: `U2_FINAL_FREEZE_PASS=PASS` and `INDEPENDENT_COMMAND_PASS=PASS`.

## Operational scope

- One normal service row is added byte-for-byte if absent; an existing mismatch is a refusal.
- The single service request is the prescribed `bin/request-test integration:agent d141b-pristine-comparator-2358 --no-cache`.
- The service snapshot is not the test source. The authored command changes into and guards the immutable pinned Agent/Runtime paths, uses the existing Agent venv, 17 roots, `-n 3`, cleared addopts, no cache provider, timeout 45, durable JUnit, and decimal disk guards.
- No local pytest/product import/collection/body is run. This remains a `PRISTINE COMPARATOR` with no REG or ship credit.

## Receipts to complete

## Terminal receipt

- Exactly one request: `agent-d141b-pristine-comparator-2358-1026003644-27388`; service status `fail`, service exit `1`, elapsed `332s`. The service snapshot tree was `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`.
- Suite registration was the only operational config change: `suites.conf` grew from 162042 bytes / SHA-256 `84d3045878ea806439b73b0a5ca983c06371fcac2d42bc8c7e8add0ebfbd3988` to 162785 bytes / SHA-256 `38a5a5f808b14f1778ba75d90d4024fb3cb38941ed60669c7e113c0c86bc797b`; the exact authored row occurs once and all 187 prior rows were preserved.
- Command terminal status: `state=FAIL`, `exit=1`, `body_started=1`, `body_exit=1`, `monitor_exit=0`, `source_before_exit=0`, `source_after=clean`, `evidence_exit=0`, finished `2026-10-26T00:42:31Z`.
- Four pristine source records were identical before/after and clean at the exact pinned SHA/tree/path tuple. Interpreter: requested `/home/user/work/venv-agent/bin/python`, resolved `/usr/bin/python3.13`, version `Python 3.13.16`.
- Disk witness recorded source admission `5295308800`, body dispatch `5295300608`, and minimum observed `5277556736` bytes; continuous stop floor was `4000000000` bytes. Monitor exit was `0`.
- Direct XML suite attributes from `pristine-comparator.xml`: `tests=3255`, `errors=1`, `failures=4`, `skipped=0`. No passed count is inferred. The central service `log.txt` was empty; raw stdout/stderr, pytest log, XML, source witnesses, disk witness, exits, and terminal status remain private in the command run root.
- This is a terminal comparator `FAIL`, not behavior PASS, REG, or ship credit. No retry, alternate body, waiver, environment fix, or root-cause investigation was performed.
- No other D141b service status was `running` at final inspection; the one D141b heavy-body lock is the retained command run-root lock.

Raw receipt hashes are recorded in `result.json`; raw private artifacts remain in the command run root and the central service result directory.
