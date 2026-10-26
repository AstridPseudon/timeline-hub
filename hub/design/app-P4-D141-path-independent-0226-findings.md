# D141 P4 path-independent review

## Verdict

`PASS_SOURCE_PATH_UNRELATED_XML_CUSTODY_PENDING`.

The App 867-to-5fe five-file delta cannot reach the actual registered P4 body. The launcher validates the App pin as four-way metadata, but its preflight/body import and execution roots are Agent and Runtime. The three selected Agent tests instantiate the Runtime daemon/HTTP handler, use the generated client/provider, and read canonical history through the Runtime routes. The frozen Composition 635f pin is documentary/preflight package identity only.

This is a bounded source/import/client/dataflow result. It is not an execution result and not cumulative P4 GO.

## Findings

1. **Actual process preserved.** Agent launcher blob `f1bde17ea107a8b669cb6924fbdbd2f3979da988` at lines 24-58 guards all four pins; lines 125-161 run with `PYTHONPATH` containing only Agent and Runtime. The selected test blobs are `033482ec...`, `afc9c112...`, and `192efbfa...`; their imports and test bodies are cited in `source-map.json`.

2. **Full execution/dataflow chain is real in the recorded process.** `test_native_batch_ingress.py` blob `b002de2e...` lines 43-109 constructs `RuntimeDaemon` and `RuntimeHandler` transport. Runtime blobs route POST commit through `server.py:301-341,405-414,552-553`, `service.py:2468-2525`, and `timeline_commit_execution.py:365-431`; history is `server.py:575-585`.

3. **App delta is unrelated to that body.** The exact five changed App blobs and SHA-256 values are recorded in `review.json`. They affect App provider pairing, placement outbox/mutation setup, shot-group commands, and the App-only mock. No changed App file is imported by the launcher or selected Agent tests, and the App path is not an execution root.

4. **0225 check.** `tl/app-P2-D141-materialization-expectation-0225` exists and resolves exactly to 5fe3e4d/tree af5179. Its 867-to-ref delta is the same five files; it adds no P4 executable edge.

5. **Custody boundary.** The recorded XML path and stale alternate path are absent here. The recorded hash is `afca45b778f118b22f30e2cac08654a902dd86241b76442f146ae0ad8623316d`; it was not parsed or rehashed in this review. Preserve old 0114 `FAIL`, historical 10086 3/3 result, correction0159 metadata-only scope, and queued/unstarted 19479.

## Contract preservation

C0 request/reply/patch/conflict/undo/history requirements were checked against `contract/commit-v2.md` sections 1-5 and 7. The required request fields, accepted/merged receipt fields, conflict/invalid/preview fields, and original Agent test tails/input/assertions remain unchanged. This review does not re-execute or re-qualify them.
