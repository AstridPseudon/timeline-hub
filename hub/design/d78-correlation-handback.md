# D78 retained-input correlation handback

Status: **PASS for handback completeness**. This is a read-only diagnostic return, not a causal verdict, gate credit, or closure.

## Result

The single genuine 2-second watchdog dump belongs to local request ordinal 1. Request 1 ran from offsets `4556.035–7300.056 ms`; its handler envelope was `2.742991 s` and it completed normally with local HTTP 200. The dump was captured at `2026-10-24T20:05:17.584Z`, while request 1 was still active. The phase sink is monotonic-relative, so the monotonic-to-wall offset is not directly serialized; the ordinal is nevertheless fixed by the watchdog timestamp, retained JUnit chronology, request ordering, and request 1 being the only active dispatch at the dump boundary. This was not inferred from file presence.

Request 2 ran from `17454.444–51952.355 ms` (`34.497911 s` observed span; `34.498 s` reported). Its SDK 30-second boundary is offset `47454.444 ms`. The Runtime continued into its response path: local response status 200 was selected, one response write ended, and a later response write was marked `raised` at `51952.355 ms`. That local 200 is not evidence that the caller received a response.

## Timeout meaning

- SDK: `astrid_runtime_client/generated.py:639,664,679-685` sets the default transport timeout to 30.0 seconds and maps a timeout to `transport_timeout` / `runtime request timed out`. This is the observed caller-side failure for request 2.
- App: `tests/e2e/local/support/harness.ts:1024-1025` sets the enclosing Python process ceiling to `120_000` ms. That ceiling was configured but did not fire; the retained failure is the SDK `transport_timeout`, not an outer Node process timeout.
- Runtime: `runtime_protocol/server.py:321-341` can select local status 200 and then raise while writing. The phase sink intentionally retains only `start`, `end`, `raised`, bounded counts, relative times, and allowlisted status; it does not retain exception text.

Thus “raised”, “locally HTTP 200”, and “caller timeout” are three distinct observations: response-path exception state, Runtime-selected status, and SDK caller outcome.

## Safe phase record

The bounded vocabulary, in order, is:

`handler_entry → authorization → coordinator_admission → coordinator_lock → provider → accept → receipt → http_response`

Request 1: authorization count 14; all other non-response phases count 1; response count 2; all terminal states normal. Request 2: authorization count 23; all other non-response phases count 1; response count 2; response terminal states `end, raised`. Both response records carry local status 200. Exact per-phase starts, ends, envelope durations, counts, local ordinals, codes, and end-state meanings are in [d78-correlation-handback.json](./d78-correlation-handback.json).

The phase code is schema version 1. The only externally observed error vocabulary is `transport_timeout`; no phase record invents or asserts a Runtime domain error code.

## Retained artifacts and source facts

- Phase sink: `.../app-pin-860e9755-d78-watchdog-live-2001-1024200242-14383/d66/runtime-private/p2-commit-phase.jsonl`, 108 lines, mode `0600`, SHA-256 `8966b306726f91a805342fff0a1ed3b43317acda53c85218176bb47eeb77b3a9`.
- Raw stack: same directory, 57 lines / 4,206 bytes, mode `0600`, captured `2026-10-24T20:05:17.584Z`, SHA-256 `eb2e55e78734850ad08f7f36724f3e316e4535f8fec54591d6ac645796276f04`.
- XML: readiness `1/1` pass (`d66/readiness.xml`); original P2 element `1` test with `1` error (`d66/p2-element.xml`).
- Safe stack frame tuples: `p2_commit_phase_capture.py:_watchdog_fire:226`, `auth.py:_read_bytes:69`, `auth.py:_read_actor:102`, `server.py:_authorize_timeline_commit:276`, `timeline_commit_store.py:_validate:942`, `timeline_commit_store.py:accept:1229`, and `commit.py:commit:1444`.
- Bounded all-thread categories: one request-thread auth/validation chain, two server selector waits, and one CLI main thread.

Raw stack, auth, body, key, URL, realm, and PID identifiers are not exported. Existing raw files remain unchanged. Runtime owns causality/fix; recommended next step is its local fix loop using this handback.
