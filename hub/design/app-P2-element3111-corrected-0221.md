# P2 element3111: finite safe producer facts (corrected correlation)

This corrected packet supersedes the immutable `app-P2-D88b-element3111-facts-0212` packet. It is a safe projection of the same retained D88b result, not an independent NO-GO verdict, reproduction, whole-path causal diagnosis, or source author.

## Correction ledger

The prior packet said that `intended_request_dump_correlation.dump_intent` was a watchdog dump for Runtime ordinal 3. That attribution is unsupported. The retained helper source (`tests/helpers/p2_commit_phase_capture.py`, SHA-256 `812bcda5fb0eea60f4a66225e454400b16c296ce12c982963ac47f7de5d6d6fa`) shows that `_watchdog_fire` calls `faulthandler.dump_traceback(..., all_threads=True)` without writing an ordinal header, request identity, or timestamp. The raw sink is two concatenated dump blocks, and `_summary` contains no watchdog fields. Therefore dump request identity and dump-to-ordinal mapping are `UNKNOWN`; the safe frame is an observed raw-stack frame only and is not attributed to the element or ordinal 3.

The source default `max_watchdog_captures=2` is global to one capture instance. The actual ordinals 1 and 2 had dispatch totals of 2807.839 ms and 18603.793 ms, both beyond the configured 2-second timer. Either or both may have consumed the two captures before the intended element ordinal 3. This is a budget possibility, not a per-block mapping. The App diagnostic still safely correlates `apply-1` / `scoped-commit` to incomplete Runtime ordinal 3; that is separate from dump correlation.

## Actual result

Run `app-pin-24865fa2-p2-d88b-element-0205-1025020649-3111` on `app-pin-24865fa2` finished `FAIL`.

- Preflight `...-31113`: PASS.
- Readiness: 1 test, 0 failures, 50.267861 s suite time; XML SHA-256 `a48a5fd9f52e591be54144866418750773f03c180c8bea22159581837d2271a4`.
- Original XML: 1 test, 1 failure, 60.987685 s suite time; XML SHA-256 `f4c596837e38fa97d9ec1fdbd766d19dbc7c0112b92dd3105a73deabfac45271`.
- Exact source heads, trees, schema digest, manifest hash, and protected UI/source hashes are retained in the JSON artifact.

The first true failed predicate is `tests/e2e/local/three-products.p2-elements-assets.spec.ts:433`: `dialog.getByRole('status')` did not contain `applied` because the status element was not found within 5000 ms. Reached assertions established by the retained failure are only lines 429, 431, and 433. The response-watcher error at line 155 is a teardown follow-on after page closure; assertions after line 433 are not claimed as reached. The original first-failure timing and XML remain authentic and unchanged.

## Runtime phase projection

The exact qualified tuple is App `24865fa212148e9bc149a1285936372656037e55`, Agent `6386c700ee56264aebe12da4558ac74dda0d60ca`, Runtime `6634a17f3ffd885567ba3c91b6c7a560df7375a4`, Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`; manifest/tree values and artifact hashes are in the JSON artifact.

The retained phase file contains exactly 128 JSONL records: 126 phase records and 2 terminal summaries, across 3 observed ordinals. All emitted records use helper schema version 1; no schema version 2 was observed. The bounded limits were 8 requests, 128 events, and 65536 bytes; the retained summaries report `truncated: false`. Schema version 1 already has observed `dispatch_queue` and `handler_entry` records plus safe summary durations; lack of schema version 2 does not mean those queue fields are absent.

1. Ordinal 1 completed through accept, receipt, and HTTP response, with HTTP 200 observations and 2807.839 ms Runtime dispatch total. Its safe summary durations are dispatch queue 1.523 ms, handler 2806.316 ms, provider 2093.870 ms, and response write 1.735 ms; exact lock-wait and caller-receipt durations are unavailable.
2. Ordinal 2 completed through accept, receipt, and HTTP response, with HTTP 200 observations and 18603.793 ms Runtime dispatch total. Its safe summary durations are dispatch queue 2.866 ms, handler 18600.927 ms, provider 11851.016 ms, and response write 15.101 ms; exact lock-wait and caller-receipt durations are unavailable.
3. Ordinal 3 is phase-correlated to the App `apply-1` / `scoped-commit` request. It has 16 phase records, reaches provider start, and has no observed provider end, accept, receipt, or HTTP response. Its observed phase span is 180.240 ms; no terminal summary was retained because the dispatch did not finish.

The App diagnostic records request start at 29143 ms, test outcome at 33653 ms, retained evidence at 33725 ms, teardown at 33727 ms, and page close at 33746 ms. It records response status `UNKNOWN`, response `none`, and terminal `pending`; no later outcome is retained. This request-to-ordinal correlation does not identify either raw watchdog block.

The 128-record cardinality and `truncated: false` summaries establish what the bounded observer retained. They do not establish an unobserved post-close outcome for pending ordinal 3. There is no causal queue, lock, or wait claim: caller receipt, client-to-server arrival, exact `threading.Lock.acquire` wait, and any later accept/receipt/response remain `UNKNOWN`.

## Watchdog and raw-stack limits

The actual launch configured `watchdog_seconds=2` through the existing `sitecustomize.py` loader (SHA-256 `83c28b437417753a221e0fec36047dd6bb267256366dd4acacb8ef8d8137615e`). The helper arms one daemon timer per active dispatch. With a 2-second setting there is no follow-up timer: the request-owned follow-up is enabled only when `watchdog_seconds == 5.0`. A request timer is cancelled at dispatch return, including raised or aborted returns; `stop()` cancels timers for still-active requests. `_watchdog_fire` checks that the request remains active and unfinished, the timer token is current, and the global capture count is below 2 before appending a raw all-thread dump.

Two private dump blocks were retained at `d66/runtime-private/p2-commit-phase.stacks.txt`, mode `0600`, size 15077 bytes, SHA-256 `0bf7f3e3eae3873147124a6f9d73a2f32c9489a047404c7993aa47e13fbb02ab`. The file has no ordinal/request header, so block order-to-ordinal mapping is `UNKNOWN`. The safe frame projection is `runtime_protocol/timeline_commit_validation.py:173 validate_commit_value`; it is an observed raw-stack frame only, not a causal diagnosis, independent verdict, or element/ordinal attribution.

## Retention

Raw private phase, stack, body, browser, and original output files remain in place and were not modified. No new collector, source, product, test, pin, manifest, Runtime, Agent, or shared-dependency change was made. Old element8897 remains a distinct result and is not combined with this run.
