# P2 parent 12208 safe evidence handback

The retained browser trace classifies the intended parent-move commit POST as **absent**: 245 records contain 22 POSTs, but zero POSTs match the commit endpoint. The observed POST categories are one Astrid handshake, five Runtime handshakes, and sixteen Runtime inspect requests; all observed POST responses were HTTP 200. No intended commit status, error code, safe error message, or request duration is available. The 90,000 ms value is the Playwright response-wait ceiling, not a request duration.

The original run reached readiness PASS and then terminal NO-GO at the response wait. Accepted-reply inspection, field-delta checks, reload, guarded undo, and closure were unreached. No Runtime cause is established from the timeout.

The private Runtime phase artifact contains ordinals 1 and 2. Both have the exact phase sequence `dispatch_queue → handler_entry → authorization → coordinator_admission → coordinator_lock → provider → accept → receipt → http_response`, with HTTP 200 and no error code/message. Ordinal 1 has provider 2093.717–3427.728 ms, accept 3031.407–3427.570 ms, receipt 3045.154–3427.266 ms, and two response observations at 3771.058–3771.263 and 3771.575–3772.190 ms. Ordinal 2 has provider 9434.211–17759.338 ms, accept 13491.302–17758.465 ms, receipt 13594.041–17755.980 ms, and two response observations at 22491.819–22492.285 and 22493.080–22496.275 ms. Neither ordinal is attributable to the intended parent gesture; no intended-parent Runtime ordinal is established. The detailed safe values are in the JSON/TSV companion files.

Source hashes: runtime phase JSONL `65936e06a366da94234047b2bbbe53433d6a3553819c1ad842612ffc36f05b80`; browser trace ZIP `1e69066591f18bdc4163e9fd59e024656b68ad7fd2e7532f37b63744aaa2f7ed`; service manifest `a0cb6b2c87f268dbb0ea0fb189cbf005ab83191ebf23c636cc70f298518806ab`; JUnit `1740913b9c9466de0addec1df10cfd149c1f0f02849434bb9abb187e482677e1`.

Single 5678 remains the independent PASS and was not reviewed. Raw auth, body, keys, URLs, IDs, and private dumps are not included here. No diagnosis, new collector, reproduction, or product/test change was made.
