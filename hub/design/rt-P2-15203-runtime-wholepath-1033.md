# P2-15203 Runtime whole-path investigation

Result: `PASS_SOURCE_FACTS`; attribution: `UNKNOWN`. This was read-only. No Runtime product, test, generated, pin, kit, registry, collector, or body file changed.

## What the retained packet proves

The App D118 original P2 run has readiness PASS and outcomes 2 PASS, 2 FAIL, 1 ERROR, 3 NOTRUN. The two credited cases are popup ADD and automatic child placement. SWAP is an initial 409 refusal with `history_unavailable` at 23.149 seconds. Element failed separately at 11.905 seconds; parent separately waited 90 seconds; serially dependent cases were not run. Runtime stderr is empty and the retained diagnostic has no safe reason, class chain, or correlation field: correlation is explicitly UNKNOWN. No backend result is inferred from client waits.

The packet’s exact four-repo tuple and source hashes are in the companion JSON. Payloads, credentials, private URLs, service IDs, and stack contents are not reproduced.

## Safe source anchors

- Registration and production entry: `runtime_protocol/service.py:2391-2411`, `:2447-2537`.
- Coordinator execute/lookup/provider/re-lookup: `runtime_protocol/timeline_commit_execution.py:222-275`.
- Agent port ancestry/history lookup and refusal mapping: `runtime_protocol/timeline_commit_port.py:225-255`.
- Accepted-history graph and replay: `runtime_protocol/timeline_commit_store.py:601-695`, `:697-783`, `:808-838`, `:862-875`.
- Equality and declared-read guards: `runtime_protocol/timeline_commit_producer.py:60-70`; `runtime_protocol/timeline_commit_auth.py:221-228`, `:245-263`.
- Sequential input/output and effect projection: `runtime_protocol/timeline_commit_auth.py:2868-2879`; D115’s `step_output`/materialized-image change is at `:765-820`.
- Public `history_unavailable` construction/preservation: `runtime_protocol/timeline_commit_baseline.py:24-27`; `runtime_protocol/timeline_commit_port.py:89-100`.

The production path is therefore App → registered Agent provider → Runtime coordinator/port → history verification/authentication. App owns browser request/parent attribution; this investigation did not duplicate that trace or infer a missing POST.

## Comparison

The recorded App packet uses Runtime `d23a8` / tree `6283b5…`, the released D112a source. Current normal `369ffa` keeps Runtime store, port, and producer byte-identical to `d23a8` and adds the existing D115 Runtime-auth change. D115 makes authenticated sequential landing output the expected intermediate image, aligns materialized images against that authenticated projection, and compares the projected result to the landing image. Failure mapping is otherwise unchanged.

Retained D112a native evidence is bounded positive evidence for registered-provider seed → ADD → SWAP → native Undo, startup/refusal control, and final history. Its own release note says it is not the original SWAP-409 proof and does not prove byte-identical source-object identity.

The D118 packet does not retain the exact SWAP request, Agent record, observed/base/head pins, authenticated history entry, failing predicate, or correlation. It therefore cannot show whether SWAP entered D115’s sequential path, whether `covers`/effect/unchanged-image auth rejected it, whether a history guard rejected it, or whether the Agent producer supplied a non-authentic record. No Runtime defect, proved-fixed seam, or Agent producer seam is demonstrated.

## Bounded handback

Keep the original refusal and current guards. The missing records needed for a safe attribution are: the redacted SWAP request and response envelope; registered Agent producer output; observed/base/head pins; authenticated history entry; and the first correlated Runtime failure predicate. App owns acquisition of browser/parent trace attribution. No alternate route, guard relaxation, fabricated history/effect ordinal, or source/test change is justified.

