# D127e independent waiter review

## Result: PASS

The completed `rt-D127e-waiter-census-2153` evidence is substantively correct and within scope. The historical Runtime `ab1e4f6141987706132916e2da16477f5a019464` and Agent `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2` source tuple was used read-only. Composition `tl/integration` was the sourcebase context; it was not substituted for the historical behavioral evidence.

## Full production chain

`Runtime server._timeline_commit:300` → `RuntimeService.commit_timeline:2469` → `_execute_timeline_commit:2486` → authorization and store/coordinator setup → `CommitExecutionCoordinator.execute:365` → `_execution` guard `:328` and matching idempotency entry lock `:341` → `port_factory:2541` → synchronous `provider.commit:395` → Agent `RuntimeCommitService.commit:1160` → provider reads and `commands.execute:1331` → bounded `range(3)` stale-head loop `:1336` → `port.preview:1443` or `port.accept:1444` → Runtime `RequestCommitPort._read:217` / `TimelineCommitStore` history and validation scopes → conditional `_store_version:349-357` / `_reestablish_connection:307-347` → acceptance `_accepting:455` / `BEGIN IMMEDIATE` at `runtime_protocol/store.py:933` → outcome verification and port close `timeline_commit_execution.py:400-408` → HTTP return.

The production caller is the unchanged `_timeline_commit` → registered Agent provider route. The C0/F wire-shape list is retained as scope: request fields are `api_version`, both scope IDs, both base IDs, `commands[{schema_version,op,version,select,args}]`, label, steps, merge, reads, idempotency, dry-run and annotations; replies are `accepted|merged`, conflict, invalid and preview forms as specified. This review does not claim frozen R4 implements later v2 schema behavior.

## Ranked waiters and max waits

1. `runtime_protocol/timeline_commit_store.py:315`: conditional `store._mutex` acquisition in D112 recovery. It is an unbounded/no-timeout `RLock` acquisition when `_store_version:353-357` detects changed DB/WAL/connection identity.
2. `runtime_protocol/timeline_commit_port.py:221` and `timeline_commit_store.py:383`: outer provider-read and history-read transaction `RLock` acquisitions. Both are unbounded/no-timeout; they are ordinary contention points and the D112 entry path.
3. `runtime_protocol/timeline_commit_execution.py:341`: matching idempotency-key entry lock, unbounded/no-timeout. Hash mismatches refuse rather than wait.
4. `runtime_protocol/store.py:933`: `BEGIN IMMEDIATE`; an SQLite busy operation can wait up to the configured 10 seconds, but the total route bound is unknown/unbounded.
5. `runtime_protocol/timeline_commit_execution.py:395`: synchronous provider call, no source timeout; the elapsed provider interval is not proof of waiting.
6. `astrid/sdk/timeline/commit.py:1336`: exactly three attempts, no sleep/backoff; bounded retry candidate, not an elapsed-wait attribution.

The remaining census entries are reachable and correctly classified: service mutex family (`service.py:2438,2464,2517,2538,2625`), evaluation/store mutex family (`timeline_commit_store.py:172,583,977,1026,1075,1100,1150,1205,1273,1792,1834`), authorization `store.py:1516`, SQLite open/busy setup `store.py:1230-1246`, provider call Agent endpoint `commit.py:1160`, and conditional restore preflight `timeline_commit_port.py:155` / `store.py:6210`. Restore is not the ordinary element route.

Two additional source sites are nested reentrant acquisitions, not missing independent waiters: `timeline_commit_port.py:875` (`MediaReads.selection` under `_read:221`) and `timeline_commit_store.py:264` (`clear_replay_memo` while the store mutex is held). They are covered by their outer lock paths.

## D112 and evidence limits

D112 reconnect/RLock/SQLite-10s is `REACHABLE_CONDITIONALLY`: provider port read → history read scope → `_read_transaction` → `_store_version`; if DB/WAL identity changes, `_reestablish_connection` first takes the store RLock and same-connection recovery closes/reopens through `_open`, which uses `sqlite3.connect(timeout=10)` and `PRAGMA busy_timeout=10000`. This is a source fact only and is the D130-held SWAP/WAL path. No occurrence, duration, or causal attribution is established.

The retained element boundaries remain separate and safe:

- 32016: handler 21,740.631 ms, provider 13,780.929 ms, dispatch wall 21,741.532 ms; handler-minus-provider 7,959.702 ms and dispatch-minus-handler 0.901 ms; 828 samples, 15 lost.
- 15200: handler 19,557.721 ms, provider 12,290.285 ms, dispatch wall 19,558.850 ms; handler-minus-provider 7,267.436 ms and dispatch-minus-handler 1.129 ms; 737 samples, 17 lost.

Both captures have missing raw per-sample membership for explicit lock/select/sleep markers; 15200 also lacks exact cProfile top-40 and edges. Inclusive sampling/rows cannot distinguish CPU from blocking waits. 10721 request 2 is explicitly not the element request. The direct 1.75 s replay is not a controlled same-state comparison. No 85% inference or non-element timings were imported.

Static source scans found no reachable `time.sleep`, `selectors.select`, Event/Condition wait, or subprocess wait in this provider chain. Unrelated Agent standalone-store sleeps/subprocess helpers and Runtime media/worker/lifecycle waits are excluded by call reachability. No authoring, live body, profiler, collector, benchmark, qualification, retry, alternative route, or D130 transfer was performed.

One non-blocking citation correction: the census call-path parenthetical labels lines 1792/1834 as `store.py`; those lines are in `runtime_protocol/timeline_commit_store.py`. The source behavior and line numbers are otherwise correct.
