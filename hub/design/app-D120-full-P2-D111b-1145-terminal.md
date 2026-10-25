# D120 full P2 terminal

The one normal D66 `p2` body reached terminal `FAIL` (exit 1) after 643 s central duration; D66 manifest duration was 637.532 s. Readiness passed 1/1. The original tour was 5 PASS, 2 FAIL, 1 NOTRUN.

- PASS: popup ADD, parent move, transition None single, transition None bulk, automatic child placement.
- FAIL: popup SWAP at `tests/e2e/local/three-products.p2-popup.spec.ts:495`, expected accepted HTTP 200 but observed public 409 `history_unavailable`.
- FAIL: element edit at `tests/e2e/local/three-products.p2-elements-assets.spec.ts:1052`; applied completion did not settle and the retained safe error reports the target page/context/browser closed. Backend outcome is UNKNOWN.
- NOTRUN: registerAsset at `tests/e2e/local/three-products.p2-elements-assets.spec.ts:1133`, serially not entered after the element failure.

Exact JUnit outputs: `d66/readiness.xml` SHA-256 `aee8a153c0f5dd86b21aa6b4a40125d3636642a975e29e9dcf1a81ff3dd5560c`; `d66/p2.xml` SHA-256 `b349d93a672f3b5d8996eea63824035b06605dee0169190f86405efc0b0f8b8c`; manifest SHA-256 `892c089c4a03c04c7ca12f487766116e39595be7970bd1a733418e65356588ca`. The four source hashes were unchanged before/after.

Runtime-private searches covered all six phase files and all six stderr files listed in `terminal.json`, including every repeated-start namespace. Four populated phase files reached `http_response`; one had redacted authorization/provider raises with HTTP status unknown; one was empty. No D102 reason tag, class chain, or redacted frame file-line-function was retained there, and all searched stderr files were empty. The retained element diagnostic files were byte-identical (SHA-256 `3ebfb19267ac21080a387bd2a0464d503be26152bb254c075932ee544d402821`) and contain only safe lifecycle facts: terminal `pending`, correlation `apply-1`, page closed, reason/class/frame UNKNOWN.

No raw stderr, request/response body, auth, URL, opaque payload, or private stack was exported. No retry, collector, or second body was run.
