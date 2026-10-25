# P2 element3111: finite safe producer facts

Scope: this is a safe projection of the same retained D88b result, not an independent NO-GO verdict, reproduction, whole-path diagnosis, or source author.

## Actual result

Run `app-pin-24865fa2-p2-d88b-element-0205-1025020649-3111` on host `app-pin-24865fa2` finished `FAIL`.

- Preflight `...-31113`: PASS.
- Readiness: 1 test, 0 failures, 50.267861 s suite time; XML sha256 `a48a5fd9f52e591be54144866418750773f03c180c8bea22159581837d2271a4`.
- Original XML: 1 test, 1 failure, 60.987685 s suite time; XML sha256 `f4c596837e38fa97d9ec1fdbd766d19dbc7c0112b92dd3105a73deabfac45271`.
- Original UI5/source spec hashes did not change before versus after: the two protected spec SHA-256 values are recorded in the JSON artifact.

The first true failed predicate is `tests/e2e/local/three-products.p2-elements-assets.spec.ts:433`: `dialog.getByRole('status')` did not contain `applied` because the status element was not found within 5000 ms. Reached assertions established by the retained failure are only lines 429, 431, and 433. The response-watcher error at line 155 is a teardown follow-on after page closure; assertions after line 433 are not claimed as reached.

## Runtime phase projection

The exact qualified tuple is App `24865fa212148e9bc149a1285936372656037e55`, Agent `6386c700ee56264aebe12da4558ac74dda0d60ca`, Runtime `6634a17f3ffd885567ba3c91b6c7a560df7375a4`, Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`; the manifest/tree values and artifact hashes are in `p2-element3111-safe-facts.json`.

The retained phase file contains 128 JSONL records: 126 phase records and 2 terminal summaries, across 3 observed ordinals. All emitted records use helper schema version 1; no schema version 2 was observed. The bounded limits were 8 requests, 128 events, and 65536 bytes; truncation is false in the retained summaries.

1. Ordinal 1 completed through accept, receipt, and HTTP response, with HTTP 200 observations and 2807.839 ms Runtime dispatch total.
2. Ordinal 2 completed through accept, receipt, and HTTP response, with HTTP 200 observations and 18603.793 ms Runtime dispatch total.
3. Ordinal 3 is the intended element apply correlation. It has 16 phase records, reaches provider start, and has no observed provider end, accept, receipt, or HTTP response. Its observed phase span is 180.240 ms; its terminal summary was not emitted because dispatch did not finish.

The App diagnostic correlates `apply-1` / `scoped-commit` request start at 29143 ms to the incomplete Runtime ordinal 3. It records test outcome at 33653 ms, retained evidence at 33725 ms, teardown at 33727 ms, page close at 33746 ms, response status `UNKNOWN`, response `none`, and terminal `pending`. No later outcome is retained.

The actual launch configured a 2-second watchdog. Two private dump blocks were retained. The safe frame projection is `runtime_protocol/timeline_commit_validation.py:173 validate_commit_value`; this is a stack observation only, not causal attribution. The private dump remains mode 0600 and is represented by its size/hash only.

Unknown boundaries remain unknown: caller receipt, client-to-server arrival, exact lock-acquire wait, and any post-close accept/receipt/response. No queue timing is inferred.

## Retention and limits

Raw private phase/stack/body/browser/original outputs remain in the original result directory and were not modified. No new collector, server, browser, source, product, test, pin, manifest, Runtime, Agent, or shared dependency changes were made.
