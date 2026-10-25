# D124 final helper review facts

## Verdict

- SOURCE: **PASS** for the exact cumulative `181952babeb3454e5d18f441dcb355f203ed775b` helper against Runtime `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`.
- ATTACH: **PENDING**. This review does not qualify the App normal hook, a production preflight, a full-body tour, element causality, or P2 GO.

Reviewed helper SHA256:

`6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760`

Exact bytes are in `evidence/p2_commit_phase_capture.py`.

## Independent source findings

The old protected-1304 FAIL is corrected in actual new source, not by assertion:

- `arrival` is never begun or emitted from the dispatch trace. Its summary is `unsupported`, with a reason naming the absent earlier socket/server-accept hook and `network_arrival_ms: null`.
- The real observed dispatch boundary is `RuntimeHandler._dispatch` entry; the real handler boundary is `RuntimeHandler._timeline_commit` entry. Runtime 5e9ad contains those names unchanged. Coordinator, port, store, authorization, and response mappings also match actual Runtime definitions.
- `dispatch_to_completion_wall_ms` is explicitly dispatch-entry through `_dispatch` return and is the sampler denominator. Body receive, network arrival, caller receipt, and exact lock wait remain unsupported/null rather than inferred.
- Sampler CPU is labeled capture-wide and explicitly not attributed per request. Samples select active request thread identities, de-duplicate safe frame identities within each sample, and retain sample loss counts and selected-request evidence.
- Each capture carries a UTC anchor, relative monotonic timestamps, PID, process birth ticks, and a distinct process/capture namespace. Correlation retains only method, the static sanitized commit route template, and SHA256 of the exact Idempotency-Key.
- Private poison-marker checks found no request body, raw key, authorization, credentials, opaque IDs, private URL, or exception text in safe JSON export. Existing private watchdog stack output remains private harness evidence.
- `git diff` from Runtime 5e9ad contains only the two assigned test/helper files; Runtime product source is unchanged.

## Attachment route and limitation

The App `fe3309dba4520835a685f925468bff1acdc0506f` hook can load an explicitly supplied helper path offline; the Node 20 compatibility probe used the exact reviewed helper and created a sink. That is compatibility evidence only.

The current D66 source still derives the helper from `RUNTIME_CHECKOUT/tests/helpers/p2_commit_phase_capture.py`, while Runtime 5e9ad has no such helper, and `serviceRecipe` does not carry a reviewed helper path/hash. Therefore normal attachment is **PENDING**. The D66 owner must add/accept an explicit reviewed diagnostic helper path/hash route while preserving the production Runtime checkout and manifest at 5e9ad. If the source guard insists the helper live inside Runtime home, the precise route is blocked until an approved test-helper merge/adoption; this review does not invent that change.

No normal production preflight, actual sampler-active full-body request, browser tour, element cause, or P2 GO is claimed.
