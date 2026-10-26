# F D141y custody correction

Result: **F1 remains substantiated; historical custody is unresolved and disclosed.** This is an immutable derivative of the retained author/reviewer evidence, not a new review PASS and not a delivery-build run.

The original result remains byte-exact: one canonical `delivery-build --dry-run` invocation, exit `2`, ordinary App ancestry refusal (`fc24f84994dc36cfae9349112782ab4d91dbc73b` → `4de54db14bdc9ddc2ce2e5887258b03acbffd30d`), exact tuple SHA `6fe1b04ca64f38cc8a524bc397950df5a6bce835be614341a70e2c163d253c4d`, and raw stderr SHA `8723a85802bb604561bf76ba507e71dc13fc4d4c4ae9bda553b32fee0fb90c95`. All four patch/tree/bundle/apply results remain **NOT_REACHED**. No ZIP or publication exists.

The old author transcript proves only that a sampler command was started (retained `log.txt` line 853). It does not retain the original sampler PID, a terminal/TERM record, a kill return, or a wait/reap return. The later `ps` poll of guessed PID 3265 (line 3880) is not terminal or reap evidence. `finalize.log` proves wrapper finalization/cleanup, not sampler reaping. The author’s “reaped” sentence is therefore retracted in this derivative. Original files and original FAIL review remain preserved with hashes in `source-manifest.json`.

This worker made a separate present-time observation only: sampler PID 8 ran for two 5-second samples above the 4,000,000,000-byte stop, `kill -TERM` returned 0, `wait` returned 143, and PID 8 was reaped. `sampler-start.json`, `sampler-terminal.json`, `sampler-reap.json`, and `disk-trace.txt` are not historical evidence and do not repair F1.

No delivery-build invocation, retry, subset run, fetch, checkout, source change, product/test/kit work, ZIP, publication, or full/targeted test run was performed.
