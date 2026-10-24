# P2 D84a finite existing-evidence handoff

This is a bounded Runtime handoff, not an independent NO-GO verdict or causal diagnosis. It uses only the retained same-run manifest, XML, element diagnostic, allowlisted phase JSONL, and private stack metadata.

## Source and outcomes

The retained four-pin source tuple is App `bceb0350326f22beefdde5c5ba275412bb09b419`, Agent `039ff2c2187d02b723074a8a6dfcbc6a70544c19`, Runtime `732c48c6f5a9441a65c61b24595d454a1cd3e180`, and Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`. The App tree is `46ad4dde505a376e22026c3377615a5fca05a55e`; the retained before/after test hashes are identical.

The readiness XML is 1/1 PASS in 9.19 s. The original mounted-element XML is 1/1 FAIL in 22.517 s at the 5 s UI assertion. The retained run summary says approximately 172 s of service time; the manifest start/end timestamps span 167.460 s. Eventual element outcome remains UNKNOWN.

## Request-correlated phase facts

The allowlisted phase capture has 123 JSONL records including three summaries, `truncated=false`.

| ordinal | logical phase counts | duration | last phase | terminal observation |
| ---: | --- | ---: | --- | --- |
| 1 | handler 1; authorization 14; admission 1; lock 1; provider 1; accept 1; receipt 1; HTTP response 2 | 1909.237 ms | `http_response` | accept, receipt, and HTTP response observed |
| 2 | handler 1; authorization 23; admission 1; lock 1; provider 1; accept 1; receipt 1; HTTP response 2 | 17251.351 ms | `http_response` | accept, receipt, and HTTP response observed |
| 3 | handler 1; authorization 5; admission 1; lock 1; provider 1; accept 0; receipt 0; HTTP response 0 | 122.618 ms | `authorization` | provider observed; terminal Runtime phases not observed |

The element-correlated ordinal is **3**: it is the incomplete Runtime ordinal corresponding to the retained p2-element scoped-commit/apply lifecycle (`apply-1`). Ordinals 1 and 2 are earlier completed/seed-control observations and must not be substituted for the element request.

There is an important boundary distinction. App transport metadata records a terminal `response` for ordinal 3 after 46 ms, but the retained element diagnostic has response status `UNKNOWN`, response `none`, and terminal `pending`. Thus this is a transport-terminal observation without a retained response status/body, while Runtime has no accept, receipt, or HTTP-response phase for ordinal 3.

The diagnostic records request start at 36,433 ms, test outcome at 41,045 ms, teardown at 41,072 ms, and page close at 41,087 ms. The original UI assertion budget was 5,000 ms. The retained facts do not prove the 30 s SDK or 120 s outer limits were reached, and `truncated=false` means this is a missing terminal observation rather than phase-budget truncation.

## Private dump and safe frame

The private phase JSONL is 14,376 bytes, mode `0600`, SHA-256 `1856981624e20d669028f39a16b92e53a764bdc7a5a0d9da50304fcd7caee194`. The private stack dump is 5,868 bytes, mode `0600`, SHA-256 `e45bf1c3d586cc38a4967794c7ac62500b4fcdf74739b8e64dc26344055336f6`; it contains 5 threads and 60 observed frames. The retained element diagnostic is 2,344 bytes, mode `0600`, SHA-256 `5281af9b141c09bce9d73370e0de74746efc73768c4c716f6a0f2c2cceeda84a`. Ordinal-3 terminal metadata is 201 bytes, mode `0600`, SHA-256 `b2b8319d9877942a8e35ecbbddb22b0866431621ff72754c067a461654ebed28`.

Safe provider frame: `astrid/sdk/timeline/commands.py:137 validate_command`. The retained safe call chain continues through `commands.py:223 execute`, `commit.py:1331 commit`, `runtime_protocol/timeline_commit_execution.py:91 _execute`, `runtime_protocol/timeline_commit_execution.py:71 execute`, `runtime_protocol/service.py:2499 _execute_timeline_commit`, and `runtime_protocol/service.py:2444 commit_timeline`.

Comparison to the previous exact provider-history boundary is **UNKNOWN**: the prior handoff was explicitly formatting-only for this task, and no previous boundary is present in the allowed same-ID retained sources.

No element payload dump is retained in the allowed sources. Raw stacks remain private and are not reproduced. No raw body, credential, key, URL, or identifier is included. Runtime owns product-cause diagnosis; no causal closure is claimed.
