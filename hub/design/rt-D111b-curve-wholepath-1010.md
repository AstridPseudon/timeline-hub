# D111b whole-path investigation

Decision: corrected measurement seam; no product cost is established by the existing native run.

## Finding

The native 0905 and native 0958 packets measured different things. Native 0905 reported 208 “source-document reads” by classifying a suffix of generic `RequestCommitPort._read` records by position, totaling 22.891 seconds (97.2% of its `_read` wall). Native 0958 directly instrumented `RequestCommitPort._document` and the store document-capture hook. Both direct source counters were zero in baseline and candidate. Its ordinary `_read` wall was 17.353s versus 18.255s, with 2,058 deepcopies in both and two manifest pins per request.

This is a measurement-seam discrepancy, not evidence that either candidate or harness is faulty. Native 0958’s executed request is a direct Runtime `commitTimeline` POST containing a `doc.patch`, one step, reads, `merge: atomic`, and `source: {via: app}`. It does not carry a source-bearing Agent command, `schema_source`, or a `clip.anchor` source choice. The `doc.patch` executor applies structural changes; it does not call Agent `_hydrate` source methods. Therefore the request legitimately exercises authentication, ordinary head/history/closure reads, patch execution, receipts and readback, but not the source-document capture path.

## Whole-path trace

Production wiring is intact. Runtime daemon startup loads the explicit `astrid.sdk.timeline.commit.create_runtime_commit_service` factory and registers the provider. `commit_timeline` validates the v2 request shape, authenticates the publisher, creates `RequestCommitPort`, and the coordinator calls `provider.commit(provider_context, port)`. The candidate changes are confined to the request port/store snapshot seam; provider import, bootstrap and coordinator files are unchanged between Runtime `8b3895cf141f5b7359cceacefde62c9a9475eabf` and `02b244732e788f22d8e3d9e9497387543ab410fa`.

The genuine source path is: Agent `_hydrate` obtains dependency-manifest documents and explicit `schema_source`/`clip.anchor` pins; it calls `port.transcript_source` or `port.config_source`; Runtime `_document` validates reachability and calls `TimelineCommitStore._capture_document_input`; the store capture performs the existing source binding/live capture, digest and schema checks. The candidate’s request-private snapshot is only used when this path is reached. Native 0958’s zero direct source counters show it did not reach that path.

## Exact corrected comparator

Use the same Runtime baseline/candidate pair (`8b3895cf` versus `02b24473`), the same registered Agent provider (`070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`), same authenticated inputs, same process, and the same unforced growing journey. The sole missing condition is an existing real source-bearing Agent fixture/client path that produces a valid `schema_source` project-pack input or `clip.anchor` transcript input. Do not invent a source payload, old profile, cache, or generic cross-request memo.

Acceptance requires nonzero direct `source_document_calls` and `source_store_calls` in both stages, equal source-pin/capture counts, and measurements for source-document/store wall, ordinary `_read`/store wall, deepcopy/finite-json counts, canonical receipt/readback equality, mutation isolation, and authorization/refusal witnesses. A drop at the direct source seam identifies the candidate’s intended product cost as source capture/validation. No drop leaves the measured source capture SQL/digest/deepcopy work as the next existing port/store seam. Until that comparator runs, neither conclusion is justified.

## Contract and unknowns

The inspected v2 contract preserves request fields `api_version`, both scope IDs, both base IDs, `commands`, `label`, `steps`, `patch`, `reads`, `merge`, `dry_run`, and the HTTP `Idempotency-Key`. Success remains `accepted`/`merged` with canonical receipt/result data, head/accepted IDs, effects, bindings and dependencies; conflicts/invalid requests and dry-run previews retain their distinct shapes. No contract change is proposed.

Unknowns are limited to the unmeasured source-bearing path and its source-specific wall/copy breakdown. Native0958 remains the owner of the actual measurement/final report; this worker did not duplicate or alter its diagnostic and made no runtime, test, generated, pin, hub or deletion changes.

Sources: `PLAN.md`; native0958 `evidence/D111b-failure-summary.json`; native0905 `report.md`; cost-wholepath-0923 `evidence/progress.md`; Runtime `daemon.py:239-260`, `timeline_commit_provider.py:70-93`, `service.py:2447-2525`, `timeline_commit_execution.py:222-275`, `timeline_commit_port.py:214-300,302-340,413-446`, `timeline_commit_store.py:547-572`; Agent pin 070dfc `commit.py:442-500,1319-1360`, `sync.py:525-558`; `contract/commit-v2.md:60-150,703-715`; frozen R4 refs `11caf1d9...` and `31c7ac3a...` inspected read-only.
