# P4 D141 corrected preparation handoff

Status: `NOT_READY`. This is a finite, source-only handoff. No row was installed, no control or submission was made, and no service body was run.

## Correction F001: the named row is currently D84 five-selector history

The current `p4-current-becfe-http-3legs` row in `orch/tests/suites.conf` has live registry preimage SHA-256 `38a5a5f808b14f1778ba75d90d4024fb3cb38941ed60669c7e113c0c86bc797b`, mode `0600`, and row SHA-256 `db3ee5aac42aa0be7e98a5bd7b8a0bf2cd87c228db3806aaf53d187b92ea7f59`. It points to the D84 five-selector manifest SHA-256 `13e5c3080d0df736b70924ba785eeb55a8af4ebd7ea575da6e433d4ab93b9636`:

- the ten-note selector; and
- four `test_public_helper_restart_exact_retry_later_head_inverse_redo` parameter cases.

An earlier read-only review recorded registry snapshot `84d304…`; the registry changed externally while this packet was being inspected, while the named row remained byte-identical. Therefore the live `38a5a5…` value is the only valid later CAS preimage. The current row must not be described as already three-primary, and its D84 receipt must not be retargeted. The exact later three-primary command is recorded in `recipe.json`; its only unresolved values are the final tuple-derived manifest, evidence directory, and Agent checkout path.

## Supported continuation

After the final four-way tuple and ordinary receiving receipts exist, render a `p4-d73-v1` manifest with every launcher-required key. Render the candidate row with exactly these three selectors: CLI/sheet, ten-note, and conflict/rerun. CAS-install only the owned named row with the existing `tools/install_p4_launcher.py`, asserting the live registry preimage above. The installer’s backup, before/after hashes, outside-row identity, and final registration are the publication receipts. Then use the existing central request route:

```text
request-test integration:agent p4-current-becfe-http-3legs --no-cache
```

`request-test` cannot carry arbitrary command or environment fields. No second controller, helper API, or new route is supported.

## Source and historical boundary

The binding Agent source is `28e56cacb42d3da85b02e5b3543895b44f3d0f70`, tree `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`, with parents `c585cb2aa73c5298d474e614cb2144f58f27e605` and `b4eb5db76fda523407b90a9dbe820f4e20cc1f1d`. Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` and recorded Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` are the integrated producer bindings. The final App source, clean checkout, and receiving receipt are absent; no App home is substituted.

All three original P4 sources and their exact hashes remain protected. D84a is retained as authentic mixed historical coverage: four restart/late-head cases passed and the ten-note selector timed out at 45.314 seconds. D97 original/independent0450 is the sole authentic historical ten-note pass at 28.101 seconds. Existing restart, history, undo/redo, conflict/rerun, receipt, no-write, and no-leak predicates remain unchanged historical/source requirements.

## Admission and remaining inputs

Use `4600000000` bytes as the source-preparation floor and `4000000000` as the stop. These are not an automatic P4 body floor. Future P4 heavy admission follows the recorded D89-kind `5200000000` floor unless genuine retained D89d peak evidence supports its measured floor; D89a/core-pristine `4700000000` and the App packet’s `5000000000` are not automatic P4 body floors. Preparation and future body admission remain distinct, with no new policy or gate.

The App/GO/registration inputs are genuinely missing. Comparator sequencing is one-heavy/MAIN input before body, not a prerequisite for preparing this source. AST hashes are conditional on an actual final cut-record requirement. No body, GO, REG, or ship credit is granted here.
