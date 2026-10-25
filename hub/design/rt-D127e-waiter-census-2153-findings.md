# D127e findings

## Result

The historical source census is complete and read-only. D112 reconnect/WAL recovery can wait on the actual element path. This is the D130-held SWAP/WAL path, so work stops at source evidence; no authoring, test, qualification, retry, alternate route, or cross-machine execution was attempted.

## Ranked source candidates

1. `Runtime runtime_protocol/timeline_commit_store.py:315` — `_reestablish_connection` takes the store `RLock` with no timeout after `_store_version` sees DB/WAL identity change. Its same-connection branch reopens at lines 333-338; `Runtime runtime_protocol/store.py:1230-1246` uses a 10-second SQLite connect/busy timeout. This is the most likely waiter by source evidence, but occurrence in 32016/15200 is unproven.
2. `Runtime runtime_protocol/timeline_commit_store.py:383` and `timeline_commit_port.py:221` — nested read locks around every provider port read; max UNKNOWN/unbounded. These can be ordinary contention or the D112 entry point.
3. `Runtime runtime_protocol/timeline_commit_execution.py:341` — same-idempotency-key execution serialization; max UNKNOWN/unbounded. The retained captures do not expose exact lock-wait duration.
4. `Runtime runtime_protocol/store.py:933` — `BEGIN IMMEDIATE` in acceptance; SQLite busy timeout is 10 seconds per busy operation, but total request bound is UNKNOWN.
5. `Runtime timeline_commit_execution.py:395` — synchronous provider call, max UNKNOWN/unbounded. It accounts for the measured 13.781 s / 12.290 s provider intervals, but no source or retained safe frame proves those intervals are waiting.
6. `Agent astrid/sdk/timeline/commit.py:1336` — three-attempt `StaleHead` retry loop. It is bounded, has no sleep/backoff, and is not itself a waiter.

## Retained evidence limits

32016 is independently qualified at 21.741532 s handler / 13.780929 s provider; 15200 at 19.558850 s / 12.290285 s. 32016's published top leaves and 15200's published inclusive rows contain no explicit `lock.acquire`, `selectors.select`, or `sleep` marker, but raw per-sample membership is EXACTMISSING; 15200 exact cProfile top-40 and edges are also EXACTMISSING. Inclusive sampling cannot distinguish CPU from waits.

10721 request 2 is explicitly NOT the element, and the direct 1.75 s replay is not a same-state comparison. Neither is used to attribute a waiter.

## Exclusions

Agent's standalone `sdk/timeline/store.py` has file-lock sleeps and subprocess helpers, but the historical provider handler does not import/call them. Runtime media ffmpeg subprocesses, task retry/sleep paths, worker Event waits, and unrelated lifecycle waits are not reachable from `_timeline_commit` through the Agent provider and return.

## D130 disposition

Source evidence identifies the held D130 path. The next step belongs to the orchestrator/owner after the hold is resolved; this worker does not propose a fix or qualification action.
