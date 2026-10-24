**INSUFFICIENT:** retained timings confirm repeated GETs, but do not establish global-mutex cost causing the 5000 ms failure; P3’s two GETs did **not** overlap.

All times below are milliseconds relative to each archive’s `0-trace.trace` context origin. Completed ends are `_monotonicTime + time`; `-1` means unfinished in the retained trace.

| Context alias | GET ordinal | Status | Start | End | Duration |
|---|---:|---:|---:|---:|---:|
| P3 bootstrap | 1 | 200 | 12658.885 | 16214.712 | 3555.827 |
| P3 bootstrap | 2 | -1 | 16355.040 | -1 | -1 |
| P2 elements | 1 | 200 | 12530.013 | 15141.988 | 2611.975 |
| P2 elements | 2 | 200 | 12831.712 | 20087.221 | 7255.509 |
| P2 popup | 1 | 200 | 80340.873 | 84304.561 | 3963.688 |
| P2 popup | 2 | 200 | 81968.821 | 89605.918 | 7637.097 |
| P2 tour | 1 | 200 | 11633.781 | 14333.446 | 2699.665 |
| P2 tour | 2 | 200 | 14413.752 | 19387.192 | 4973.440 |

P3’s second GET started **140.328 ms after** the first ended. Elements and popup overlapped by 2310.276 and 2335.740 ms respectively; tour had an 80.306 ms gap.

| Context/page | Retained close timing |
|---|---|
| P3 bootstrap, page 2 | Actual `pageClosed`: **17916.736** |
| P3 fixture, page 1 | Exact page close UNKNOWN; context close 18337.559–18390.037 |
| P2 elements, sole page | Exact page close UNKNOWN; context close starts 26253.119, end absent |
| P2 popup, sole page | Exact page close UNKNOWN; context close 180195.509–180236.416 |
| P2 tour, sole page | Exact page close UNKNOWN; context close 109974.725–109998.081 |

Request/close clocks are corroborated by retained `context-options` wall/monotonic anchors, with residual differences ≤0.714 ms. **Generation alignment remains UNKNOWN:** lifecycle records use page `performance.now()`, and no retained `timeOrigin` anchor connects that clock to the trace clock.

P3 owner alias 1 records generation 0 `basis-read` at 4041.200, cancellation at 8116.600, then generation 1 `basis-read` at 8121.200. No request carries a generation alias. The snapshot contains **7/32 records**, accepted 7, rejected/overflow/listenerErrors 0, and no reported read/write/record losses. P2 case traces retain no equivalent generation mapping.

P2’s mandatory readiness leaf **passed**; its later originals had **3 FAIL, 5 NOTRUN**. Those three case traces use separate `native-none` fixtures, distinct from native21 readiness. P3 failed bootstrap outbox readiness; subsequent checks and Gate 5 were NOTRUN. Unfinished GET 2 does not establish server completion, lock contention, or cancellation.

Source: App `804134d74782d40855146aa568ff289200b79142`, tree `8437e47666853b62e03a58af3716235346316fba`. Exact Git blobs:

- `client.ts`: `6e9a894d09959ed9fa8f1c0c6f01b9423441c59b` — history uses `withSession`.
- `useTimelineSave.ts`: `e79e083dbca9d67fbc0c66051a365ad59b897ff5`.
- `timeline-diagnostics.ts`: `233135cdc0101a5fe3191010ce6a4011d0203b2c`.

Artifact SHA-256 values, under the specified ORCH `tests/` directory:

| Artifact alias | SHA-256 |
|---|---|
| `3362` mounted-readiness `trace.zip` | `0cd0b09473f1c98ffa411d4d4924a3d6706f1320bd36e310dfb0ce7c7532519c` |
| `12221` elements `trace.zip` | `40e41d21d7eedafd966ec1bac8c09fec2ee35f8f86a727d5b6bb67fa6550e2a0` |
| `12221` popup `trace.zip` | `28ef30d2cf6d41ddf7c32333733683ef36ad5cc88901adc2ef79171e5528097f` |
| `12221` tour `trace.zip` | `6ba0979ce2181bf35e091e45a9a8256fb1766d5663da155f02e8771c150ad024` |
| `3362` lifecycle JSON | `679cc75ec9507d42538d4c8364ba28b9c3355fe0b4b6c8964336e3f188cee77b` |

Read-only Python extraction covered four archives and eight history GETs. **No tests or new runs executed.** `git diff --check` passed; worktree remains clean. Commit message and `DONE` created. Runtime memo and App coalescing remain with their assigned owners; the causal clock/request joins remain unverified.