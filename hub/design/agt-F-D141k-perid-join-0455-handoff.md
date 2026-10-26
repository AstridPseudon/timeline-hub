# D141k per-ID join handoff

## Result

- Corrected D141i service `agent-agent-core-full-1026032321-26496` terminal fail/exit 1; XML hash `7adf18d3a9cd20c2198d4cd4ccd7e0be59497e6111a73284c4977fe31b92b25d`.
- Stdlib parse: 204 FAIL, 8988 PASS, 196 ERROR concrete records; 173 raw-summary aggregate PASS members have no selectors. Derivative accounting passes, but original qualification remains `FAIL_CUSTODY_DISCREPANCY`.
- Pristine input hash `7535b9a70b0da2f36e2c9e2f0115cf70ef429d3b8152496a7f44a723033ae6a5`: 3082 concrete IDs + 173 unnamed aggregate members; 3250 PASS / 4 FAIL / 1 ERROR.

## Join

- 17 REG candidates: cut nonpass + same-kind venv-agent pristine PASS.
- 15 are env-sensitive/undecidable (`y`): exact host-bootstrap/source-identity IDs in historical cluster `root-043`; one conditional matched-kind Farm analysis is required.
- 2 are not env-sensitive (`n`): exact timeline rows in `root-007`.
- 4 matched pristine environment-bad/current-nonpass rows are `FAILS_BOTH` measurement rows with `y` (render adapter 2, live scene 1, video publication 1), retained for matched-kind follow-up only within the conditional analysis.
- 376 current nonpass rows are UNKNOWN from no exact pristine ID; 3 are N/A under explicitly absent project-only roots. No pass/nonREG conclusion is inferred from no-match. The fifth pristine timeout remains UNKNOWN because its cut match is PASS.

## Boundaries

- Farm is conditional and triggered by the 15 flagged REG candidates; no Farm body, unconditional child/core run, four-pristine-env gate, retry, or product investigation was run here.
- Raw XML and custody/KEEP artifacts remain private at their named paths. Safe source-manifest hashes genuine inputs.
- The 4GB stop was enforced before/after and across this read-only join; minimum observed available bytes were `4699422720`.

See the other assigned evidence files for the complete safe rows, aggregate accounting, cluster index, env list, historical notes, hashes, and validation.
